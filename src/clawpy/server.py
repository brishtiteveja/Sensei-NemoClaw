"""DikkhaClaw — Koji-style Bangla AI tutor backend.

Run:
    python -m clawpy.server
    # or
    uvicorn clawpy.server:app --port 4039

Built on the ClawPy engine. Creates a tutor Engine per student session,
uses Socratic dialogue to teach, and streams responses as SSE.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import re
import uuid
from datetime import datetime, timezone
from typing import Any

from clawpy.config.config import Config
from clawpy.engine.engine import Engine
from clawpy.provider.base import EventType, StreamEvent
from clawpy.tool.permission import PermissionEnforcer, PermissionMode
from clawpy.tool.registry import ToolRegistry

logger = logging.getLogger("clawpy.server")

# Concurrency limiter — subscription rate limits are tight
_query_semaphore = asyncio.Semaphore(2)

# ── Engine factory ─────────────────────────────────────────────────────────

_engines: dict[str, Engine] = {}


def _create_provider(config: Config):
    """Create the LLM provider from config."""
    import clawpy.provider.anthropic  # noqa: F401
    import clawpy.provider.openai  # noqa: F401
    import clawpy.provider.gemini  # noqa: F401
    import clawpy.provider.ollama  # noqa: F401
    import clawpy.provider.deepseek  # noqa: F401

    from clawpy.provider.registry import create

    provider_cfg = config.provider_config()
    return create(config.provider, provider_cfg)


def _build_tools(engine: Engine) -> ToolRegistry:
    """Register tutor tools for Dikkha."""
    from clawpy.tool.web_fetch import WebFetchTool
    from clawpy.tool.tutor.question_lookup import QuestionLookupTool
    from clawpy.tool.tutor.student_profile import StudentProfileTool
    from clawpy.tool.tutor.knowledge_check import KnowledgeCheckTool

    registry = ToolRegistry()
    registry.register(QuestionLookupTool())
    registry.register(StudentProfileTool())
    registry.register(KnowledgeCheckTool())
    registry.register(WebFetchTool())
    return registry


async def _connect_mcp_servers(registry: ToolRegistry, config: Config) -> list:
    """Discover and connect MCP servers, adding their tools to the registry."""
    from clawpy.mcp.client import MCPClient, MCPToolWrapper, load_mcp_configs

    mcp_configs = load_mcp_configs(config.work_dir)
    clients = []

    for server_cfg in mcp_configs:
        try:
            client = MCPClient(server_cfg)
            await client.connect()
            for spec in client.tool_specs():
                registry.register(MCPToolWrapper(client, spec))
            clients.append(client)
            logger.info("Connected MCP server '%s' with %d tools", server_cfg.name, len(client.tools))
        except Exception as e:
            logger.warning("Failed to connect MCP server '%s': %s", server_cfg.name, e)

    return clients


# Where a runtime model choice is persisted, so a restart keeps whatever the operator
# last selected in the app rather than snapping back to the launch environment.
_MODEL_STATE_PATH = os.path.join(
    os.environ.get("SENSEI_DATA_DIR", os.path.join(os.path.dirname(__file__), "..", "..", "data")),
    "model_choice.json",
)


def _load_model_choice() -> dict | None:
    try:
        with open(_MODEL_STATE_PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def apply_model_choice(mode: str, model: str, *, persist: bool = True) -> dict:
    """Switch the active provider/model for the whole server.

    Applied by writing the environment rather than holding a parallel override dict:
    `translate.py` and everything else already resolve their provider from the same
    env, so a single source of truth avoids the case where chat moves to a new model
    while translation quietly stays on the old one.

    Cached engines hold a constructed provider, so they must be dropped or existing
    sessions would keep talking to the previous model.
    """
    mode = (mode or "").lower()
    if mode == "local":
        base_url = os.environ.get("SENSEI_LOCAL_BASE_URL", "")
        api_key = os.environ.get("SENSEI_LOCAL_API_KEY", "")
        if not base_url:
            raise ValueError("SENSEI_LOCAL_BASE_URL is not configured")
        os.environ["CLAWPY_PROVIDER"] = "openai"  # the router is OpenAI-compatible
        os.environ["OPENAI_BASE_URL"] = base_url
        os.environ["OPENAI_API_KEY"] = api_key
    elif mode == "cloud":
        api_key = os.environ.get("SENSEI_CLOUD_API_KEY", "") or os.environ.get("GEMINI_API_KEY", "")
        if not api_key:
            raise ValueError("No cloud API key configured (SENSEI_CLOUD_API_KEY)")
        os.environ["CLAWPY_PROVIDER"] = "gemini"
        os.environ["GEMINI_API_KEY"] = api_key
        # Leaving a stale OpenAI base URL set would send Gemini traffic to the router.
        os.environ.pop("OPENAI_BASE_URL", None)
        os.environ.pop("OPENAI_API_KEY", None)
    else:
        raise ValueError(f"mode must be 'local' or 'cloud', got {mode!r}")

    os.environ["CLAWPY_MODEL"] = model
    _engines.clear()

    choice = {"mode": mode, "model": model}
    if persist:
        try:
            os.makedirs(os.path.dirname(_MODEL_STATE_PATH), exist_ok=True)
            with open(_MODEL_STATE_PATH, "w", encoding="utf-8") as f:
                json.dump(choice, f)
        except Exception as e:
            logger.warning("Could not persist model choice: %s", e)
    return choice


def _get_server_config() -> Config:
    """Build config for server mode."""
    cfg = Config()
    cfg.work_dir = os.environ.get("CLAWPY_WORK_DIR", os.getcwd())
    cfg.provider = os.environ.get("CLAWPY_PROVIDER", "gemini")
    cfg.model = os.environ.get("CLAWPY_MODEL", "gemini-2.5-flash")
    cfg.max_tokens = int(os.environ.get("CLAWPY_MAX_TOKENS", "16384"))
    cfg.permission_mode = "bypass"
    return cfg


async def get_or_create_engine(session_id: str | None = None) -> tuple[str, Engine]:
    """Get an existing engine or create a new one for a session."""
    from clawpy.session.session import SessionStore

    sid = session_id or str(uuid.uuid4())

    if sid in _engines:
        return sid, _engines[sid]

    config = _get_server_config()
    provider = _create_provider(config)
    enforcer = PermissionEnforcer(
        mode=PermissionMode.BYPASS,
        work_dir=config.work_dir,
    )

    engine = Engine(
        provider=provider,
        tools=ToolRegistry(),
        enforcer=enforcer,
        config=config,
    )
    engine.tools = _build_tools(engine)

    await _connect_mcp_servers(engine.tools, config)

    from clawpy.prompts.dikkha import build_dikkha_prompt
    engine.set_system_prompt(build_dikkha_prompt())

    store = SessionStore(sid)
    previous = store.load_session()
    if previous:
        engine.messages = previous
        logger.info("Resumed session '%s' with %d messages", sid, len(previous))
    else:
        store.save_meta(config.model, config.work_dir)
    engine.session_store = store

    _engines[sid] = engine
    return sid, engine


# ── SSE formatting ─────────────────────────────────────────────────────────

def _format_sse(event: str, data: dict) -> str:
    """Format a single SSE event line."""
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


def stream_event_to_sse(
    event: StreamEvent,
    tools_called: list[str],
) -> str | None:
    """Convert a ClawPy StreamEvent to an SSE-formatted string."""
    match event.type:
        case EventType.DELTA:
            if event.delta and event.delta.text:
                return _format_sse("token", {"text": event.delta.text})
        case EventType.TOOL_START:
            if event.tool_call:
                tools_called.append(event.tool_call.name)
                return _format_sse("tool_use", {
                    "name": event.tool_call.name,
                    "input": event.tool_call.input if hasattr(event.tool_call, 'input') else {},
                })
        case EventType.TOOL_END:
            if event.tool_call:
                return _format_sse("tool_result", {
                    "name": event.tool_call.name,
                    "summary": f"Completed {event.tool_call.name}",
                })
        case EventType.ERROR:
            msg = event.delta.text if event.delta else "Unknown error"
            return _format_sse("error", {"message": msg})
    return None


# ── FastAPI app ────────────────────────────────────────────────────────────

try:
    from fastapi import FastAPI, HTTPException, Request
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import StreamingResponse
    from pydantic import BaseModel
except ImportError:
    raise ImportError("FastAPI is required for server mode: pip install fastapi uvicorn")


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None
    system_prompt: str | None = None
    context_type: str | None = None
    context_id: str | None = None
    context_data: dict | None = None


class SuggestionsResponse(BaseModel):
    suggestions: list[str]


class HandoffRequest(BaseModel):
    """An image sent from a paired phone to a waiting desktop session."""

    image: str
    kind: str = "image"  # "sketch" when drawn on the phone, "image" when a photo


class AttemptSummaryRequest(BaseModel):
    """One analysable row per attempt at a problem."""

    session: str
    summary: dict
    learner: str | None = None


class ObserveRequest(BaseModel):
    """A batch of workspace events from one learner session."""

    session: str
    events: list[dict]
    learner: str | None = None


class CoachRequest(BaseModel):
    """A look at the student's work-in-progress, for a Socratic nudge."""

    image: str
    problem: str | None = None
    language: str | None = None
    # Per-role overrides; either may name a cloud model while the other stays local.
    reading_model: str | None = None
    coaching_model: str | None = None


class SeeRequest(BaseModel):
    """A piece of the student's own work for the tutor to look at.

    `image` is a data URI (or bare base64) of a scratchpad sketch or an uploaded
    photo; `problem` is what they were asked to solve, when the client knows it.
    """

    image: str
    problem: str | None = None
    language: str | None = None


