"""ClawPy interactive REPL.

Own visual identity — amber/orange theme, claw branding, unique layout.
"""

from __future__ import annotations

import asyncio
import time
import uuid
from typing import Any

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion, merge_completers
from prompt_toolkit.history import InMemoryHistory
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from clawpy.engine.engine import Engine
from clawpy.engine.token_budget import get_context_window
from clawpy.provider.base import EventType, StreamEvent, Usage

# ---- Branding ----

_BRAND = "ClawPy"
_VERSION = "0.1.0"
_ACCENT = "dark_orange3"  # Our signature color (amber/orange)
_DIM = "dim"
_CLAW = "🐾"

# ---- Model catalog ----

_MODEL_CATALOG: list[dict[str, str]] = [
    # Anthropic
    {"alias": "opus", "id": "claude-opus-4-6", "label": "Opus 4.6", "tier": "anthropic", "note": "Deep reasoning, complex tasks"},
    {"alias": "opus[1m]", "id": "claude-opus-4-6[1m]", "label": "Opus 4.6 (1M)", "tier": "anthropic", "note": "Extended context window"},
    {"alias": "sonnet", "id": "claude-sonnet-4-6", "label": "Sonnet 4.6", "tier": "anthropic", "note": "Balanced speed and quality"},
    {"alias": "sonnet[1m]", "id": "claude-sonnet-4-6[1m]", "label": "Sonnet 4.6 (1M)", "tier": "anthropic", "note": "Extended context window"},
    {"alias": "haiku", "id": "claude-haiku-4-5-20251001", "label": "Haiku 4.5", "tier": "anthropic", "note": "Fast, lightweight"},
    # OpenAI
    {"alias": "gpt-4o", "id": "gpt-4o", "label": "GPT-4o", "tier": "openai", "note": "OpenAI flagship"},
    {"alias": "gpt-4o-mini", "id": "gpt-4o-mini", "label": "GPT-4o Mini", "tier": "openai", "note": "Fast and affordable"},
    # Google
    {"alias": "gemini-2.5-pro", "id": "gemini-2.5-pro", "label": "Gemini 2.5 Pro", "tier": "gemini", "note": "1M context, multimodal"},
    {"alias": "gemini-2.5-flash", "id": "gemini-2.5-flash", "label": "Gemini 2.5 Flash", "tier": "gemini", "note": "Speed optimized"},
    # DeepSeek
    {"alias": "deepseek-chat", "id": "deepseek-chat", "label": "DeepSeek V3", "tier": "deepseek", "note": "Open-weight flagship"},
    {"alias": "deepseek-reasoner", "id": "deepseek-reasoner", "label": "DeepSeek R1", "tier": "deepseek", "note": "Chain-of-thought reasoning"},
]

_TIER_COLORS = {
    "anthropic": "medium_purple3",
    "openai": "green3",
    "gemini": "dodger_blue1",
    "deepseek": "cyan3",
    "ollama": "bright_white",
}


def _resolve_model(name: str) -> str:
    lower = name.lower().strip()
    for m in _MODEL_CATALOG:
        if lower in (m["alias"].lower(), m["id"].lower(), m["label"].lower()):
            return m["id"]
    return name


def _get_model_info(model_id: str) -> dict[str, str] | None:
    for m in _MODEL_CATALOG:
        if model_id == m["id"] or model_id == m["alias"]:
            return m
    return None


def _format_ctx(tokens: int) -> str:
    if tokens >= 1_000_000:
        return f"{tokens // 1_000_000}M"
    return f"{tokens // 1000}K"


class _SlashCompleter(Completer):
    """Autocomplete / commands."""

    _COMMANDS = [
        "/model", "/tasks", "/bg", "/fg", "/kill", "/usage", "/status",
        "/context", "/memory", "/dream", "/plan", "/clear", "/compact",
        "/plugin", "/resume", "/agents", "/mcp", "/login", "/logout",
        "/help", "/quit",
    ]

    def get_completions(self, document: Any, complete_event: Any) -> Any:
        text = document.text_before_cursor
        if not text.startswith("/"):
            return
        for cmd in self._COMMANDS:
            if cmd.startswith(text):
                yield Completion(cmd, start_position=-len(text))


class _FileCompleter(Completer):
    """Autocomplete @file mentions."""

    def get_completions(self, document: Any, complete_event: Any) -> Any:
        text = document.text_before_cursor
        # Find the last @ mention
        at_pos = text.rfind("@")
        if at_pos < 0:
            return
        partial = text[at_pos + 1:]
        if " " in partial and not partial.endswith("/"):
            return
        from pathlib import Path
        try:
            if "/" in partial:
                parent = Path(partial).parent
                stem = Path(partial).name
                for p in sorted(parent.iterdir()):
                    if p.name.startswith(stem) or not stem:
                        rel = str(p.relative_to(".")) if not str(p).startswith("/") else str(p)
                        display = rel + ("/" if p.is_dir() else "")
                        yield Completion(display, start_position=-len(partial))
            else:
                for p in sorted(Path(".").iterdir()):
                    if p.name.startswith(partial):
                        display = p.name + ("/" if p.is_dir() else "")
                        yield Completion(display, start_position=-len(partial))
        except OSError:
            return


