"""CLI entry point — argparse-based with run (non-interactive) and repl (default) modes."""

from __future__ import annotations

import argparse
import asyncio
import sys

from clawpy.config.config import Config
from clawpy.engine.engine import Engine
from clawpy.provider.base import EventType, StreamEvent
from clawpy.tool.permission import PermissionEnforcer, PermissionMode
from clawpy.tool.registry import ToolRegistry


def _build_tools(engine: Engine | None = None) -> ToolRegistry:
    """Register all tools, passing file_state to tools that need it."""
    from clawpy.engine.file_state import FileStateTracker
    from clawpy.tool.bash import BashTool
    from clawpy.tool.file_edit import FileEditTool
    from clawpy.tool.file_read import FileReadTool
    from clawpy.tool.file_write import FileWriteTool
    from clawpy.tool.glob_tool import GlobTool
    from clawpy.tool.grep_tool import GrepTool
    from clawpy.tool.list_files import ListFilesTool
    from clawpy.tool.web_fetch import WebFetchTool

    fs = engine.file_state if engine else FileStateTracker()

    registry = ToolRegistry()
    registry.register(BashTool())
    registry.register(FileReadTool(file_state=fs))
    registry.register(FileWriteTool(file_state=fs))
    registry.register(FileEditTool(file_state=fs))
    registry.register(GrepTool())
    registry.register(GlobTool())
    registry.register(ListFilesTool())
    registry.register(WebFetchTool())
    return registry


def _create_provider(config: Config):  # type: ignore[no-untyped-def]
    """Create the appropriate provider based on config."""
    # Import all providers to trigger registration
    import clawpy.provider.anthropic  # noqa: F401
    import clawpy.provider.openai  # noqa: F401
    import clawpy.provider.gemini  # noqa: F401
    import clawpy.provider.ollama  # noqa: F401
    import clawpy.provider.deepseek  # noqa: F401

    from clawpy.provider.registry import create

    provider_cfg = config.provider_config()
    return create(config.provider, provider_cfg)


def _build_engine(config: Config) -> Engine:
    """Build the full engine with provider, tools, and permission enforcer."""
    provider = _create_provider(config)
    enforcer = PermissionEnforcer(
        mode=PermissionMode(config.permission_mode),
        work_dir=config.work_dir,
        allow_rules=config.allow_tools,
        deny_rules=config.deny_tools,
    )
    # Create engine first so tools can reference its file_state
    engine = Engine(
        provider=provider,
        tools=ToolRegistry(),  # Temporary, replaced below
        enforcer=enforcer,
        config=config,
    )
    engine.tools = _build_tools(engine)

    # Set a basic system prompt
    engine.set_system_prompt(_build_system_prompt(config))
    return engine


def _build_system_prompt(config: Config) -> str:
    """Build the full system prompt with memory and environment info."""
    from clawpy.engine.system_prompt import build_system_prompt

    return build_system_prompt(config.work_dir, config.model)


async def do_login(args: argparse.Namespace) -> None:
    """Login with Claude subscription via OAuth."""
    from clawpy.auth.oauth import OAuthFlow, is_logged_in, load_tokens

    if is_logged_in():
        tokens = load_tokens()
        if tokens and tokens.email:
            print(f"Already logged in as {tokens.email}")
            resp = input("Re-authenticate? (y/n): ").strip().lower()
            if resp != "y":
                return

    flow = OAuthFlow()
    try:
        tokens = await flow.login(manual=args.manual)
        email = tokens.email or tokens.account_uuid or "unknown"
        print(f"\nLogged in as: {email}")
        print("You can now use ClawPy with your Claude subscription.")
        print("Run 'clawpy' to start.")
    except RuntimeError as e:
        print(f"Login failed: {e}", file=sys.stderr)
        sys.exit(1)


def do_logout() -> None:
    """Remove stored OAuth credentials."""
    from clawpy.auth.oauth import clear_tokens, is_logged_in

    if not is_logged_in():
        print("Not logged in.")
        return
    clear_tokens()
    print("Logged out. Stored credentials removed.")


def do_status() -> None:
    """Show authentication status."""
    from clawpy.auth.oauth import load_tokens

    tokens = load_tokens()
    if tokens is None:
        print("Not logged in.")
        print("Run 'clawpy login' to authenticate with your Claude subscription.")
        print("Or set ANTHROPIC_API_KEY for API key auth.")
        return

    import time
    email = tokens.email or tokens.account_uuid or "unknown"
    expired = tokens.is_expired
    remaining = max(0, int(tokens.expires_at - time.time()))
    mins = remaining // 60

    print(f"Logged in as: {email}")
    print(f"Token: {'EXPIRED' if expired else f'valid ({mins}m remaining)'}")
    print(f"Scopes: {', '.join(tokens.scopes)}")
    if tokens.organization_uuid:
        print(f"Organization: {tokens.organization_uuid}")