app = FastAPI(
    title="DikkhaClaw",
    description="দীক্ষা — Koji-style Bangla AI Tutor for ShikkhaDikkha",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def _restore_model_choice() -> None:
    """Re-apply whatever model was last chosen in the app.

    Without this a restart silently reverts to the launch environment, so an operator
    who switched models in Settings would find it undone by the next deploy without
    any indication why.
    """
    choice = _load_model_choice()
    if not choice:
        return
    try:
        apply_model_choice(choice["mode"], choice["model"], persist=False)
        print(f"restored model choice: {choice['mode']}/{choice['model']}")
    except Exception as e:
        logger.warning("Could not restore saved model choice: %s", e)


@app.get("/dikkhatutor")
async def dikkha_chat_ui():
    """Browser-based chat UI for testing Dikkha tutor."""
    from fastapi.responses import HTMLResponse
    return HTMLResponse(content=_CHAT_HTML)


@app.post("/tutor/stream")
async def tutor_stream(req: ChatRequest):
    """Stream a tutor response as SSE events — main chat endpoint."""
    session_id, engine = await get_or_create_engine(req.session_id)

    user_lang = (req.context_data or {}).get("language")
    if req.system_prompt:
        engine.set_system_prompt(req.system_prompt)
    else:
        from clawpy.prompts.dikkha import build_dikkha_prompt, build_lesson_context
        ctx = req.context_data or {}
        if req.context_id:
            ctx["context_id"] = req.context_id

        # Check if this is a structured lesson with rich content
        lesson_id = ctx.get("lesson_id")
        lesson_step = ctx.get("lesson_step", 1)
        lesson_ctx = build_lesson_context(lesson_id, lesson_step) if lesson_id else None

        base_prompt = build_dikkha_prompt(
            context_type=req.context_type or "free_chat",
            context_data=ctx or None,
            language=user_lang,
        )

        if lesson_ctx:
            engine.set_system_prompt(base_prompt + lesson_ctx)
        else:
            engine.set_system_prompt(base_prompt)

    tools_called: list[str] = []
    collected_events: list[StreamEvent] = []

    def on_stream(event: StreamEvent) -> None:
        collected_events.append(event)

    async def generate():
        yield _format_sse("progress", {"step": "starting", "session_id": session_id})

        task = asyncio.create_task(
            engine.run_turn(req.message, on_stream=on_stream)
        )

        TAG_OPEN = "<<SUGGESTIONS>>"
        TAG_CLOSE = "<</SUGGESTIONS>>"
        hold_buf = ""
        capturing = False

        def _process_chunk(chunk: str):
            """Returns list of SSE strings to yield."""
            nonlocal hold_buf, capturing
            results = []

            if capturing:
                hold_buf += chunk
                return results

            combined = hold_buf + chunk

            if TAG_OPEN in combined:
                before, after = combined.split(TAG_OPEN, 1)
                if before.strip():
                    results.append(_format_sse("token", {"text": before}))
                hold_buf = after
                capturing = True
                return results

            # Check if end of combined could be start of TAG_OPEN
            for i in range(min(len(TAG_OPEN) - 1, len(combined)), 0, -1):
                if TAG_OPEN.startswith(combined[-i:]):
                    safe = combined[:-i]
                    hold_buf = combined[-i:]
                    if safe:
                        results.append(_format_sse("token", {"text": safe}))
                    return results

            hold_buf = ""
            if combined:
                results.append(_format_sse("token", {"text": combined}))
            return results

        while not task.done():
            while collected_events:
                ev = collected_events.pop(0)
                if ev.type == EventType.DELTA and ev.delta and ev.delta.text:
                    for sse in _process_chunk(ev.delta.text):
                        yield sse
                else:
                    sse = stream_event_to_sse(ev, tools_called)
                    if sse:
                        yield sse
            await asyncio.sleep(0.05)

        while collected_events:
            ev = collected_events.pop(0)
            if ev.type == EventType.DELTA and ev.delta and ev.delta.text:
                for sse in _process_chunk(ev.delta.text):
                    yield sse
            else:
                sse = stream_event_to_sse(ev, tools_called)
                if sse:
                    yield sse

        suggestions = []
        summary = None
        if capturing:
            raw = hold_buf.replace(TAG_CLOSE, "").strip()
            # Check if buffer has both SUMMARY and SUGGESTIONS
            import re as _re
            summary_match = _re.search(r'<<SUMMARY>>(.+?)<<//SUMMARY>>', raw, _re.DOTALL)
            if summary_match:
                try:
                    summary = json.loads(summary_match.group(1).strip())
                except Exception:
                    pass
                raw = _re.sub(r'<<SUMMARY>>.*?<<//SUMMARY>>', '', raw, flags=_re.DOTALL).strip()

            if raw:
                try:
                    parsed = json.loads(raw)
                    if isinstance(parsed, list):
                        suggestions = [s for s in parsed if isinstance(s, str)][:4]
                except Exception:
                    m = _re.findall(r'"([^"]+)"', raw)
                    if m:
                        suggestions = m[:4]
        elif hold_buf.strip():
            # Check for summary in non-captured buffer too
            import re as _re
            summary_match = _re.search(r'<<SUMMARY>>(.+?)<<//SUMMARY>>', hold_buf, _re.DOTALL)
            if summary_match:
                try:
                    summary = json.loads(summary_match.group(1).strip())
                except Exception:
                    pass
                clean = _re.sub(r'<<SUMMARY>>.*?<<//SUMMARY>>', '', hold_buf, flags=_re.DOTALL).strip()
                if clean:
                    yield _format_sse("token", {"text": clean})
            else:
                yield _format_sse("token", {"text": hold_buf})

        if summary:
            yield _format_sse("summary", summary)
        if suggestions:
            yield _format_sse("suggestions", {"suggestions": suggestions})

        result = task.result()
        yield _format_sse("done", {
            "session_id": session_id,
            "model": engine.config.model,
            "tools_called": tools_called,
            "stop_reason": result.stop_reason.value if result.stop_reason else "end_turn",
            "usage": {
                "input_tokens": result.usage.input_tokens,
                "output_tokens": result.usage.output_tokens,
            },
        })

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.get("/tutor/suggestions", response_model=SuggestionsResponse)
async def get_suggestions(context_type: str = "free_chat", subject: str | None = None):
    """Return context-aware starter prompts for the chat UI."""
    if context_type == "exam_question":
        return SuggestionsResponse(suggestions=[
            "এই প্রশ্নটা কিভাবে সমাধান করবো?",
            "Can you give me a hint?",
            "এখানে কোন concept কাজে লাগবে?",
            "Why is my answer wrong?",
        ])
    elif context_type == "exam_review":
        return SuggestionsResponse(suggestions=[
            "আমার সবচেয়ে দুর্বল বিষয় কোনটা?",
            "Explain my mistakes one by one",
            "এই ভুলগুলো থেকে কি pattern দেখা যাচ্ছে?",
            "Give me practice questions on my weak areas",
        ])
    elif subject:
        subject_prompts = {
            "physics": ["Newton's laws বুঝিয়ে বলো", "Solve a circuit problem with me"],
            "chemistry": ["Organic naming practice করি", "Acid-base কনসেপ্ট clear করো"],
            "math": ["Integration practice করি", "Logarithm এর basic থেকে শুরু করো"],
            "biology": ["Cell biology revision করি", "Photosynthesis explain করো"],
        }
        return SuggestionsResponse(suggestions=subject_prompts.get(subject, [
            "আজ কোন বিষয় পড়বে?",
            "তোমার দুর্বল বিষয় নিয়ে কাজ করি?",
            "একটা mock test দিতে চাও?",
            "গতকালের ভুলগুলো review করি?",
        ]))
    return SuggestionsResponse(suggestions=[
        "আজ কোন বিষয় পড়বে?",
        "Physics practice শুরু করি?",
        "BUET এর গত বছরের প্রশ্ন দেখাও",
        "আমার weak areas কী কী?",
        "একটা quick quiz দাও!",
        "Calculus এর chain rule বুঝিয়ে দাও",
    ])


class HintRequest(BaseModel):
    question_id: str
    student_answer: str | None = None
    session_id: str | None = None
    user_id: str | None = None


class ExplainRequest(BaseModel):
    question_id: str
    student_answer: str | None = None
    correct_answer: str | None = None
    session_id: str | None = None


@app.post("/tutor/hint")
async def tutor_hint(req: HintRequest):
    """Quick Socratic hint for a specific question — non-streaming, fast."""
    import json as _json
    # Load the question
    bank_path = os.environ.get(
        "DIKKHA_QUESTION_BANK",
        os.path.join(os.path.dirname(__file__), "..", "..", "data", "question_bank.json"),
    )
    try:
        with open(bank_path, encoding="utf-8") as f:
            questions = _json.load(f)
    except FileNotFoundError:
        return {"hint": "Question bank not found.", "error": True}

    question = next((q for q in questions if q["id"] == req.question_id), None)
    if not question:
        return {"hint": "Question not found.", "error": True}

    # Build a focused prompt for a quick hint
    session_id, engine = await get_or_create_engine(req.session_id)
    from clawpy.prompts.dikkha import build_dikkha_prompt
    engine.set_system_prompt(build_dikkha_prompt(
        context_type="exam_question",
        context_data=question,
    ))

    hint_prompt = f"I'm stuck on this question."
    if req.student_answer:
        hint_prompt += f" I think the answer is {req.student_answer}. Am I right?"
    hint_prompt += " Give me a hint without telling me the answer."

    result = await engine.run_turn(hint_prompt)

    # Extract text from result
    text = ""
    for msg in result.messages:
        if msg.role.value == "assistant":
            for block in msg.content:
                if hasattr(block, 'text') and block.text:
                    text = block.text
                    break

    return {
        "hint": text,
        "session_id": session_id,
        "question_id": req.question_id,
    }


@app.post("/tutor/explain")
async def tutor_explain(req: ExplainRequest):
    """Full step-by-step explanation after exam — non-streaming."""
    import json as _json
    bank_path = os.environ.get(
        "DIKKHA_QUESTION_BANK",
        os.path.join(os.path.dirname(__file__), "..", "..", "data", "question_bank.json"),
    )
    try:
        with open(bank_path, encoding="utf-8") as f:
            questions = _json.load(f)
    except FileNotFoundError:
        return {"explanation": "Question bank not found.", "error": True}

    question = next((q for q in questions if q["id"] == req.question_id), None)
    if not question:
        return {"explanation": "Question not found.", "error": True}

    session_id, engine = await get_or_create_engine(req.session_id)
    from clawpy.prompts.dikkha import build_dikkha_prompt
    engine.set_system_prompt(build_dikkha_prompt(
        context_type="exam_review",
        context_data={"mistakes": [question]},
    ))

    prompt = f"I got this question wrong."
    if req.student_answer:
        prompt += f" I chose {req.student_answer}."
    if req.correct_answer:
        prompt += f" The correct answer is {req.correct_answer}."
    prompt += " Please explain step by step why the correct answer is right and where I went wrong."

    result = await engine.run_turn(prompt)

    text = ""
    for msg in result.messages:
        if msg.role.value == "assistant":
            for block in msg.content:
                if hasattr(block, 'text') and block.text:
                    text = block.text
                    break

    return {
        "explanation": text,
        "session_id": session_id,
        "question_id": req.question_id,
    }


MODEL_MAX_OUTPUT_TOKENS = {
    "claude-opus-4-8": 128000,
    "claude-opus-4-7": 128000,
    "claude-opus-4-6": 128000,
    "claude-sonnet-4-6": 64000,
    "claude-sonnet-4-5-20250929": 64000,
    "claude-haiku-4-5-20251001": 64000,
}


def _resolve_max_tokens(model: str | None, requested: int | None) -> int:
    """Use the model's actual max if no explicit limit requested."""
    if requested and requested > 0:
        return requested
    if model and model in MODEL_MAX_OUTPUT_TOKENS:
        return MODEL_MAX_OUTPUT_TOKENS[model]
    for key, val in MODEL_MAX_OUTPUT_TOKENS.items():
        if model and key.startswith(model):
            return val
    return 64000


class QueryRequest(BaseModel):
    """Simple non-streaming LLM query — no agentic loop, no tools."""
    prompt: str
    system_prompt: str | None = None
    model: str | None = None
    provider: str | None = None
    max_tokens: int | None = None
    temperature: float | None = None
    fallback_models: list[str] | None = None


@app.post("/tutor/query")
async def simple_query(req: QueryRequest):
    """Direct LLM call — fast, no tools, no agentic loop.

    Use for batch pipeline tasks: content extraction, summarization,
    selector generation, classification, etc.

    Supports provider/model override and automatic fallback chain.
    """
    models_to_try = []
    if req.model:
        models_to_try.append((req.provider, req.model))
    else:
        models_to_try.append((None, None))

    if req.fallback_models:
        for fm in req.fallback_models:
            if ":" in fm:
                p, m = fm.split(":", 1)
                models_to_try.append((p, m))
            else:
                models_to_try.append((None, fm))

    async with _query_semaphore:
        return await _execute_query(req, models_to_try)


async def _execute_query(req: QueryRequest, models_to_try: list):
    import time as _time
    from clawpy.provider.base import Request as ProviderRequest
    from clawpy.types import ContentType, Role, text_message

    last_error = None
    for provider_name, model_name in models_to_try:
        cfg = _get_server_config()
        if provider_name:
            cfg.provider = provider_name
        if model_name:
            cfg.model = model_name

        provider = _create_provider(cfg)
        target_model = model_name or cfg.model

        messages = [text_message(Role.USER, req.prompt)]

        resolved_max = _resolve_max_tokens(target_model, req.max_tokens)

        provider_req = ProviderRequest(
            model=target_model,
            system=req.system_prompt or "",
            messages=messages,
            tools=[],
            max_tokens=resolved_max,
            temperature=req.temperature,
        )

        # Retry with exponential backoff for rate limits (429)
        max_retries = 5
        for attempt in range(max_retries):
            try:
                start = _time.time()
                response = await provider.send(provider_req)
                elapsed = _time.time() - start

                content = ""
                for block in response.content:
                    if block.type == ContentType.TEXT:
                        content += block.text

                return {
                    "success": True,
                    "content": content,
                    "model": target_model,
                    "provider": provider_name or cfg.provider,
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                    "execution_time": round(elapsed, 2),
                }
            except Exception as e:
                last_error = str(e)
                if "429" in str(e) and attempt < max_retries - 1:
                    wait = 2 ** attempt * 10  # 10s, 20s, 40s, 80s, 160s
                    logger.info(f"Rate limited, retrying in {wait}s (attempt {attempt + 1}/{max_retries})")
                    await asyncio.sleep(wait)
                    continue
                prov = provider_name or "default"
                mod = model_name or "default"
                logger.warning(f"Query failed ({prov}/{mod}): {last_error}")
                break

    return {"success": False, "error": last_error or "All models failed", "content": ""}


@app.get("/tutor/health")
async def health():
    return {"status": "ok", "engines": len(_engines)}


@app.get("/tutor/accounts")
async def account_status():
    """Show account pool status — which accounts are available, rate-limited, etc."""
    try:
        from clawpy.auth.account_pool import get_pool
        pool = get_pool()
        return pool.get_status()
    except Exception as e:
        return {"error": str(e), "total_accounts": 0}


# ── Curriculum API ────────────────────────────────────────────────────────

class LessonPlanRequest(BaseModel):
    student_id: str
    target_exam: str = "general"  # du, buet, medical, gst, general
    difficulty: str = "medium"  # easy, medium, hard
    subjects: list[str] | None = None
    weak_topics: list[str] | None = None
    max_lessons: int | None = None


def _prefer_bn_titles(node) -> None:
    """Promote authored `title_bn` into `title` throughout the tree.

    Lets the client read `title` unconditionally instead of branching on language --
    the binary `useBn ? title_bn : title` pattern is exactly what broke every third
    language, silently falling back to English.
    """
    if isinstance(node, dict):
        if isinstance(node.get("title_bn"), str) and node["title_bn"]:
            node["title"] = node["title_bn"]
        for value in node.values():
            _prefer_bn_titles(value)
    elif isinstance(node, list):
        for item in node:
            _prefer_bn_titles(item)


async def _localise_titles(node, lang: str | None) -> None:
    """Translate curriculum titles/descriptions in place, into `lang`.

    The curriculum ships only `title` (English) and `title_bn` (Bangla), so a student on
    any third language saw English subject, unit and lesson names beside a translated UI.
    Sensei's claim is that a student works entirely in their own language, so the
    curriculum has to follow the setting like everything else does.

    Each distinct string is one cache key. Subject and unit names repeat heavily across
    the tree and across students, so after the first pass this is nearly all cache hits.
    """
    if not lang or lang == "en":
        return

    from clawpy.curriculum.translate import translate_text

    targets: list[tuple[dict, str]] = []

    def walk(n) -> None:
        if isinstance(n, dict):
            for key in ("title", "description"):
                if isinstance(n.get(key), str) and n[key]:
                    targets.append((n, key))
            for value in n.values():
                walk(value)
        elif isinstance(n, list):
            for item in n:
                walk(item)

    walk(node)
    if not targets:
        return

    uniq = sorted({container[key] for container, key in targets})
    results = await asyncio.gather(
        *(translate_text(text, lang, "en") for text in uniq),
        return_exceptions=True,
    )
    mapping = {
        src: (out if isinstance(out, str) and out else src)
        for src, out in zip(uniq, results)
    }
    for container, key in targets:
        container[key] = mapping.get(container[key], container[key])


# Models known to work on the cloud provider. Deliberately a short curated list rather
# than everything the API advertises: /v1beta/models lists ids that 404 on an actual
# call (gemini-2.5-flash is "no longer available to new users"), so showing the raw
# catalogue would offer the operator choices that fail only once selected.
_CLOUD_MODELS = [
    {"id": "gemini-3.5-flash-lite", "label": "Gemini 3.5 Flash-Lite", "note": "cheapest"},
    {"id": "gemini-3.6-flash", "label": "Gemini 3.6 Flash", "note": "balanced"},
    {"id": "gemini-3.7-flash", "label": "Gemini 3.7 Flash", "note": "best quality"},
]

# Vision is required for the photo/handwriting flow. A text-only model silently breaks
# it, so the app needs to be able to warn rather than let it fail at the camera.
_VISION_MODEL_HINTS = ("-vl-", "glm-4.6v", "internvl", "qwen3.6-27b")


@app.get("/admin/models")
async def list_model_options():
    """What the settings screen offers, plus which model is live right now."""
    current_mode = "local" if os.environ.get("CLAWPY_PROVIDER") == "openai" else "cloud"
    current = {"mode": current_mode, "model": os.environ.get("CLAWPY_MODEL", "")}

    local: list[dict] = []
    resident: str | None = None
    base_url = os.environ.get("SENSEI_LOCAL_BASE_URL", "")
    if base_url:
        import httpx
        key = os.environ.get("SENSEI_LOCAL_API_KEY", "")
        headers = {"Authorization": f"Bearer {key}"} if key else {}
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                r = await client.get(f"{base_url}/models", headers=headers)
                r.raise_for_status()
                for m in r.json().get("data", []):
                    mid = m["id"]
                    local.append({
                        "id": mid,
                        "label": mid,
                        "vision": any(h in mid for h in _VISION_MODEL_HINTS),
                    })
                local.sort(key=lambda m: (not m["vision"], m["id"]))
                # Which one is actually resident -- selecting any other costs a cold swap.
                h = await client.get(f"{base_url.removesuffix('/v1')}/health")
                loaded = h.json().get("loaded") or []
                resident = loaded[0] if loaded else None
        except Exception as e:
            logger.warning("Could not list local models: %s", e)

    return {
        "current": current,
        "resident_local_model": resident,
        "cloud": _CLOUD_MODELS,
        "local": local,
        # Surfaced so the client can warn before a switch instead of appearing to hang.
        "local_swap_warning": (
            "Only one local model stays loaded. Choosing a different one takes "
            "1-5 minutes to swap and affects everyone using this box."
        ),
    }


@app.post("/admin/model")
async def set_model(body: dict):
    """Switch the active provider/model. Takes effect immediately for new turns."""
    try:
        choice = apply_model_choice(body.get("mode", ""), body.get("model", ""))
    except ValueError as e:
        raise HTTPException(400, str(e))

    is_vision = any(h in choice["model"] for h in _VISION_MODEL_HINTS)
    return {
        "ok": True,
        **choice,
        "vision": is_vision,
        "warning": None if is_vision or choice["mode"] == "cloud" else (
            "This model has no vision support, so reading photos of handwritten work "
            "will not work until you switch back to a vision model."
        ),
    }


@app.get("/curriculum/subjects")
async def list_subjects(lang: str | None = None):
    """List all available subjects with their unit/lesson counts."""
    from clawpy.curriculum.planner import get_subject_overview
    from clawpy.curriculum.models import SubjectId

    results = []
    for sid in SubjectId:
        overview = get_subject_overview(sid)
        if "error" not in overview:
            results.append({
                "id": overview["subject"],
                "title": overview["title"],
                "title_bn": overview["title_bn"],
                "icon": overview["icon"],
                "target_exams": overview["target_exams"],
                "total_units": overview["total_units"],
                "total_lessons": overview["total_lessons"],
            })

    if lang == "bn":
        # Bangla names are authored, not machine-translated -- always prefer them.
        for r in results:
            r["title"] = r.get("title_bn") or r["title"]
    else:
        await _localise_titles(results, lang)
    return {"subjects": results}


@app.get("/curriculum/subjects/{subject_id}")
async def get_subject(subject_id: str, lang: str | None = None):
    """Get full curriculum tree for a subject — units and lessons."""
    from clawpy.curriculum.planner import get_subject_overview
    from clawpy.curriculum.models import SubjectId

    try:
        sid = SubjectId(subject_id)
    except ValueError:
        return {"error": f"Unknown subject: {subject_id}"}

    overview = get_subject_overview(sid)
    if lang == "bn":
        _prefer_bn_titles(overview)
    else:
        await _localise_titles(overview, lang)
    return overview


@app.get("/curriculum/lessons/{lesson_id}")
async def get_lesson(lesson_id: str):
    """Get details of a specific lesson."""
    from clawpy.curriculum.planner import get_lesson_detail
    result = get_lesson_detail(lesson_id)
    if not result:
        return {"error": f"Lesson not found: {lesson_id}"}
    return result


@app.get("/curriculum/ready-plans")
async def list_ready_plans():
    """List pre-built lesson plans with real admission questions."""
    import glob
    plans_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "plans")
    plans = []
    for path in sorted(glob.glob(os.path.join(plans_dir, "*.json"))):
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            plans.append({
                "file": os.path.basename(path),
                "name": data.get("plan_name", ""),
                "name_bn": data.get("plan_name_bn", ""),
                "target_exam": data.get("target_exam", ""),
                "difficulty": data.get("difficulty", ""),
                "total_lessons": data.get("total_lessons", 0),
                "total_exercises": data.get("total_exercises", 0),
            })
        except Exception:
            pass
    return {"plans": plans}