class REPL:
    """ClawPy interactive REPL."""

    def __init__(self, engine: Engine, console: Console | None = None) -> None:
        self.engine = engine
        self.console = console or Console()
        completer = merge_completers([_SlashCompleter(), _FileCompleter()])
        self.session: PromptSession[str] = PromptSession(
            history=InMemoryHistory(),
            completer=completer,
        )
        self._session_id = uuid.uuid4().hex[:12]
        self._start_time = time.time()
        self._total_input_tokens = 0
        self._total_output_tokens = 0
        self._turn_count = 0
        self._slash_awaitable: Any = None

        # Wire engine callbacks
        self.engine.on_agent_event = self._on_agent_event
        self.engine._ask_user = self._ask_permission

        # Initialize session persistence
        from clawpy.session.session import SessionMeta, SessionStore
        store = SessionStore()
        store.save_meta(self.engine.config.model, self.engine.config.work_dir)
        self.engine.session_store = store
        SessionStore.save_to_history(SessionMeta(
            session_id=store.session_id,
            created_at=self._start_time,
            model=self.engine.config.model,
            work_dir=self.engine.config.work_dir,
        ))

    async def _wait_with_keys(self, engine_task: asyncio.Task[Any], task: Any) -> bool:
        """Wait for engine_task to finish. Returns False (no backgrounding mid-turn).

        Use /bg <id> after Ctrl+C to background, /tasks to view log.
        Raw stdin key capture conflicts with prompt_toolkit, so we keep it simple.
        """
        try:
            await engine_task
        except asyncio.CancelledError:
            raise KeyboardInterrupt
        return False

    async def _ask_permission(self, question: str) -> str:
        """Interactive permission prompt using prompt_toolkit."""
        self.console.print(f"  [yellow]{question}[/yellow]", end="")
        return await self.session.prompt_async("")

    def _on_agent_event(self, task_id: str, message: str) -> None:
        """Called when an agent (background or foregrounded) has an update."""
        reg = self.engine.task_registry
        task = reg.get(task_id)
        is_fg = task and not task.is_background and reg.foreground_id == task_id

        if is_fg:
            # Foregrounded task — show without [bg] prefix
            self.console.print(f"  [{_ACCENT}][{task_id}][/{_ACCENT}] {message}")
        else:
            self.console.print(f"  [{_DIM}][bg {task_id}][/{_DIM}] [{_ACCENT}]{message}[/{_ACCENT}]")

        # Terminal bell on completion/failure
        if "completed" in message or "failed" in message:
            print("\a", end="", flush=True)

    async def run(self) -> None:
        cfg = self.engine.config
        info = _get_model_info(cfg.model)
        model_label = info["label"] if info else cfg.model

        # Banner
        self.console.print()
        self.console.print(f"  [{_ACCENT} bold]{_CLAW} {_BRAND}[/{_ACCENT} bold]  [dim]v{_VERSION}[/dim]")
        self.console.print(f"  [{_DIM}]{cfg.work_dir}[/{_DIM}]")
        self.console.print(f"  [{_DIM}]model: {model_label} via {cfg.provider}[/{_DIM}]")
        self.console.print()

        while True:
            try:
                user_input = await self.session.prompt_async(f"🐾 ")
            except (EOFError, KeyboardInterrupt):
                self.console.print(f"\n[{_ACCENT}]See you later![/{_ACCENT}]")
                break

            user_input = user_input.strip()
            if not user_input:
                continue

            if user_input.startswith("/"):
                if self._handle_slash(user_input):
                    break
                # Run any async slash command
                if self._slash_awaitable is not None:
                    await self._slash_awaitable
                    self._slash_awaitable = None
                continue

            await self._run_turn(user_input)

    async def _run_turn(self, user_input: str) -> None:
        """Run a turn as a detachable task.

        Ctrl+B (double press): background the running turn
        Ctrl+O: show activity log of running turn
        """
        turn_start = time.time()
        text_buf_ref: list[str] = [""]  # Use list for closure mutability

        # Create a task entry for this turn
        from clawpy.engine.tasks import TaskStatus
        reg = self.engine.task_registry
        task = reg.create(user_input[:50], background=False)
        task.status = TaskStatus.RUNNING

        def on_stream(event: StreamEvent) -> None:
            elapsed = time.time() - turn_start
            match event.type:
                case EventType.DELTA:
                    if event.delta and event.delta.text:
                        text_buf_ref[0] += event.delta.text
                        if not task.is_background:
                            print(event.delta.text, end="", flush=True)
                case EventType.TOOL_START:
                    if event.tool_call:
                        log_entry = f">> {event.tool_call.name} ({elapsed:.0f}s)"
                        task.log.append(log_entry)
                        if not task.is_background:
                            if text_buf_ref[0] and not text_buf_ref[0].endswith("\n"):
                                print()
                            self.console.print(
                                f"  [{_ACCENT}]{log_entry}[/{_ACCENT}]"
                            )
                        elif self.engine.on_agent_event:
                            self.engine.on_agent_event(task.task_id, log_entry)
                case EventType.TOOL_END:
                    pass
                case EventType.ERROR:
                    if event.error:
                        task.log.append(f"ERROR: {event.error}")
                        if not task.is_background:
                            self.console.print(f"[red]Error: {event.error}[/red]")

        # Run the turn as an asyncio.Task so it can be backgrounded
        async def _engine_turn() -> Any:
            return await self.engine.run_turn(user_input, on_stream=on_stream)

        engine_task = asyncio.create_task(_engine_turn())
        task._asyncio_task = engine_task

        # Listen for Ctrl+B / Ctrl+O while turn runs
        backgrounded = False
        try:
            backgrounded = await self._wait_with_keys(engine_task, task)
        except KeyboardInterrupt:
            engine_task.cancel()
            self.console.print(f"\n  [{_ACCENT}]Interrupted[/{_ACCENT}]")
            reg.kill(task.task_id)
            return

        if backgrounded:
            # Turn was sent to background — add completion callback
            def _on_bg_done(fut: asyncio.Task[Any]) -> None:
                try:
                    result = fut.result()
                    task.output = text_buf_ref[0]
                    task.input_tokens = result.usage.input_tokens
                    task.output_tokens = result.usage.output_tokens
                    reg.complete(task.task_id, output=task.output)
                    tokens = result.usage.input_tokens + result.usage.output_tokens
                    self.console.print(
                        f"\n  [{_DIM}][bg {task.task_id}][/{_DIM}] "
                        f"[{_ACCENT}]completed ({task.elapsed:.0f}s, {tokens:,} tokens)[/{_ACCENT}]"
                    )
                    print("\a", end="", flush=True)
                except asyncio.CancelledError:
                    reg.kill(task.task_id)
                except Exception as e:
                    reg.fail(task.task_id, str(e))

            engine_task.add_done_callback(_on_bg_done)
            self.console.print(
                f"\n  [{_ACCENT}]Backgrounded [{task.task_id}][/{_ACCENT}] "
                f"[{_DIM}]use /tasks or /fg {task.task_id}[/{_DIM}]"
            )
            return

        # Turn completed in foreground
        try:
            result = engine_task.result()
        except asyncio.CancelledError:
            self.console.print(f"\n  [{_ACCENT}]Cancelled[/{_ACCENT}]")
            reg.kill(task.task_id)
            return
        except Exception as e:
            self.console.print(f"\n[red]Error: {e}[/red]")
            reg.fail(task.task_id, str(e))
            return

        if text_buf_ref[0] and not text_buf_ref[0].endswith("\n"):
            print()

        task.output = text_buf_ref[0]
        task.input_tokens = result.usage.input_tokens
        task.output_tokens = result.usage.output_tokens
        reg.complete(task.task_id, output=task.output)

        turn_elapsed = time.time() - turn_start
        self._total_input_tokens += result.usage.input_tokens
        self._total_output_tokens += result.usage.output_tokens
        self._turn_count += 1

        if result.usage.input_tokens > 0 or result.usage.output_tokens > 0:
            from clawpy.engine.cost import estimate_cost, format_cost
            turn_cost = estimate_cost(
                self.engine.config.model,
                result.usage.input_tokens,
                result.usage.output_tokens,
            )
            self.console.print(
                f"  [{_DIM}]{turn_elapsed:.1f}s  "
                f"{result.usage.input_tokens}in {result.usage.output_tokens}out  "
                f"{format_cost(turn_cost)}[/{_DIM}]"
            )
        print()

        if result.error:
            self.console.print(f"[yellow]  {result.error}[/yellow]")

        # Check auto-dream after turn
        await self._maybe_auto_dream()

    def _handle_slash(self, raw: str) -> bool:
        parts = raw.split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        match cmd:
            case "/quit" | "/exit" | "/q":
                self.console.print(f"[{_ACCENT}]See you later![/{_ACCENT}]")
                return True
            case "/clear":
                self.engine.clear()
                self._total_input_tokens = 0
                self._total_output_tokens = 0
                self._turn_count = 0
                self.console.print(f"[{_ACCENT}]Conversation cleared.[/{_ACCENT}]")
            case "/model":
                self._cmd_model(args)
            case "/context":
                self._cmd_context()
            case "/status":
                self._cmd_status()
            case "/usage":
                self._slash_awaitable = self._cmd_usage()
            case "/memory" | "/mem":
                self._cmd_memory(args)
            case "/dream":
                self._slash_awaitable = self._cmd_dream()
            case "/compact":
                self.console.print(f"[{_DIM}]Manual compact not yet implemented.[/{_DIM}]")
            case "/tasks" | "/task":
                self._cmd_tasks(args)
            case "/bg":
                self._cmd_bg(args)
            case "/fg":
                self._cmd_fg(args)
            case "/kill":
                self._cmd_kill(args)
            case "/resume":
                self._cmd_resume()
            case "/plan":
                self._cmd_plan()
            case "/plugin" | "/plugins":
                self._cmd_plugin(args)
            case "/login":
                self._cmd_login()
            case "/logout":
                from clawpy.auth.oauth import clear_tokens
                clear_tokens()
                self.console.print(f"[{_ACCENT}]Logged out.[/{_ACCENT}]")
            case "/agents":
                self._cmd_agents()
            case "/mcp":
                self._cmd_mcp()
            case "/help":
                self._cmd_help()
            case _:
                self.console.print(f"[{_DIM}]Unknown command: {cmd}. Try /help[/{_DIM}]")
        return False

    # ---- /model ----

    def _cmd_model(self, args: str) -> None:
        if args:
            resolved = _resolve_model(args)
            self.engine.config.model = resolved
            info = _get_model_info(resolved)
            label = info["label"] if info else resolved
            note = f"  [{_DIM}]{info['note']}[/{_DIM}]" if info else ""
            self.console.print(f"  [{_ACCENT}]model[/{_ACCENT}] {label}{note}")
            return

        # Show model picker grouped by provider
        self.console.print()
        self.console.print(
            Panel(
                self._render_model_list(),
                title=f"[{_ACCENT} bold]Models[/{_ACCENT} bold]",
                subtitle=f"[{_DIM}]/model <alias> to switch[/{_DIM}]",
                border_style=_ACCENT,
                padding=(1, 2),
            )
        )

    def _render_model_list(self) -> str:
        current = self.engine.config.model
        lines: list[str] = []

        # Group by tier
        tiers: dict[str, list[dict[str, str]]] = {}
        for m in _MODEL_CATALOG:
            tiers.setdefault(m["tier"], []).append(m)

        tier_names = {"anthropic": "Anthropic", "openai": "OpenAI", "gemini": "Google Gemini", "deepseek": "DeepSeek"}

        for tier, models in tiers.items():
            color = _TIER_COLORS.get(tier, "white")
            lines.append(f"[{color} bold]{tier_names.get(tier, tier)}[/{color} bold]")
            for m in models:
                is_current = m["id"] == current or m["alias"] == current
                marker = f"[{_ACCENT}]>[/{_ACCENT}]" if is_current else " "
                ctx = _format_ctx(get_context_window(m["id"]))
                bold = " bold" if is_current else ""
                lines.append(
                    f"  {marker} [{color}{bold}]{m['label']:<24}[/{color}{bold}] "
                    f"[{_DIM}]{m['note']:<30} {ctx}[/{_DIM}]"
                )
            lines.append("")

        # Aliases
        aliases = ", ".join(f"{m['alias']}" for m in _MODEL_CATALOG)
        lines.append(f"[{_DIM}]aliases: {aliases}[/{_DIM}]")

        return "\n".join(lines)

    # ---- /status ----

    def _cmd_status(self) -> None:
        # Gather info
        cfg = self.engine.config
        info = _get_model_info(cfg.model)
        model_label = info["label"] if info else cfg.model
        model_note = info["note"] if info else ""

        auth_line = "API Key"
        email_line = ""
        try:
            from clawpy.auth.oauth import load_tokens
            tokens = load_tokens()
            if tokens and tokens.access_token:
                auth_line = "Claude Subscription"
                email_line = tokens.email or tokens.account_uuid or ""
                if tokens.is_expired:
                    auth_line += " [red](expired)[/red]"
        except Exception:
            pass
        if not email_line and cfg.api_key:
            auth_line = f"{cfg.provider.title()} API Key"

        elapsed = time.time() - self._start_time
        total_tok = self._total_input_tokens + self._total_output_tokens

        rows = [
            ("session", self._session_id),
            ("uptime", f"{int(elapsed) // 60}m {int(elapsed) % 60}s"),
            ("", ""),
            ("auth", auth_line),
        ]
        if email_line:
            rows.append(("account", email_line))
        rows += [
            ("", ""),
            ("model", f"{model_label}  [{_DIM}]{model_note}[/{_DIM}]"),
            ("provider", cfg.provider),
            ("permissions", cfg.permission_mode),
            ("tools", f"{len(self.engine.tools)} loaded"),
            ("", ""),
            ("turns", str(self._turn_count)),
            ("tokens", f"{total_tok:,} total  [{_DIM}]{self._total_input_tokens:,}in {self._total_output_tokens:,}out[/{_DIM}]"),
        ]
        from clawpy.engine.cost import estimate_cost, format_cost
        session_cost = estimate_cost(cfg.model, self._total_input_tokens, self._total_output_tokens)
        rows += [
            ("est. cost", format_cost(session_cost)),
        ]

        table = Table(show_header=False, box=None, padding=(0, 1), expand=False)
        table.add_column(style=_ACCENT, width=14, justify="right")
        table.add_column()
        for key, val in rows:
            table.add_row(key, val)

        self.console.print()
        self.console.print(Panel(table, title=f"[{_ACCENT} bold]{_CLAW} {_BRAND}[/{_ACCENT} bold]", border_style=_ACCENT, padding=(1, 2)))

    # ---- /context ----

    def _cmd_context(self) -> None:
        model = self.engine.config.model
        ctx_window = get_context_window(model)
        msg_count = len(self.engine.messages)
        info = _get_model_info(model)
        model_label = info["label"] if info else model

        # Estimate tokens
        sys_tokens = len(self.engine.system_prompt) // 4
        msg_tokens = sum(
            sum(
                len(b.text) + len(b.thinking)
                + (50 if b.tool_call else 0)
                + len(b.tool_result.content if b.tool_result else "")
                for b in m.content
            )
            for m in self.engine.messages
        ) // 4
        tool_tokens = len(self.engine.tools) * 100
        total = sys_tokens + msg_tokens + tool_tokens

        pct = min(100.0, (total / ctx_window) * 100) if ctx_window > 0 else 0.0

        # Build bar with our accent color
        bar_w = 40
        filled = int(bar_w * pct / 100)
        if pct < 50:
            fill_color = "green"
        elif pct < 80:
            fill_color = _ACCENT
        else:
            fill_color = "red"
        bar = f"[{fill_color}]{'━' * filled}[/{fill_color}][{_DIM}]{'╌' * (bar_w - filled)}[/{_DIM}]"

        lines: list[str] = []
        lines.append(f"{bar}  {pct:.0f}%")
        lines.append(f"[{_DIM}]{model_label} — ~{total:,} / {ctx_window:,} tokens ({_format_ctx(ctx_window)} window)[/{_DIM}]")
        lines.append("")
        lines.append(f"  [{_ACCENT}]system[/{_ACCENT}]    ~{sys_tokens:,} tokens")
        lines.append(f"  [{_ACCENT}]tools[/{_ACCENT}]     ~{tool_tokens:,} tokens  [{_DIM}]({len(self.engine.tools)} schemas)[/{_DIM}]")
        lines.append(f"  [{_ACCENT}]messages[/{_ACCENT}]  ~{msg_tokens:,} tokens  [{_DIM}]({msg_count} messages)[/{_DIM}]")

        self.console.print()
        self.console.print(Panel(
            "\n".join(lines),
            title=f"[{_ACCENT} bold]Context[/{_ACCENT} bold]",
            border_style=_ACCENT,
            padding=(1, 2),
        ))

    # ---- /usage ----

    async def _cmd_usage(self) -> None:
        from clawpy.auth.usage import fetch_usage

        self.console.print(f"  [{_DIM}]Fetching usage...[/{_DIM}]")
        info = await fetch_usage()

        if info.error:
            self.console.print(f"  [red]{info.error}[/red]")
            return

        if not info.windows:
            self.console.print(f"  [{_DIM}]No usage data available.[/{_DIM}]")
            return

        lines: list[str] = []
        for w in info.windows:
            pct = w.utilization
            bar_w = 30
            filled = int(bar_w * min(pct, 100) / 100)
            if pct < 50:
                color = "green"
            elif pct < 80:
                color = _ACCENT
            else:
                color = "red"
            bar = f"[{color}]{'━' * filled}[/{color}][{_DIM}]{'╌' * (bar_w - filled)}[/{_DIM}]"
            reset_text = f"resets in {w.resets_in}" if w.resets_at else ""
            lines.append(f"  [{_ACCENT}]{w.label:<22}[/{_ACCENT}] {bar} {pct:.0f}%  [{_DIM}]{reset_text}[/{_DIM}]")

        if info.extra and info.extra.enabled:
            lines.append("")
            ex = info.extra
            if ex.monthly_limit is not None and ex.used_credits is not None:
                lines.append(
                    f"  [{_ACCENT}]{'Extra usage':<22}[/{_ACCENT}] "
                    f"${ex.used_credits:.2f} / ${ex.monthly_limit:.2f}"
                )
            elif ex.utilization is not None:
                lines.append(f"  [{_ACCENT}]{'Extra usage':<22}[/{_ACCENT}] {ex.utilization:.0f}% used")

        self.console.print()
        self.console.print(Panel(
            "\n".join(lines),
            title=f"[{_ACCENT} bold]Usage[/{_ACCENT} bold]",
            border_style=_ACCENT,
            padding=(1, 2),
        ))

    # ---- /tasks /bg /fg /kill ----

    def _cmd_tasks(self, args: str) -> None:
        """List tasks or show output of a specific task."""
        reg = self.engine.task_registry
        tasks = reg.list_all()

        if args.strip():
            # Show specific task output
            task = reg.get(args.strip())
            if not task:
                self.console.print(f"  [{_DIM}]Task not found: {args.strip()}[/{_DIM}]")
                return
            self.console.print()
            status_color = {
                "running": _ACCENT,
                "completed": "green",
                "failed": "red",
                "killed": "red",
                "pending": _DIM,
            }.get(task.status.value, _DIM)
            self.console.print(
                f"  [{_ACCENT} bold][{task.task_id}][/{_ACCENT} bold] "
                f"{task.description}  [{status_color}]{task.status.value}[/{status_color}]"
            )
            self.console.print(
                f"  [{_DIM}]{task.elapsed:.0f}s | "
                f"{task.input_tokens + task.output_tokens:,} tokens | "
                f"{task.tool_calls} tools[/{_DIM}]"
            )

            # Show live activity log
            if task.log:
                self.console.print(f"\n  [{_ACCENT}]Activity log:[/{_ACCENT}]")
                # Show last 20 log entries
                for entry in task.log[-20:]:
                    self.console.print(f"  [{_DIM}]{entry}[/{_DIM}]")
                if len(task.log) > 20:
                    self.console.print(f"  [{_DIM}]... ({len(task.log)} total entries)[/{_DIM}]")

            # Show final output for completed tasks
            if task.output and task.is_done:
                self.console.print(f"\n  [{_ACCENT}]Output:[/{_ACCENT}]")
                for line in task.output[:2000].splitlines():
                    self.console.print(f"  {line}")
            if task.error:
                self.console.print(f"  [red]Error: {task.error}[/red]")
            self.console.print()
            return

        if not tasks:
            self.console.print(f"  [{_DIM}]No tasks. Agents will appear here when spawned.[/{_DIM}]")
            return

        self.console.print()
        for t in tasks:
            status_color = {
                "running": _ACCENT,
                "completed": "green",
                "failed": "red",
                "killed": "red",
                "pending": _DIM,
            }.get(t.status.value, _DIM)
            bg = " [bg]" if t.is_background else ""
            self.console.print(
                f"  [{_ACCENT}][{t.task_id}][/{_ACCENT}] "
                f"{t.description:<40} "
                f"[{status_color}]{t.status.value}{bg}[/{status_color}]  "
                f"[{_DIM}]{t.elapsed:.0f}s[/{_DIM}]"
            )
        self.console.print(
            f"\n  [{_DIM}]/tasks <id> to view output | /kill <id> to stop | /fg <id> to foreground[/{_DIM}]"
        )
        self.console.print()

    def _cmd_bg(self, args: str) -> None:
        """Background a task or list background tasks."""
        reg = self.engine.task_registry
        if args.strip():
            reg.background(args.strip())
            self.console.print(f"  [{_ACCENT}]Backgrounded [{args.strip()}][/{_ACCENT}]")
        else:
            bg = reg.list_background()
            if not bg:
                self.console.print(f"  [{_DIM}]No background tasks running.[/{_DIM}]")
            else:
                for t in bg:
                    self.console.print(
                        f"  [{_ACCENT}][{t.task_id}][/{_ACCENT}] {t.description}  "
                        f"[{_DIM}]{t.elapsed:.0f}s[/{_DIM}]"
                    )

    def _cmd_fg(self, args: str) -> None:
        """Bring a background task to foreground — shows live log."""
        if not args.strip():
            self.console.print(f"  [{_DIM}]Usage: /fg <task_id>[/{_DIM}]")
            return
        reg = self.engine.task_registry
        task = reg.get(args.strip())
        if not task:
            self.console.print(f"  [{_DIM}]Task not found: {args.strip()}[/{_DIM}]")
            return

        self.console.print(
            f"  [{_ACCENT} bold][{task.task_id}][/{_ACCENT} bold] "
            f"{task.description}  [{_DIM}]{task.elapsed:.0f}s[/{_DIM}]"
        )

        if task.is_done:
            # Show log + final output
            if task.log:
                self.console.print(f"\n  [{_ACCENT}]Activity log:[/{_ACCENT}]")
                for entry in task.log:
                    self.console.print(f"  [{_DIM}]{entry}[/{_DIM}]")
            if task.output:
                self.console.print(f"\n  [{_ACCENT}]Output:[/{_ACCENT}]")
                for line in task.output[:3000].splitlines():
                    self.console.print(f"  {line}")
            if task.error:
                self.console.print(f"  [red]Error: {task.error}[/red]")
        else:
            # Running: bring to foreground, show log so far
            reg.foreground(args.strip())
            self.console.print(f"  [{_ACCENT}]Foregrounded — live updates below[/{_ACCENT}]")
            if task.log:
                for entry in task.log:
                    self.console.print(f"  [{_DIM}]{entry}[/{_DIM}]")
            self.console.print(f"  [{_DIM}]New events will appear as they happen...[/{_DIM}]")

    def _cmd_kill(self, args: str) -> None:
        """Kill a running task."""
        if not args.strip():
            self.console.print(f"  [{_DIM}]Usage: /kill <task_id>[/{_DIM}]")
            return
        reg = self.engine.task_registry
        if reg.kill(args.strip()):
            self.console.print(f"  [{_ACCENT}]Killed [{args.strip()}][/{_ACCENT}]")
        else:
            self.console.print(f"  [{_DIM}]Task not found or already done: {args.strip()}[/{_DIM}]")

    # ---- /resume ----

    def _cmd_resume(self) -> None:
        """Resume a previous session."""
        from clawpy.session.session import SessionStore

        sessions = SessionStore.list_sessions()
        if not sessions:
            self.console.print(f"  [{_DIM}]No previous sessions found.[/{_DIM}]")
            return

        # Show recent sessions (last 10)
        self.console.print()
        recent = sessions[-10:]
        for i, s in enumerate(reversed(recent), 1):
            import datetime
            dt = datetime.datetime.fromtimestamp(s.created_at).strftime("%Y-%m-%d %H:%M")
            title = s.title or s.session_id[:8]
            self.console.print(
                f"  [{_ACCENT}]{i}.[/{_ACCENT}] {title:<30} [{_DIM}]{dt}  {s.model}[/{_DIM}]"
            )

        self.console.print(f"\n  [{_DIM}]Enter number to resume, or Esc to cancel:[/{_DIM}]")

        try:
            choice = input("  > ").strip()
        except (EOFError, KeyboardInterrupt):
            return

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(recent):
                selected = list(reversed(recent))[idx]
            else:
                self.console.print(f"  [{_DIM}]Invalid selection.[/{_DIM}]")
                return
        except ValueError:
            return

        # Load the session
        store = SessionStore(selected.session_id)
        messages = store.load_session()
        if not messages:
            self.console.print(f"  [{_DIM}]Session is empty.[/{_DIM}]")
            return

        self.engine.messages = messages
        self.engine.session_store = store
        self.console.print(
            f"  [{_ACCENT}]Resumed session {selected.session_id[:8]}[/{_ACCENT}] "
            f"[{_DIM}]({len(messages)} messages)[/{_DIM}]"
        )

    # ---- /dream ----

    async def _cmd_dream(self) -> None:
        from clawpy.engine.dream import dream_and_save

        self.console.print(f"  [{_DIM}]Dreaming... consolidating memories from this session[/{_DIM}]")

        result = await dream_and_save(
            provider=self.engine.provider,
            model=self.engine.config.model,
            work_dir=self.engine.config.work_dir,
            messages=self.engine.messages,
        )

        if result.success:
            self.engine.reload_system_prompt()
            self.console.print(
                f"  [{_ACCENT}]Dream complete[/{_ACCENT}] "
                f"[{_DIM}]{result.tokens_used:,} tokens used, memory updated[/{_DIM}]"
            )
        else:
            self.console.print(f"  [red]Dream failed: {result.error}[/red]")

    async def _maybe_auto_dream(self) -> None:
        """Check and run auto-dream after a turn if conditions met."""
        from clawpy.engine.dream import dream_and_save, should_auto_dream

        work_dir = self.engine.config.work_dir
        if not should_auto_dream(work_dir, self._turn_count):
            return

        self.console.print(f"\n  [{_DIM}]Auto-dreaming... consolidating session memories[/{_DIM}]")
        result = await dream_and_save(
            provider=self.engine.provider,
            model=self.engine.config.model,
            work_dir=work_dir,
            messages=self.engine.messages,
        )
        if result.success:
            self.engine.reload_system_prompt()
            self.console.print(
                f"  [{_ACCENT}]Auto-dream complete[/{_ACCENT}] [{_DIM}]memory updated[/{_DIM}]"
            )

    # ---- /memory ----

    def _cmd_memory(self, args: str) -> None:
        from clawpy.engine.memory import (
            MemoryFile,
            MemoryType,
            append_to_memory,
            discover_all_memory,
            edit_in_editor,
            get_project_memory_path,
        )

        parts = args.split(maxsplit=1)
        subcmd = parts[0].lower() if parts else ""
        subargs = parts[1].strip() if len(parts) > 1 else ""

        work_dir = self.engine.config.work_dir

        if not subcmd or subcmd == "list":
            # Show all memory files
            files = discover_all_memory(work_dir)
            lines: list[str] = []

            for mf in files:
                try:
                    display = str(mf.path.relative_to(work_dir))
                except ValueError:
                    display = str(mf.path)

                if mf.exists:
                    status = f"[green]{mf.line_count} lines[/green]"
                    preview = mf.preview.replace("\n", " ")[:60]
                    if preview:
                        preview = f"  [{_DIM}]{preview}...[/{_DIM}]"
                else:
                    status = f"[{_DIM}]not created[/{_DIM}]"
                    preview = ""

                type_color = {
                    MemoryType.GLOBAL: "magenta",
                    MemoryType.PROJECT: _ACCENT,
                    MemoryType.PROJECT_LOCAL: "cyan",
                    MemoryType.PARENT: _DIM,
                }.get(mf.memory_type, _DIM)

                lines.append(
                    f"  [{type_color}]{mf.label:<16}[/{type_color}] "
                    f"{display:<40} {status}{preview}"
                )

            self.console.print()
            self.console.print(Panel(
                "\n".join(lines) if lines else "No memory files found.",
                title=f"[{_ACCENT} bold]Memory Files[/{_ACCENT} bold]",
                subtitle=f"[{_DIM}]/memory add <text> | /memory edit | /memory reload[/{_DIM}]",
                border_style=_ACCENT,
                padding=(1, 2),
            ))

        elif subcmd == "add":
            if not subargs:
                self.console.print(f"  [{_DIM}]Usage: /memory add <text to remember>[/{_DIM}]")
                return
            path = get_project_memory_path(work_dir)
            append_to_memory(path, subargs)
            self.console.print(f"  [{_ACCENT}]Added to {path.name}[/{_ACCENT}]")
            # Auto-reload
            self.engine.reload_system_prompt()
            self.console.print(f"  [{_DIM}]System prompt reloaded[/{_DIM}]")

        elif subcmd == "edit":
            if subargs:
                # Edit specific file
                from pathlib import Path
                target = Path(subargs)
                if not target.is_absolute():
                    target = Path(work_dir) / target
            else:
                # Default: project memory
                target = get_project_memory_path(work_dir)

            self.console.print(f"  [{_DIM}]Opening {target} in editor...[/{_DIM}]")
            if edit_in_editor(target):
                self.engine.reload_system_prompt()
                self.console.print(f"  [{_ACCENT}]System prompt reloaded[/{_ACCENT}]")
            else:
                self.console.print(f"  [red]Editor not found. Set $EDITOR env var.[/red]")

        elif subcmd == "show":
            files = discover_all_memory(work_dir)
            active = [f for f in files if f.exists and f.content.strip()]
            if not active:
                self.console.print(f"  [{_DIM}]No memory files with content.[/{_DIM}]")
                return
            for mf in active:
                try:
                    display = str(mf.path.relative_to(work_dir))
                except ValueError:
                    display = str(mf.path)
                self.console.print(f"\n  [{_ACCENT} bold]{mf.label}: {display}[/{_ACCENT} bold]")
                # Print content with indentation
                for line in mf.content.strip().splitlines():
                    self.console.print(f"  {line}")

        elif subcmd == "reload":
            self.engine.reload_system_prompt()
            files = discover_all_memory(work_dir)
            active = sum(1 for f in files if f.exists)
            self.console.print(f"  [{_ACCENT}]Reloaded[/{_ACCENT}] {active} memory file(s)")

        else:
            self.console.print(f"  [{_DIM}]Memory commands:[/{_DIM}]")
            self.console.print(f"  [{_ACCENT}]/memory[/{_ACCENT}]              List all memory files")
            self.console.print(f"  [{_ACCENT}]/memory add <text>[/{_ACCENT}]  Add a note to project memory")
            self.console.print(f"  [{_ACCENT}]/memory edit[/{_ACCENT}]         Open in $EDITOR")
            self.console.print(f"  [{_ACCENT}]/memory show[/{_ACCENT}]         Print all memory content")
            self.console.print(f"  [{_ACCENT}]/memory reload[/{_ACCENT}]       Reload into system prompt")

    # ---- /plugin ----

    def _cmd_plugin(self, args: str) -> None:
        from clawpy.plugins.manager import PluginManager

        pm = PluginManager()
        parts = args.split(maxsplit=1)
        subcmd = parts[0].lower() if parts else ""
        subargs = parts[1].strip() if len(parts) > 1 else ""

        if not subcmd or subcmd == "list":
            installed = pm.list_installed()
            if not installed:
                self.console.print(f"  [{_DIM}]No plugins installed.[/{_DIM}]")
                self.console.print(f"  [{_DIM}]Install with: /plugin install owner/repo[/{_DIM}]")
                return
            self.console.print()
            for entry in installed:
                status = f"[green]enabled[/green]" if entry.enabled else f"[red]disabled[/red]"
                ver = f" v{entry.version}" if entry.version else ""
                self.console.print(
                    f"  [{_ACCENT}]{entry.name}[/{_ACCENT}]{ver}  {status}  [{_DIM}]{entry.source}[/{_DIM}]"
                )
            self.console.print()

        elif subcmd == "install":
            if not subargs:
                self.console.print(f"  [{_DIM}]Usage: /plugin install owner/repo  or  /plugin install /local/path[/{_DIM}]")
                return
            try:
                if subargs.startswith("/") or subargs.startswith("./") or subargs.startswith("~"):
                    plugin = pm.install_from_local(subargs)
                    self.console.print(f"  [{_ACCENT}]Installed {plugin.name}[/{_ACCENT}] from local path")
                else:
                    self.console.print(f"  [{_DIM}]Cloning {subargs}...[/{_DIM}]")
                    plugin = pm.install_from_github(subargs)
                    self.console.print(f"  [{_ACCENT}]Installed {plugin.name}[/{_ACCENT}] v{plugin.manifest.version}")

                # Show what was loaded
                if plugin.commands:
                    cmds = ", ".join(c.name for c in plugin.commands)
                    self.console.print(f"  [{_DIM}]Commands: {cmds}[/{_DIM}]")
                if plugin.agents:
                    agents = ", ".join(a.name for a in plugin.agents)
                    self.console.print(f"  [{_DIM}]Agents: {agents}[/{_DIM}]")
                if plugin.skills:
                    self.console.print(f"  [{_DIM}]Skills: {len(plugin.skills)}[/{_DIM}]")
                if plugin.errors:
                    for err in plugin.errors:
                        self.console.print(f"  [yellow]{err}[/yellow]")
            except Exception as e:
                self.console.print(f"  [red]Install failed: {e}[/red]")

        elif subcmd == "remove" or subcmd == "uninstall":
            if not subargs:
                self.console.print(f"  [{_DIM}]Usage: /plugin remove <name>[/{_DIM}]")
                return
            if pm.remove(subargs):
                self.console.print(f"  [{_ACCENT}]Removed {subargs}[/{_ACCENT}]")
            else:
                self.console.print(f"  [{_DIM}]Plugin not found: {subargs}[/{_DIM}]")

        elif subcmd == "enable":
            if pm.enable(subargs):
                self.console.print(f"  [{_ACCENT}]Enabled {subargs}[/{_ACCENT}]")
            else:
                self.console.print(f"  [{_DIM}]Plugin not found: {subargs}[/{_DIM}]")

        elif subcmd == "disable":
            if pm.disable(subargs):
                self.console.print(f"  [{_ACCENT}]Disabled {subargs}[/{_ACCENT}]")
            else:
                self.console.print(f"  [{_DIM}]Plugin not found: {subargs}[/{_DIM}]")

        elif subcmd == "info":
            plugin = pm.get_loaded(subargs)
            if not plugin:
                # Try loading all first
                pm.load_all()
                plugin = pm.get_loaded(subargs)
            if not plugin:
                self.console.print(f"  [{_DIM}]Plugin not found: {subargs}[/{_DIM}]")
                return
            m = plugin.manifest
            lines = [
                f"[{_ACCENT} bold]{m.name}[/{_ACCENT} bold]  v{m.version}",
                f"{m.description}" if m.description else "",
                f"[{_DIM}]Author: {m.author}[/{_DIM}]" if m.author else "",
                f"[{_DIM}]Source: {plugin.source}[/{_DIM}]",
                f"[{_DIM}]Path: {plugin.install_path}[/{_DIM}]",
            ]
            if plugin.commands:
                lines.append(f"\nCommands: {', '.join(c.name for c in plugin.commands)}")
            if plugin.agents:
                lines.append(f"Agents: {', '.join(a.name for a in plugin.agents)}")
            if plugin.skills:
                lines.append(f"Skills: {len(plugin.skills)}")
            if plugin.errors:
                lines.append(f"\n[yellow]Errors:[/yellow]")
                for err in plugin.errors:
                    lines.append(f"  [yellow]{err}[/yellow]")
            self.console.print()
            self.console.print(Panel(
                "\n".join(l for l in lines if l),
                border_style=_ACCENT,
                padding=(1, 2),
            ))

        else:
            self.console.print(f"  [{_DIM}]Plugin commands:[/{_DIM}]")
            self.console.print(f"  [{_ACCENT}]/plugin list[/{_ACCENT}]              List installed plugins")
            self.console.print(f"  [{_ACCENT}]/plugin install <repo>[/{_ACCENT}]    Install from GitHub (owner/repo)")
            self.console.print(f"  [{_ACCENT}]/plugin install <path>[/{_ACCENT}]    Install from local directory")
            self.console.print(f"  [{_ACCENT}]/plugin remove <name>[/{_ACCENT}]     Remove a plugin")
            self.console.print(f"  [{_ACCENT}]/plugin enable <name>[/{_ACCENT}]     Enable a plugin")
            self.console.print(f"  [{_ACCENT}]/plugin disable <name>[/{_ACCENT}]    Disable a plugin")
            self.console.print(f"  [{_ACCENT}]/plugin info <name>[/{_ACCENT}]       Show plugin details")

    # ---- /plan ----

    def _cmd_plan(self) -> None:
        from clawpy.tool.permission import PermissionMode
        current = self.engine.enforcer.mode
        if current == PermissionMode.PLAN:
            self.engine.enforcer.mode = PermissionMode.DEFAULT
            self.console.print(f"  [{_ACCENT}]Plan mode off[/{_ACCENT}] — tools unrestricted")
        else:
            self.engine.enforcer.mode = PermissionMode.PLAN
            self.console.print(f"  [{_ACCENT}]Plan mode on[/{_ACCENT}] — read-only, no edits")

    # ---- /login ----

    def _cmd_login(self) -> None:
        import asyncio
        from clawpy.auth.oauth import OAuthFlow
        try:
            flow = OAuthFlow()
            tokens = asyncio.get_event_loop().run_until_complete(flow.login(manual=True))
            email = tokens.email or tokens.account_uuid or "unknown"
            self.console.print(f"  [{_ACCENT}]Logged in as {email}[/{_ACCENT}]")
        except Exception as e:
            self.console.print(f"[red]Login failed: {e}[/red]")

    # ---- /agents ----

    def _cmd_agents(self) -> None:
        """List custom agent definitions."""
        from clawpy.agents.loader import discover_agents

        agents = discover_agents(self.engine.config.work_dir)
        if not agents:
            self.console.print(f"  [{_DIM}]No custom agents found.[/{_DIM}]")
            self.console.print(
                f"  [{_DIM}]Create .clawpy/agents/<name>.md with YAML frontmatter + system prompt.[/{_DIM}]"
            )
            return

        self.console.print()
        for a in agents:
            tools_str = f"  [{_DIM}]tools: {', '.join(a.tools)}[/{_DIM}]" if a.tools else ""
            model_str = f"  [{_DIM}]model: {a.model}[/{_DIM}]" if a.model else ""
            self.console.print(
                f"  [{_ACCENT}]{a.name:<20}[/{_ACCENT}] {a.description}{tools_str}{model_str}"
            )
        self.console.print()

    # ---- /mcp ----

    def _cmd_mcp(self) -> None:
        """Show MCP server configuration."""
        from clawpy.mcp.client import load_mcp_configs

        configs = load_mcp_configs(self.engine.config.work_dir)
        if not configs:
            self.console.print(f"  [{_DIM}]No MCP servers configured.[/{_DIM}]")
            self.console.print(
                f"  [{_DIM}]Create .clawpy/mcp.json or .mcp.json with server configs.[/{_DIM}]"
            )
            return

        self.console.print()
        for cfg in configs:
            cmd = " ".join(cfg.command + cfg.args)
            self.console.print(f"  [{_ACCENT}]{cfg.name:<20}[/{_ACCENT}] [{_DIM}]{cmd}[/{_DIM}]")
        self.console.print()

    # ---- /help ----

    def _cmd_help(self) -> None:
        commands = [
            ("/model [name]", "Pick a model or list all available"),
            ("/tasks [id]", "List running agents or view output"),
            ("/bg [id]", "Background a task / list bg tasks"),
            ("/fg <id>", "Foreground a background task"),
            ("/kill <id>", "Kill a running agent"),
            ("/usage", "Claude subscription usage & rate limits"),
            ("/status", "Session info, auth, usage stats"),
            ("/context", "Context window usage breakdown"),
            ("/memory [cmd]", "View, edit, add project memory"),
            ("/dream", "Consolidate session memories (LLM-powered)"),
            ("/plan", "Toggle read-only plan mode"),
            ("/clear", "Reset conversation"),
            ("/compact", "Compress conversation history"),
            ("/resume", "Resume a previous session"),
            ("/plugin [cmd]", "Install, list, remove plugins"),
            ("/agents", "List custom agent definitions"),
            ("/mcp", "Show MCP server configuration"),
            ("/login", "Authenticate with Claude subscription"),
            ("/logout", "Clear stored credentials"),
            ("/help", "This help"),
            ("/quit", "Exit"),
        ]
        self.console.print()
        for cmd, desc in commands:
            self.console.print(f"  [{_ACCENT}]{cmd:<18}[/{_ACCENT}] {desc}")
        self.console.print()