async def run_once(args: argparse.Namespace) -> None:
    """Non-interactive mode: run a single prompt and exit."""
    config = Config.load(args.dir)
    if args.provider:
        config.provider = args.provider
    if args.model:
        config.model = args.model
    if args.permission_mode:
        config.permission_mode = args.permission_mode

    # Get prompt from argument or stdin
    prompt = args.prompt
    if not prompt:
        if not sys.stdin.isatty():
            prompt = sys.stdin.read().strip()
        if not prompt:
            print("Error: No prompt provided. Use: clawpy run 'your prompt'", file=sys.stderr)
            sys.exit(1)

    engine = _build_engine(config)

    import time as _time
    start = _time.time()

    # Stream callback for terminal output
    text_buf = ""

    def on_stream(event: StreamEvent) -> None:
        nonlocal text_buf
        if event.type == EventType.DELTA and event.delta:
            chunk = event.delta.text
            if chunk:
                print(chunk, end="", flush=True)
                text_buf += chunk

    result = await engine.run_turn(prompt, on_stream=on_stream)

    elapsed = _time.time() - start

    # Ensure we end with a newline
    if text_buf and not text_buf.endswith("\n"):
        print()

    # Show timing
    if result.usage.input_tokens > 0:
        from clawpy.engine.cost import estimate_cost, format_cost
        cost = estimate_cost(config.model, result.usage.input_tokens, result.usage.output_tokens)
        print(f"\n  {elapsed:.1f}s  {result.usage.input_tokens}in {result.usage.output_tokens}out  {format_cost(cost)}", file=sys.stderr)

    if result.error:
        print(f"\nError: {result.error}", file=sys.stderr)
        sys.exit(1)


async def run_repl(args: argparse.Namespace) -> None:
    """Interactive REPL mode using prompt_toolkit + rich."""
    from clawpy.ui.repl import REPL

    config = Config.load(args.dir)
    if args.provider:
        config.provider = args.provider
    if args.model:
        config.model = args.model
    if args.permission_mode:
        config.permission_mode = args.permission_mode

    engine = _build_engine(config)

    # Handle --resume
    if args.resume:
        from clawpy.session.session import SessionStore
        if args.resume == "__latest__":
            sessions = SessionStore.list_sessions()
            if sessions:
                latest = sessions[-1]
                store = SessionStore(latest.session_id)
                messages = store.load_session()
                if messages:
                    engine.messages = messages
                    engine.session_store = store
                    print(f"Resumed session {latest.session_id[:8]} ({len(messages)} messages)")
                else:
                    print("Last session was empty, starting fresh.")
            else:
                print("No previous sessions found, starting fresh.")
        else:
            store = SessionStore(args.resume)
            messages = store.load_session()
            if messages:
                engine.messages = messages
                engine.session_store = store
                print(f"Resumed session {args.resume[:8]} ({len(messages)} messages)")
            else:
                print(f"Session {args.resume} not found or empty, starting fresh.")

    repl = REPL(engine)
    await repl.run()


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="clawpy",
        description="ClawPy — Multi-model CLI coding agent",
    )
    parser.add_argument("-p", "--provider", help="LLM provider (anthropic, openai, gemini, ollama, deepseek)")
    parser.add_argument("-m", "--model", help="Model name/ID")
    parser.add_argument("--dir", default=".", help="Working directory")
    parser.add_argument(
        "--permission-mode",
        default=None,
        choices=["default", "accept_edits", "bypass", "plan"],
        help="Permission mode",
    )
    parser.add_argument("--version", action="version", version="clawpy 0.1.0")
    parser.add_argument(
        "--resume", nargs="?", const="__latest__", default=None, metavar="SESSION_ID",
        help="Resume a previous session (latest if no ID given)",
    )

    sub = parser.add_subparsers(dest="command")

    run_parser = sub.add_parser("run", help="Non-interactive single prompt")
    run_parser.add_argument("prompt", nargs="?", help="Prompt text (or pipe via stdin)")

    login_parser = sub.add_parser("login", help="Login with Claude subscription")
    login_parser.add_argument("--manual", action="store_true", help="Manual code entry (no browser auto-open)")

    sub.add_parser("logout", help="Remove stored credentials")
    sub.add_parser("status", help="Show auth status")

    args = parser.parse_args()

    if args.command == "login":
        asyncio.run(do_login(args))
    elif args.command == "logout":
        do_logout()
    elif args.command == "status":
        do_status()
    elif args.command == "run":
        asyncio.run(run_once(args))
    else:
        asyncio.run(run_repl(args))


if __name__ == "__main__":
    main()