@app.get("/curriculum/ready-plans/{plan_file}")
async def get_ready_plan(plan_file: str, lesson_index: int | None = None):
    """Get a pre-built plan. Optionally get a single lesson by index."""
    plans_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "plans")
    path = os.path.join(plans_dir, plan_file)
    if not os.path.exists(path):
        return {"error": f"Plan not found: {plan_file}"}

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    if lesson_index is not None:
        if 0 <= lesson_index < len(data.get("lessons", [])):
            return data["lessons"][lesson_index]
        return {"error": f"Lesson index {lesson_index} out of range"}

    # Return plan overview without full exercises (too large)
    overview = {k: v for k, v in data.items() if k != "lessons"}
    overview["lessons"] = [
        {
            "lesson_id": l["lesson_id"],
            "lesson_title": l["lesson_title"],
            "lesson_title_bn": l["lesson_title_bn"],
            "subject": l["subject"],
            "subject_title_bn": l["subject_title_bn"],
            "unit_title_bn": l["unit_title_bn"],
            "exercise_count": l["exercise_count"],
            "estimated_minutes": l["estimated_minutes"],
            "xp_reward": l["xp_reward"],
        }
        for l in data.get("lessons", [])
    ]
    return overview


@app.post("/curriculum/plan")
async def create_lesson_plan(req: LessonPlanRequest):
    """Generate a personalized Duolingo-style lesson plan."""
    from clawpy.curriculum.planner import generate_lesson_plan
    from clawpy.curriculum.models import Difficulty, SubjectId, TargetExam

    try:
        target = TargetExam(req.target_exam)
    except ValueError:
        target = TargetExam.GENERAL

    try:
        diff = Difficulty(req.difficulty)
    except ValueError:
        diff = Difficulty.MEDIUM

    subjects = None
    if req.subjects:
        subjects = []
        for s in req.subjects:
            try:
                subjects.append(SubjectId(s))
            except ValueError:
                pass

    plan = generate_lesson_plan(
        student_id=req.student_id,
        target_exam=target,
        difficulty=diff,
        subjects=subjects or None,
        weak_topics=req.weak_topics,
        max_lessons=req.max_lessons,
    )

    return {
        "id": plan.id,
        "title": plan.title,
        "title_bn": plan.title_bn,
        "target_exam": plan.target_exam.value,
        "difficulty": plan.difficulty.value,
        "subjects": [s.value for s in plan.subjects],
        "total_lessons": plan.total_lessons,
        "estimated_hours": plan.estimated_hours,
        "path": plan.path,
    }


