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
import uuid
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
    from fastapi import FastAPI, Request
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


@app.get("/curriculum/subjects")
async def list_subjects():
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
    return {"subjects": results}


@app.get("/curriculum/subjects/{subject_id}")
async def get_subject(subject_id: str):
    """Get full curriculum tree for a subject — units and lessons."""
    from clawpy.curriculum.planner import get_subject_overview
    from clawpy.curriculum.models import SubjectId

    try:
        sid = SubjectId(subject_id)
    except ValueError:
        return {"error": f"Unknown subject: {subject_id}"}
    return get_subject_overview(sid)


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


@app.get("/practice/questions")
async def practice_questions(
    subject: str | None = None,
    university: str | None = None,
    chapter: str | None = None,
    limit: int = 10,
    exclude: str | None = None,
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