@app.get("/curriculum/languages")
async def list_languages():
    """List all supported languages."""
    from clawpy.curriculum.regions import get_languages
    return {"languages": get_languages()}


@app.get("/curriculum/translate/stats")
async def translation_stats():
    """Show translation cache stats."""
    from clawpy.curriculum.translate import get_cache_stats
    return {"cache": get_cache_stats()}


@app.post("/curriculum/translate")
async def translate_content(req: Request):
    """Translate text or question to a target language. Results are cached."""
    from clawpy.curriculum.translate import translate_text, translate_question
    body = await req.json()
    target_lang = body.get("target_lang", "en")
    source_lang = body.get("source_lang", "bn")

    if "question" in body:
        result = await translate_question(body["question"], target_lang, source_lang)
        return {"translated": result}
    elif "text" in body:
        result = await translate_text(body["text"], target_lang, source_lang)
        return {"translated": result}
    return {"error": "Provide 'text' or 'question' in body"}


@app.get("/curriculum/lessons/{lesson_id}/content")
async def get_lesson_content_endpoint(lesson_id: str):
    """Get rich teaching content for a specific lesson."""
    from clawpy.curriculum.lesson_content import get_lesson_content
    content = get_lesson_content(lesson_id)
    if not content:
        return {"lesson_id": lesson_id, "has_content": False}
    return {"lesson_id": lesson_id, "has_content": True, **content}


@app.post("/admin/lessons/{lesson_id}")
async def save_lesson_content_endpoint(lesson_id: str, request: Request):
    """Save or update lesson content from the dashboard. Persists to disk."""
    from clawpy.curriculum.lesson_content import save_lesson_content
    body = await request.json()
    content = {
        "title": body.get("title", ""),
        "learning_objectives": body.get("learning_objectives", []),
        "teaching_steps": body.get("teaching_steps", []),
        "key_formulas": body.get("key_formulas", []),
        "common_mistakes": body.get("common_mistakes", []),
        "practice_prompts": body.get("practice_prompts", []),
        "real_world_example": body.get("real_world_example", ""),
    }
    save_lesson_content(lesson_id, content)
    return {"ok": True, "lesson_id": lesson_id}


@app.get("/curriculum/tracks")
async def list_tracks(region: str | None = None):
    """List admission tracks for a region. Defaults to Bangladesh."""
    from clawpy.curriculum.regions import get_region
    r = get_region(region)
    return {"region": r["id"], "tracks": r["tracks"]}


@app.get("/curriculum/regions")
async def list_regions():
    """List all supported regions/countries."""
    from clawpy.curriculum.regions import get_all_regions
    return {"regions": get_all_regions()}


@app.get("/curriculum/region/{region_id}")
async def get_region_detail(region_id: str):
    """Get full region config: tracks, universities, subjects."""
    from clawpy.curriculum.regions import get_region
    r = get_region(region_id)
    return r


@app.get("/curriculum/exams")
async def list_exams():
    """List available target exams and their subjects."""
    from clawpy.curriculum.syllabus import EXAM_SUBJECTS
    return {
        "exams": {
            exam.value: {
                "subjects": [s.value for s in subjects],
                "label": _exam_label(exam.value),
                "label_bn": _exam_label_bn(exam.value),
            }
            for exam, subjects in EXAM_SUBJECTS.items()
        }
    }


def _exam_label(exam: str) -> str:
    return {
        "du": "Dhaka University", "buet": "BUET (Engineering)",
        "medical": "Medical Admission", "ru": "Rajshahi University",
        "ju": "Jahangirnagar University", "cu": "Chittagong University",
        "gst": "GST (Combined)", "general": "General Preparation",
    }.get(exam, exam.upper())


def _exam_label_bn(exam: str) -> str:
    return {
        "du": "ঢাকা বিশ্ববিদ্যালয়", "buet": "বুয়েট (ইঞ্জিনিয়ারিং)",
        "medical": "মেডিকেল ভর্তি", "ru": "রাজশাহী বিশ্ববিদ্যালয়",
        "ju": "জাহাঙ্গীরনগর বিশ্ববিদ্যালয়", "cu": "চট্টগ্রাম বিশ্ববিদ্যালয়",
        "gst": "জিএসটি (সম্মিলিত)", "general": "সাধারণ প্রস্তুতি",
    }.get(exam, exam.upper())


# ── Practice Quiz API ─────────────────────────────────────────────────────

_PRACTICE_DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://shikkha:shikkha_secret@localhost:5432/shikkhadikkha",
)

# University slug → search patterns (same as QuestionLookupTool)
_PRACTICE_UNIVERSITY_MAP: dict[str, list[str]] = {
    "du": ["dhaka-university"],
    "buet": ["buet"],
    "medical": ["medical"],
    "ru": ["rajshahi-university"],
    "cu": ["chittagong-university"],
    "ju": ["jahangirnagar-university", "jagannath-university"],
    "kuet": ["kuet"],
    "ruet": ["ruet"],
    "cuet": ["cuet"],
}

_practice_db_conn = None

# Subject (English id OR the Bangla name the app sends) → list of DB tag
# fragments. The DB tags questions by chapter, so one subject maps to many
# chapter keywords that are OR-ed together. Keys are lowercased.
_PRACTICE_SUBJECT_MAP: dict[str, list[str]] = {
    # Physics
    "physics": ["পদার্থ", "গতি", "বল", "তাপ", "আলো", "তরঙ্গ", "তড়িৎ", "চুম্বক", "ভেক্টর", "মহাকর্ষ", "শক্তি", "সেমিকন্ডাক্টর"],
    "পদার্থবিজ্ঞান": ["পদার্থ", "গতি", "বল", "তাপ", "আলো", "তরঙ্গ", "তড়িৎ", "চুম্বক", "ভেক্টর", "মহাকর্ষ", "শক্তি", "সেমিকন্ডাক্টর"],
    # Chemistry
    "chemistry": ["রসায়ন", "জৈব", "অজৈব", "পরমাণু", "মোল", "বন্ধন", "বিক্রিয়া"],
    "রসায়ন": ["রসায়ন", "জৈব", "অজৈব", "পরমাণু", "মোল", "বন্ধন", "বিক্রিয়া"],
    # Biology
    "biology": ["জীব", "উদ্ভিদ", "প্রাণী", "কোষ", "জেনেটিক", "অণুজীব"],
    "জীববিজ্ঞান": ["জীব", "উদ্ভিদ", "প্রাণী", "কোষ", "জেনেটিক", "অণুজীব"],
    # Higher Math
    "higher_math": ["উচ্চতর গণিত", "ত্রিকোণমিতি", "ক্যালকুলাস", "যোগজীকরণ", "ম্যাট্রিক্স", "ফাংশন", "কনিক", "সমীকরণ"],
    "উচ্চতর গণিত": ["উচ্চতর গণিত", "ত্রিকোণমিতি", "ক্যালকুলাস", "যোগজীকরণ", "ম্যাট্রিক্স", "ফাংশন", "কনিক", "সমীকরণ"],
    # General Math
    "general_math": ["সাধারণ গণিত", "বীজগণিত", "জ্যামিতি", "পাটিগণিত"],
    "সাধারণ গণিত": ["সাধারণ গণিত", "বীজগণিত", "জ্যামিতি", "পাটিগণিত"],
    # Math (generic — covers both higher and general)
    "math": ["গণিত", "ত্রিকোণমিতি", "ক্যালকুলাস", "যোগজীকরণ", "ম্যাট্রিক্স", "ফাংশন", "কনিক", "সমীকরণ", "বীজগণিত", "জ্যামিতি", "পাটিগণিত"],
    "গণিত": ["গণিত", "ত্রিকোণমিতি", "ক্যালকুলাস", "যোগজীকরণ", "ম্যাট্রিক্স", "ফাংশন", "কনিক", "সমীকরণ", "বীজগণিত", "জ্যামিতি", "পাটিগণিত"],
    # English
    "english": ["English", "Grammar", "Vocabulary", "Sentence", "Preposition", "Verb"],
    "ইংরেজি": ["English", "Grammar", "Vocabulary", "Sentence", "Preposition", "Verb"],
}


# Markers that unambiguously belong to another subject. Needed because the keyword
# match is substring-based: "তড়িৎ" (electric) legitimately identifies physics, but is
# also inside "তড়িৎ রসায়ন" (electrochemistry), and "গণিত" appears inside chapter names
# across several papers. Without subtraction a physics quiz serves chemistry questions.
_PRACTICE_SUBJECT_EXCLUDE: dict[str, list[str]] = {
    "physics": ["রসায়ন", "জীববিজ্ঞান", "উদ্ভিদ", "English", "ব্যাকরণ"],
    "পদার্থবিজ্ঞান": ["রসায়ন", "জীববিজ্ঞান", "উদ্ভিদ", "English", "ব্যাকরণ"],
    "chemistry": ["জীববিজ্ঞান", "উদ্ভিদ", "English"],
    "রসায়ন": ["জীববিজ্ঞান", "উদ্ভিদ", "English"],
    "biology": ["English", "ব্যাকরণ"],
    "জীববিজ্ঞান": ["English", "ব্যাকরণ"],
}

def _normalize_bangla(text: str) -> str:
    """Precompose Bengali nukta sequences so decomposed app input matches
    the precomposed DB form. NFC excludes these compositions (RRA/RHA/YYA),
    so map them manually."""
    import unicodedata
    text = unicodedata.normalize("NFC", text)
    return (
        text.replace("\u09a1\u09bc", "\u09dc")
        .replace("\u09a2\u09bc", "\u09dd")
        .replace("\u09af\u09bc", "\u09df")
    )


def _get_db_conn():
    """Get or create a shared psycopg2 connection for practice endpoints."""
    global _practice_db_conn
    if _practice_db_conn is None or _practice_db_conn.closed:
        import psycopg2
        _practice_db_conn = psycopg2.connect(_PRACTICE_DATABASE_URL)
        _practice_db_conn.autocommit = True
    return _practice_db_conn


def _promote_translation(q: dict) -> dict:
    """Move translated text into the fields the client actually renders.

    `translate_question` writes to sidecar keys (`question_translated`,
    `text_translated`) and leaves the Bangla in `question`/`text`. Clients render the
    primary fields, so the sidecar approach silently shows Bangla to a student who
    picked another language -- the translation happens and is then thrown away.

    Promote instead, keeping the source under `*_source` so the tutor can still quote
    the original wording and so a bad translation stays debuggable.
    """
    translated = q.get("question_translated")
    if translated:
        q["question_source"] = q.get("question")
        q["question"] = translated
    q.pop("question_translated", None)

    for opt in q.get("options", []):
        opt_translated = opt.get("text_translated")
        if opt_translated:
            opt["text_source"] = opt.get("text")
            opt["text"] = opt_translated
        opt.pop("text_translated", None)

    return q


@app.get("/practice/questions")
async def practice_questions(
    subject: str | None = None,
    university: str | None = None,
    chapter: str | None = None,
    limit: int = 10,
    exclude: str | None = None,
    lang: str | None = None,
):
    """Serve real MCQ questions from PostgreSQL for the practice quiz screen."""
    try:
        conn = _get_db_conn()
    except Exception as e:
        logger.error("Practice DB connection failed: %s", e)
        return {"questions": [], "total": 0}

    limit = max(1, min(limit, 30))

    conditions: list[str] = []
    params: list = []

    if subject:
        s = _normalize_bangla(subject.strip())
        # Map the subject (English id or Bangla name) to its chapter keywords.
        # Normalize each so Bengali nukta forms match the precomposed DB values.
        patterns = _PRACTICE_SUBJECT_MAP.get(s.lower()) or _PRACTICE_SUBJECT_MAP.get(s)
        if patterns:
            normed = [_normalize_bangla(p) for p in patterns]
            or_clauses = " OR ".join(["subject ILIKE %s"] * len(normed))
            conditions.append(f"({or_clauses})")
            params.extend(f"%{p}%" for p in normed)

            # Keyword matching is substring-based, so chapter names bleed across
            # subjects: physics matches on "তড়িৎ" (electric), which is also a
            # substring of the chemistry chapter "তড়িৎ রসায়ন" (electrochemistry).
            # A physics quiz then serves chemistry questions. Subtract the markers
            # that unambiguously belong to another subject.
            excludes = [
                _normalize_bangla(x)
                for x in _PRACTICE_SUBJECT_EXCLUDE.get(s.lower(), [])
                or _PRACTICE_SUBJECT_EXCLUDE.get(s, [])
            ]
            for x in excludes:
                conditions.append("subject NOT ILIKE %s")
                params.append(f"%{x}%")
        else:
            conditions.append("subject ILIKE %s")
            params.append(f"%{s}%")

    if chapter:
        ch = _normalize_bangla(chapter.strip())
        # Split into keywords (drop short words like ও, ও, এবং) and OR-match
        # so "ভৌত জগৎ ও পরিমাপ" matches DB's "ভৌতজগত ও পরিমাপ"
        _BANGLA_STOP = {"ও", "এবং", "বা", "এর", "তার", "যে", "কি"}
        words = [w for w in ch.split() if len(w) > 1 and w not in _BANGLA_STOP]
        if words:
            or_clauses = " OR ".join(["subject ILIKE %s"] * len(words))
            conditions.append(f"({or_clauses})")
            params.extend(f"%{w}%" for w in words)
        else:
            conditions.append("subject ILIKE %s")
            params.append(f"%{ch}%")

    if university:
        uni = university.strip().lower()
        slugs = _PRACTICE_UNIVERSITY_MAP.get(uni, [uni])
        placeholders = ",".join(["%s"] * len(slugs))
        conditions.append(f"university IN ({placeholders})")
        params.extend(slugs)

    if exclude:
        exclude_ids = [eid.strip() for eid in exclude.split(",") if eid.strip()]
        if exclude_ids:
            placeholders = ",".join(["%s"] * len(exclude_ids))
            conditions.append(f"id NOT IN ({placeholders})")
            params.extend(exclude_ids)

    where = ""
    if conditions:
        where = "WHERE " + " AND ".join(conditions)

    query = f"""
        SELECT id, university, exam_name, exam_year, question_text,
               options, correct_answer, correct_index, subject
        FROM admission_question
        {where}
        ORDER BY RANDOM()
        LIMIT %s
    """
    params.append(limit)

    try:
        cur = conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()
        cur.close()
    except Exception as e:
        logger.error("Practice query failed: %s", e)
        # Reset connection on error so next call retries
        global _practice_db_conn
        _practice_db_conn = None
        return {"questions": [], "total": 0}

    questions = []
    for row in rows:
        options = []
        for i, opt in enumerate(row[5]):
            options.append({
                "id": chr(65 + i),
                "text": opt,
                "isCorrect": i == row[7],
            })
        correct_letter = chr(65 + row[7]) if isinstance(row[7], int) else row[6]
        questions.append({
            "id": str(row[0]),
            "question": row[4],
            "options": options,
            "subject": row[8],
            "university": row[1],
            "exam": row[2],
            "year": str(row[3]) if row[3] else "",
            "correct_answer": correct_letter,
        })

    # The bank is stored in Bangla. When the student has picked another language,
    # translate on demand so the whole app -- questions included -- is in one language.
    #
    # Translated results are cached to disk by source text, so a given question costs
    # one model call once per language, ever. Questions are translated concurrently
    # because doing 10 sequentially is the difference between a usable screen and a
    # visibly slow one.
    if lang and lang != "bn":
        import asyncio
        from clawpy.curriculum.translate import translate_question

        try:
            translated = await asyncio.gather(
                *(translate_question(q, lang, "bn") for q in questions)
            )
            questions = [_promote_translation(q) for q in translated]
        except Exception as e:
            # Serving the Bangla original beats serving nothing -- a student can still
            # read the maths, and the tutor explains in their language regardless.
            logger.warning("Question translation to %s failed: %s", lang, e)

    return {"questions": questions, "total": len(questions)}


@app.get("/practice/subjects")
async def practice_subjects():
    """Return distinct subjects with question counts from PostgreSQL."""
    try:
        conn = _get_db_conn()
    except Exception as e:
        logger.error("Practice DB connection failed: %s", e)
        return {"subjects": []}

    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT subject, COUNT(*) as count FROM admission_question "
            "GROUP BY subject ORDER BY count DESC"
        )
        rows = cur.fetchall()
        cur.close()
    except Exception as e:
        logger.error("Practice subjects query failed: %s", e)
        global _practice_db_conn
        _practice_db_conn = None
        return {"subjects": []}

    subjects = [{"name": row[0], "count": row[1]} for row in rows]
    return {"subjects": subjects}


# ---------------------------------------------------------------- phone handoff
#
# A desktop drawing surface shows a QR code; the phone opens it, draws or takes a
# photo, and posts the result here. The desktop polls and picks it up.
#
# Deliberately in-memory and short-lived: this is a pipe between two devices that
# are both online right now, not storage. A pairing code is one-shot -- read once
# and it is gone -- so a stale QR in a screenshot cannot replay someone's work.
_HANDOFF: dict[str, dict] = {}
_HANDOFF_TTL_S = 600
_HANDOFF_MAX_CHARS = 8_000_000  # ~6 MB of base64, generous for a phone photo
_SAFE_CODE = re.compile(r"[^A-Za-z0-9_-]")


def _handoff_gc() -> None:
    """Drop expired slots. Called on each touch -- no background task needed."""
    cutoff = datetime.now(timezone.utc).timestamp() - _HANDOFF_TTL_S
    for code in [c for c, v in _HANDOFF.items() if v["at"] < cutoff]:
        _HANDOFF.pop(code, None)


@app.post("/handoff/{code}")
async def handoff_put(code: str, req: HandoffRequest):
    """Phone -> desktop. Park an image against a pairing code."""
    _handoff_gc()
    key = _SAFE_CODE.sub("", code)[:64]
    if not key:
        raise HTTPException(400, "bad code")
    if not req.image:
        raise HTTPException(400, "empty image")
    if len(req.image) > _HANDOFF_MAX_CHARS:
        raise HTTPException(413, "image too large")
    if len(_HANDOFF) > 200:  # crude cap; the GC normally keeps this tiny
        _handoff_gc()
    _HANDOFF[key] = {
        "image": req.image,
        "kind": req.kind,
        "at": datetime.now(timezone.utc).timestamp(),
    }
    return {"ok": True}


@app.get("/handoff/{code}")
async def handoff_get(code: str):
    """Desktop <- phone. One-shot read: the slot is consumed."""
    _handoff_gc()
    key = _SAFE_CODE.sub("", code)[:64]
    slot = _HANDOFF.pop(key, None)
    if not slot:
        return {"image": None}
    return {"image": slot["image"], "kind": slot["kind"]}


# ------------------------------------------------------------- teacher tools
#
# These call Gemini's native REST API rather than the OpenAI-compatible shim,
# because native `inline_data` parts accept PDFs as well as images -- a
# teacher's "homework" is as often a scanned PDF as a photo.

_GEMINI_NATIVE = "https://generativelanguage.googleapis.com/v1beta/models"
_TEACHER_MODEL = os.environ.get("SENSEI_TEACHER_MODEL", "gemini-3.5-flash")


def _gemini_key() -> str:
    return os.environ.get("SENSEI_CLOUD_API_KEY", "") or os.environ.get("GEMINI_API_KEY", "")


async def _gemini_generate(parts: list[dict], *, max_tokens: int = 4000) -> str:
    """One native generateContent call. Returns the reply text or raises."""
    import httpx

    key = _gemini_key()
    if not key:
        raise HTTPException(503, "no Gemini API key configured")
    body = {
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {"maxOutputTokens": max_tokens, "temperature": 0.2},
    }
    async with httpx.AsyncClient(timeout=httpx.Timeout(300.0, connect=10.0)) as client:
        resp = await client.post(
            f"{_GEMINI_NATIVE}/{_TEACHER_MODEL}:generateContent",
            params={"key": key},
            json=body,
        )
    if resp.status_code >= 400:
        logger.warning("gemini native %s: %s", resp.status_code, resp.text[:300])
        raise HTTPException(502, f"Gemini call failed ({resp.status_code})")
    data = resp.json()
    try:
        return "".join(p.get("text", "") for p in data["candidates"][0]["content"]["parts"])
    except (KeyError, IndexError):
        raise HTTPException(502, "Gemini returned no content")


def _parse_json_block(text: str) -> dict:
    """Pull the first JSON object out of a reply, fences and chatter aside."""
    cleaned = text.strip()
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start < 0 or end <= start:
        raise HTTPException(502, "model reply had no JSON object")
    try:
        return json.loads(cleaned[start : end + 1])
    except json.JSONDecodeError:
        raise HTTPException(502, "model reply was not valid JSON")


def _split_data_uri(uri: str) -> tuple[str, str]:
    """data:mime;base64,payload -> (mime, payload). Bare base64 assumed PNG."""
    if uri.startswith("data:"):
        head, _, payload = uri.partition(",")
        return (head[5:].split(";")[0] or "image/png"), payload
    return "image/png", uri


class QuestionDraftRequest(BaseModel):
    """A teacher's rough problem, to be finalised into a structured question."""

    text: str | None = None
    image: str | None = None  # data URI of a photographed/scanned problem
    subject_hint: str | None = None
    language: str | None = None


_CUSTOM_QUESTIONS_PATH = os.path.join(
    os.environ.get("SENSEI_DATA_DIR", os.path.join(os.path.dirname(__file__), "..", "..", "data")),
    "custom_questions.json",
)

_DRAFT_PROMPT = """\
You are preparing a practice problem for a Socratic science/math tutor. A teacher has
supplied a rough problem below (as text and/or a photo). Finalise it into JSON with
EXACTLY these fields:

{
  "subject": "physics" | "chemistry" | "math" | "biology",
  "title": "short title, max 6 words",
  "level": "easy" | "medium" | "hard" | "advanced",
  "problem": "the cleaned-up problem statement, self-contained, with any values needed",
  "answer": "the final answer only",
  "solution_steps": ["step 1", "step 2"],
  "common_mistake": "the single most likely student error on this problem"
}

Fix ambiguity and units, keep the teacher's intent, invent no extra parts. Use $...$
LaTeX for maths. Reply with ONLY the JSON object."""


@app.post("/samples/draft")
async def samples_draft(req: QuestionDraftRequest):
    """Teacher's rough problem in, finalised structured question out (saved).

    Gemini cleans the statement, solves it and names the likely mistake, so a
    teacher can add a question in the time it takes to photograph one.
    """
    if not (req.text and req.text.strip()) and not req.image:
        raise HTTPException(400, "need text or an image")

    parts: list[dict] = [{"text": _DRAFT_PROMPT}]
    if req.subject_hint:
        parts.append({"text": f"Subject hint from the teacher: {req.subject_hint}"})
    if req.text and req.text.strip():
        parts.append({"text": f"Teacher's rough problem:\n{req.text.strip()}"})
    if req.image:
        mime, payload = _split_data_uri(req.image)
        parts.append({"inline_data": {"mime_type": mime, "data": payload}})

    q = _parse_json_block(await _gemini_generate(parts))

    # A malformed question would break the practice UI, so check before saving.
    for field in ("subject", "title", "problem", "answer"):
        if not isinstance(q.get(field), str) or not q[field].strip():
            raise HTTPException(502, f"finalised question missing '{field}'")

    q["id"] = f"custom-{uuid.uuid4().hex[:10]}"
    q["created_at"] = datetime.now(timezone.utc).isoformat()

    try:
        existing = []
        if os.path.exists(_CUSTOM_QUESTIONS_PATH):
            with open(_CUSTOM_QUESTIONS_PATH, encoding="utf-8") as f:
                existing = json.load(f)
        existing.append(q)
        os.makedirs(os.path.dirname(_CUSTOM_QUESTIONS_PATH), exist_ok=True)
        with open(_CUSTOM_QUESTIONS_PATH, "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.warning("custom question save failed: %s", e)
        raise HTTPException(500, "could not save the question")

    return {"question": q}


@app.get("/samples/custom")
async def samples_custom():
    """Teacher-added questions, merged into the practice examples by the client."""
    try:
        if os.path.exists(_CUSTOM_QUESTIONS_PATH):
            with open(_CUSTOM_QUESTIONS_PATH, encoding="utf-8") as f:
                return {"questions": json.load(f)}
    except Exception as e:
        logger.warning("custom question read failed: %s", e)
    return {"questions": []}


class GradeRequest(BaseModel):
    """Homework to grade: photos and/or PDFs, plus an optional rubric."""

    files: list[dict]  # [{"data": dataURI, "mime": "...", "name": "..."}]
    rubric: str | None = None
    language: str | None = None


_GRADE_PROMPT = """\
You are grading a student's submitted work (handwritten pages and/or a PDF report)
for their teacher. Read everything carefully. Reply with ONLY a JSON object:

{
  "summary": "2-3 sentences on the overall quality of the work",
  "score": <number 0-100>,
  "grade": "letter or band, e.g. A-",
  "questions": [
    {"label": "which question/section", "verdict": "correct" | "partial" | "wrong",
     "error": "the specific mistake, or null", "feedback": "one actionable sentence"}
  ],
  "strengths": ["..."],
  "next_steps": ["what to practise next"]
}

Grade the WORK SHOWN, not what you imagine. Follow the rubric exactly if one is given.
Be specific: name the line or step where each error happens. Do not inflate the score.
Write feedback the teacher can hand straight to the student."""


@app.post("/grade")
async def grade_work(req: GradeRequest):
    """Photos/PDF of student work in, a structured grading report out."""
    if not req.files:
        raise HTTPException(400, "no files")
    if len(req.files) > 12:
        raise HTTPException(400, "too many files (max 12)")

    parts: list[dict] = [{"text": _GRADE_PROMPT}]
    if req.rubric and req.rubric.strip():
        parts.append({"text": f"Teacher's rubric / instructions:\n{req.rubric.strip()}"})
    if req.language:
        parts.append({"text": f"Write summary and feedback in language code: {req.language}"})

    for f in req.files:
        raw = f.get("data", "")
        if not raw:
            continue
        mime, payload = _split_data_uri(raw)
        parts.append({"inline_data": {"mime_type": f.get("mime") or mime, "data": payload}})

    report = _parse_json_block(await _gemini_generate(parts, max_tokens=6000))
    return {"report": report, "model": _TEACHER_MODEL}


@app.post("/tutor/coach")
async def tutor_coach(req: CoachRequest):
    """Two stages: read the page, then decide what to ask about it.

    Stage 1 is a vision call at low temperature whose only job is to say what is
    on the paper and where the first error is. Stage 2 is TEXT ONLY -- it takes
    that reading and turns it into one Socratic nudge.

    Splitting them is what makes either job doable. A single prompt asking a
    model to both read handwriting and teach from it does neither well: it
    either transcribes and forgets to teach, or teaches and invents lines that
    are not on the page. It also means stage 2 can run on a different, faster
    model than stage 1, since it never needs to see the pixels.
    """
    image = req.image.strip()
    if not image:
        raise HTTPException(400, "empty image")
    if not image.startswith("data:"):
        image = f"data:image/png;base64,{image}"

    prompt = "Here is the student's work so far."
    if req.problem:
        prompt = f"The problem being solved:\n{req.problem}\n\n{prompt}"

    # ---- stage 1: what is actually on the page -------------------------------
    try:
        reading = await _chat(
            [
                {"role": "system", "content": _SEE_SYSTEM},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image}},
                    ],
                },
            ],
            model=req.reading_model,
            max_tokens=2500,
        )
    except HTTPException as e:
        logger.warning("coach stage 1 failed: %s", e.detail)
        return {"reading": None, "coach": None, "reason": "could not read the work"}

    if not reading:
        return {"reading": None, "coach": None, "reason": "nothing readable on the page"}

    # ---- stage 2: what to say about it ---------------------------------------
    lang = f"\nWrite hint and question in language code: {req.language}." if req.language else ""
    try:
        raw = await _chat(
            [
                {"role": "system", "content": _COACH_SYSTEM + lang},
                {
                    "role": "user",
                    "content": (
                        f"The problem:\n{req.problem or '(not given)'}\n\n"
                        f"A factual reading of the student's page:\n{reading}"
                    ),
                },
            ],
            model=req.coaching_model,
            max_tokens=1200,
            temperature=0.6,  # the teaching turn wants some warmth
        )
        coach = _parse_json_block(raw)
    except HTTPException as e:
        logger.warning("coach stage 2 failed: %s", e.detail)
        # The reading alone is still worth returning; the client can show it.
        return {"reading": reading, "coach": None, "reason": "could not form a question"}

    _, _, m1 = _endpoint_for(req.reading_model)
    _, _, m2 = _endpoint_for(req.coaching_model)
    return {"reading": reading, "coach": coach, "models": {"reading": m1, "coaching": m2}}


_OBSERVATIONS_DIR = os.path.join(
    os.environ.get("SENSEI_DATA_DIR", os.path.join(os.path.dirname(__file__), "..", "..", "data")),
    "observations",
)

# Session ids come from a client; they become a path segment, so keep them boring.
_SAFE_SESSION = re.compile(r"[^A-Za-z0-9_.-]")


@app.post("/observe/attempt")
async def observe_attempt(req: AttemptSummaryRequest):
    """Bank a one-row account of an attempt.

    The event log in /observe says what happened; this says what it meant --
    hesitation before the first mark, how much was undone, whether help was
    asked for, how it ended. Kept in its own file so the dataset can be read as
    a table of attempts without replaying every stroke.
    """
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    try:
        os.makedirs(_OBSERVATIONS_DIR, exist_ok=True)
        row = {
            "session": _SAFE_SESSION.sub("_", req.session)[:64] or "anon",
            "at": datetime.now(timezone.utc).isoformat(),
            **(({"learner": req.learner}) if req.learner else {}),
            **req.summary,
        }
        with open(os.path.join(_OBSERVATIONS_DIR, f"attempts-{day}.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    except Exception as e:
        logger.warning("attempt summary write failed: %s", e)
        return {"ok": False}
    return {"ok": True}


@app.post("/observe")
async def observe(req: ObserveRequest):
    """Append a batch of workspace events to this session's JSONL log.

    Append-only, one file per session per day. Two purposes: the tutor reads a
    digest of recent events to teach against what the student is actually doing,
    and the accumulated logs are the dataset -- timestamped mistakes and
    corrections across many learners and ability levels.
    """
    if not req.events:
        return {"ok": True, "written": 0}

    session = _SAFE_SESSION.sub("_", req.session)[:64] or "anon"
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    day_dir = os.path.join(_OBSERVATIONS_DIR, day)

    try:
        os.makedirs(day_dir, exist_ok=True)
        path = os.path.join(day_dir, f"{session}.jsonl")
        with open(path, "a", encoding="utf-8") as f:
            for ev in req.events:
                if req.learner and "learner" not in ev:
                    ev = {**ev, "learner": req.learner}
                f.write(json.dumps(ev, ensure_ascii=False) + "\n")
    except Exception as e:
        # Losing telemetry must never break the lesson the student is in.
        logger.warning("observe write failed: %s", e)
        return {"ok": False, "written": 0}

    return {"ok": True, "written": len(req.events)}


_COACH_SYSTEM = """\
You are Sensei, a Socratic tutor looking over a student's shoulder while they work.

You are given a factual reading of what is currently on their page. Turn it into ONE
short intervention. Reply with ONLY a JSON object:

{
  "status": "correct" | "error" | "incomplete" | "blank",
  "hint": "one sentence, under 20 words, shown in a speech bubble beside their work",
  "question": "the single Socratic question you would ask next",
  "focus": "the line or part of their work you want them to look at, or null"
}

Rules that matter more than anything else:
- NEVER state the correct answer, and never say what the corrected line should be.
  Point at where to look and ask what they think.
- If the work is correct, say so warmly and ask a question that extends it. Do not
  invent a fault in correct work.
- If the page is blank or barely started, ask what they think the first step is.
- The hint is glanceable. "You've got the radius right — look again at the centre."
  is the register. No preamble, no "It looks like".
- Speak to the student as "you", in their language."""


_SEE_SYSTEM = """\
You are looking at a photo or sketch of a student's own working on a problem.

Report, briefly and factually:
1. A transcription of what is written or drawn, line by line, in the order it appears.
2. The FIRST line that contains an error, and what the error is. If the work is
   correct, say so plainly -- inventing an error in correct work is the worst thing
   you can do here, because it teaches a student out of something they had right.

Do NOT address the student and do NOT teach. This is an internal note for a tutor
who will do the teaching. No greetings, no encouragement, under 150 words."""


def _endpoint_for(model: str | None) -> tuple[str, str, str]:
    """(base_url, api_key, model) for any model id, cloud or local.

    A Gemini id routes to Gemini whatever the tutor is pinned to, and anything
    else to the local router. That is what lets the two coaching stages run on
    different models: reading stays on the private local vision model while the
    teaching turn can go to a fast cloud one, or both stay local when the cable
    is out.
    """
    chosen = model or os.environ.get("CLAWPY_MODEL", "")
    if chosen.startswith("gemini"):
        return "https://generativelanguage.googleapis.com/v1beta/openai", _gemini_key(), chosen
    if os.environ.get("CLAWPY_PROVIDER") == "gemini" and not model:
        return "https://generativelanguage.googleapis.com/v1beta/openai", _gemini_key(), chosen
    return (
        os.environ.get("SENSEI_LOCAL_BASE_URL", os.environ.get("OPENAI_BASE_URL", "")).rstrip("/"),
        os.environ.get("SENSEI_LOCAL_API_KEY", os.environ.get("OPENAI_API_KEY", "")),
        chosen,
    )


async def _chat(
    messages: list[dict], *, model: str | None = None, max_tokens: int = 2000, temperature: float = 0.2
) -> str:
    """One OpenAI-compatible completion against whichever model is asked for."""
    import httpx

    base_url, api_key, chosen = _endpoint_for(model)
    if not base_url or not chosen:
        raise HTTPException(503, "no model configured")

    payload: dict[str, Any] = {
        "model": chosen,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    # Reasoning models (Nemotron Lightning, qwen3-vl-*-thinking) spend the budget
    # thinking and return content:null. The coaching stage has to emit strict
    # JSON, so thinking is turned off for local models rather than hoping the
    # JSON survives inside a chain of thought. Ignored by models without it.
    if not chosen.startswith("gemini"):
        payload["chat_template_kwargs"] = {"enable_thinking": False}
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    async with httpx.AsyncClient(timeout=httpx.Timeout(900.0, connect=10.0)) as client:
        resp = await client.post(f"{base_url}/chat/completions", json=payload, headers=headers)
    if resp.status_code >= 400:
        logger.warning("chat %s on %s: %s", resp.status_code, chosen, resp.text[:300])
        raise HTTPException(502, f"model call failed ({resp.status_code})")

    choice = (resp.json().get("choices") or [{}])[0]
    msg = choice.get("message", {}) or {}
    # Thinking models leave content empty when the budget runs out mid-thought.
    text = msg.get("content") or msg.get("reasoning") or ""
    return text.replace("<|begin_of_box|>", "").replace("<|end_of_box|>", "").strip()


def _vision_endpoint() -> tuple[str, str, str]:
    """(base_url, api_key, model) for a direct OpenAI-compatible vision call.

    The tutor engine is text-only, so an image cannot ride the normal turn. Rather
    than thread image blocks through the whole engine, this asks the SAME model the
    tutor is already pinned to -- so no cold swap -- and hands the resulting note
    back for the text turn to reason over.
    """
    model = os.environ.get("CLAWPY_MODEL", "")
    if os.environ.get("CLAWPY_PROVIDER") == "gemini":
        key = os.environ.get("GEMINI_API_KEY", "")
        return "https://generativelanguage.googleapis.com/v1beta/openai", key, model
    return (
        os.environ.get("OPENAI_BASE_URL", "").rstrip("/"),
        os.environ.get("OPENAI_API_KEY", ""),
        model,
    )


@app.post("/tutor/see")
async def tutor_see(req: SeeRequest):
    """Look at a piece of the student's work and return a note about it.

    The client inserts a sketch or photo into the conversation; this turns those
    pixels into something the text tutor can act on. Returns `{"note": ...}` — or
    `{"note": null, "reason": ...}` when the configured model cannot see, so the
    client can degrade to sending the message without pretending it was read.
    """
    import httpx

    base_url, api_key, model = _vision_endpoint()
    if not base_url or not model:
        return {"note": None, "reason": "no model configured"}

    image = req.image.strip()
    if not image:
        raise HTTPException(400, "empty image")
    if not image.startswith("data:"):
        image = f"data:image/png;base64,{image}"

    prompt = "Here is my working."
    if req.problem:
        prompt = f"The problem being solved:\n{req.problem}\n\nHere is the student's working."

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": _SEE_SYSTEM},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image}},
                ],
            },
        ],
        # Generous on purpose: a thinking model spends its budget reasoning
        # before it writes anything, and a tight cap returns finish_reason
        # "length" with content:null -- an empty answer that looks like failure.
        "max_tokens": 2500,
        "temperature": 0.2,  # transcription is not a place for creativity
    }

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    try:
        # Generous: a local cold swap is served on this same call.
        async with httpx.AsyncClient(timeout=httpx.Timeout(900.0, connect=10.0)) as client:
            resp = await client.post(
                f"{base_url}/chat/completions", json=payload, headers=headers
            )
        if resp.status_code >= 400:
            logger.warning("tutor/see upstream %s: %s", resp.status_code, resp.text[:300])
            return {"note": None, "reason": f"vision call failed ({resp.status_code})"}
        body = resp.json()
        choice = (body.get("choices") or [{}])[0]
        msg = choice.get("message", {}) or {}
        note = msg.get("content")
        if not note:
            # Thinking models put the chain of thought in `reasoning` and the
            # answer in `content`. If the budget ran out mid-thought there is no
            # content, but the reasoning still describes what it saw -- better
            # to hand that back than to report nothing.
            note = msg.get("reasoning") or ""
            if note:
                logger.info("tutor/see: using reasoning (finish=%s)", choice.get("finish_reason"))
    except Exception as e:  # network, timeout, malformed JSON
        logger.warning("tutor/see failed: %s", e)
        return {"note": None, "reason": "vision call failed"}

    if not note:
        return {"note": None, "reason": "model returned nothing"}
    # GLM-style models wrap the answer in box markers.
    note = note.replace("<|begin_of_box|>", "").replace("<|end_of_box|>", "").strip()
    return {"note": note, "model": model}


_CHAT_HTML = """<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>দীক্ষা — Dikkha AI Tutor</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',system-ui,-apple-system,sans-serif;background:#0f172a;color:#e2e8f0;height:100vh;display:flex;flex-direction:column}
.header{background:#1e293b;border-bottom:1px solid #334155;padding:16px 24px;display:flex;align-items:center;gap:12px}
.header .logo{width:40px;height:40px;background:linear-gradient(135deg,#f59e0b,#ea580c);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:20px}
.header h1{font-size:18px;font-weight:700;color:#f8fafc}
.header .sub{font-size:12px;color:#94a3b8;margin-top:2px}
.messages{flex:1;overflow-y:auto;padding:20px 24px;display:flex;flex-direction:column;gap:16px}
.msg{display:flex;gap:10px;max-width:85%}
.msg.user{align-self:flex-end;flex-direction:row-reverse}
.msg .avatar{width:32px;height:32px;border-radius:10px;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:14px}
.msg.ai .avatar{background:#1e293b;border:1px solid #334155}
.msg.user .avatar{background:#7c3aed}
.msg .bubble{padding:12px 16px;border-radius:18px;font-size:14px;line-height:1.6;white-space:pre-wrap;word-wrap:break-word}
.msg.ai .bubble{background:#1e293b;border:1px solid #334155;border-bottom-left-radius:4px;color:#e2e8f0}
.msg.user .bubble{background:#7c3aed;border-bottom-right-radius:4px;color:#fff}
.typing{display:flex;gap:5px;padding:12px 16px}
.typing span{width:8px;height:8px;background:#64748b;border-radius:50%;animation:bounce .6s infinite alternate}
.typing span:nth-child(2){animation-delay:.2s}
.typing span:nth-child(3){animation-delay:.4s}
@keyframes bounce{to{transform:translateY(-6px);opacity:.4}}
.input-area{background:#1e293b;border-top:1px solid #334155;padding:16px 24px;display:flex;gap:12px;align-items:flex-end}
.input-area textarea{flex:1;background:#0f172a;border:1px solid #334155;border-radius:16px;padding:12px 16px;color:#e2e8f0;font-size:14px;font-family:inherit;resize:none;min-height:48px;max-height:150px;outline:none;transition:border-color .2s}
.input-area textarea:focus{border-color:#7c3aed}
.input-area textarea::placeholder{color:#64748b}
.input-area button{width:44px;height:44px;background:#7c3aed;border:none;border-radius:12px;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:background .2s;flex-shrink:0}
.input-area button:hover{background:#6d28d9}
.input-area button:disabled{background:#334155;cursor:not-allowed}
.input-area button svg{width:20px;height:20px;fill:#fff}
.suggestions{display:flex;gap:8px;flex-wrap:wrap;padding:0 24px 12px}
.suggestions button{background:#1e293b;border:1px solid #334155;border-radius:20px;padding:8px 16px;color:#94a3b8;font-size:13px;cursor:pointer;transition:all .2s}
.suggestions button:hover{border-color:#7c3aed;color:#e2e8f0}
.tool-badge{display:inline-block;background:#7c3aed20;color:#a78bfa;font-size:11px;padding:2px 8px;border-radius:6px;margin-bottom:4px}
</style>
</head>
<body>
<div class="header">
  <div class="logo">🎓</div>
  <div><h1>দীক্ষা — Dikkha</h1><div class="sub">Socratic AI Tutor for Bangladesh</div></div>
</div>

<div class="messages" id="messages">
  <div class="msg ai">
    <div class="avatar">🎓</div>
    <div class="bubble">আস্সালামু আলাইকুম! আমি <b>দীক্ষা</b> — তোমার AI টিউটর।<br><br>আজ কোন বিষয় নিয়ে কাজ করবে? বলো, কোথা থেকে শুরু করি।</div>
  </div>
</div>

<div class="suggestions" id="suggestions">
  <button onclick="send('BUET এর Physics থেকে প্রশ্ন দাও')">⚛️ BUET Physics</button>
  <button onclick="send('Organic Chemistry practice করি')">⚗️ Organic Chemistry</button>
  <button onclick="send('Integration solve করতে help করো')">📐 Integration</button>
  <button onclick="send('সালোকসংশ্লেষণ বুঝিয়ে বলো')">🧬 সালোকসংশ্লেষণ</button>
  <button onclick="send('DU admission tips দাও')">🎯 DU Tips</button>
</div>

<div class="input-area">
  <textarea id="input" rows="1" placeholder="তোমার প্রশ্ন লেখো..." onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();sendFromInput()}"></textarea>
  <button onclick="sendFromInput()" id="sendBtn">
    <svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
  </button>
</div>

<script>
const messagesEl = document.getElementById('messages');
const inputEl = document.getElementById('input');
const sendBtn = document.getElementById('sendBtn');
const suggestionsEl = document.getElementById('suggestions');
let sending = false;
let sessionId = null;

function addMessage(role, html) {
  const div = document.createElement('div');
  div.className = 'msg ' + role;
  div.innerHTML = role === 'ai'
    ? '<div class="avatar">🎓</div><div class="bubble">' + html + '</div>'
    : '<div class="avatar">👤</div><div class="bubble">' + html + '</div>';
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return div;
}

function addTyping() {
  const div = document.createElement('div');
  div.className = 'msg ai';
  div.id = 'typing';
  div.innerHTML = '<div class="avatar">🎓</div><div class="typing"><span></span><span></span><span></span></div>';
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function removeTyping() {
  const el = document.getElementById('typing');
  if (el) el.remove();
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

async function send(text) {
  if (sending || !text.trim()) return;
  sending = true;
  sendBtn.disabled = true;
  inputEl.value = '';
  suggestionsEl.style.display = 'none';

  addMessage('user', escapeHtml(text));
  addTyping();

  let aiDiv = null;
  let collected = '';

  try {
    const response = await fetch('/tutor/stream', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text, session_id: sessionId, context_type: 'free_chat' }),
    });

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    let eventType = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        const trimmed = line.trim();
        if (trimmed.startsWith('event: ')) {
          eventType = trimmed.slice(7);
          continue;
        }
        if (!trimmed.startsWith('data: ')) continue;
        const jsonStr = trimmed.slice(6);
        if (!jsonStr) continue;

        try {
          const data = JSON.parse(jsonStr);

          if (eventType === 'progress' && data.session_id) {
            sessionId = data.session_id;
          } else if (eventType === 'token' && data.text) {
            if (!aiDiv) {
              removeTyping();
              aiDiv = addMessage('ai', '');
            }
            collected += data.text;
            aiDiv.querySelector('.bubble').innerHTML = collected
              .replace(/\\*\\*(.+?)\\*\\*/g, '<b>$1</b>')
              .replace(/\\n/g, '<br>');
            messagesEl.scrollTop = messagesEl.scrollHeight;
          } else if (eventType === 'tool_use' && data.name) {
            if (!aiDiv) {
              removeTyping();
              aiDiv = addMessage('ai', '');
            }
            collected += '<span class="tool-badge">🔧 ' + escapeHtml(data.name) + '</span>\\n';
            aiDiv.querySelector('.bubble').innerHTML = collected.replace(/\\n/g, '<br>');
          } else if (eventType === 'suggestions' && data.suggestions) {
            showSuggestions(data.suggestions);
          }
        } catch {}
      }
    }
  } catch (err) {
    removeTyping();
    addMessage('ai', '❌ Error: ' + escapeHtml(err.message));
  }

  if (!aiDiv) removeTyping();
  sending = false;
  sendBtn.disabled = false;
  inputEl.focus();
}

function showSuggestions(items) {
  suggestionsEl.innerHTML = '';
  items.forEach(text => {
    const btn = document.createElement('button');
    btn.textContent = text;
    btn.onclick = () => send(text);
    suggestionsEl.appendChild(btn);
  });
  suggestionsEl.style.display = 'flex';
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function sendFromInput() {
  send(inputEl.value);
}

inputEl.addEventListener('input', function() {
  this.style.height = 'auto';
  this.style.height = Math.min(this.scrollHeight, 150) + 'px';
});
</script>
</body>
</html>"""


def main():
    """Run the server with uvicorn."""
    import uvicorn

    port = int(os.environ.get("CLAWPY_SERVER_PORT", "4039"))
    host = os.environ.get("CLAWPY_SERVER_HOST", "0.0.0.0")
    logger.info("Starting DikkhaClaw tutor on %s:%d", host, port)
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
