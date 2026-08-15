"""Real-world benchmark runner for ClawPy.

Tests the agentic loop end-to-end with real LLM APIs on read-only tasks.
Uses the clawpy codebase itself as the test repository.

Usage:
    GEMINI_API_KEY=... uv run python benchmarks/run_benchmark.py
    OPENAI_API_KEY=... uv run python benchmarks/run_benchmark.py --provider openai --model gpt-4o
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from clawpy.config.config import Config, ProviderConfig
from clawpy.engine.engine import Engine, TurnResult
from clawpy.engine.system_prompt import build_system_prompt
from clawpy.provider.base import EventType, StreamEvent
from clawpy.tool.permission import PermissionEnforcer, PermissionMode
from clawpy.tool.registry import ToolRegistry
from clawpy.engine.file_state import FileStateTracker
from clawpy.tool.bash import BashTool
from clawpy.tool.file_read import FileReadTool
from clawpy.tool.grep_tool import GrepTool
from clawpy.tool.glob_tool import GlobTool
from clawpy.tool.list_files import ListFilesTool
from clawpy.tool.web_fetch import WebFetchTool


@dataclass
class BenchmarkCase:
    name: str
    prompt: str
    check: str  # substring expected in final answer
    category: str  # code_understanding, code_search, web_research, multi_step


@dataclass
class BenchmarkResult:
    case: BenchmarkCase
    passed: bool
    answer: str
    tool_calls: int
    iterations: int
    input_tokens: int
    output_tokens: int
    elapsed_sec: float
    error: str = ""


# ---- Benchmark Cases ----
# All read-only: analyze the clawpy codebase itself

BENCHMARKS: list[BenchmarkCase] = [
    # Code understanding
    BenchmarkCase(
        name="understand_provider_protocol",
        prompt="Read src/clawpy/provider/base.py and explain what the Provider Protocol requires. What methods must a provider implement?",
        check="stream",
        category="code_understanding",
    ),
    BenchmarkCase(
        name="understand_permission_modes",
        prompt="Read src/clawpy/tool/permission.py and list all permission modes and what each one does.",
        check="bypass",
        category="code_understanding",
    ),
    BenchmarkCase(
        name="understand_engine_loop",
        prompt="Read src/clawpy/engine/engine.py and explain the agentic loop in run_turn(). How does it handle tool calls?",
        check="tool",
        category="code_understanding",
    ),

    # Code search
    BenchmarkCase(
        name="find_all_tools",
        prompt="Search the codebase to find all tool implementations. List the name of each tool class and its file path.",
        check="BashTool",
        category="code_search",
    ),
    BenchmarkCase(
        name="find_sse_parser",
        prompt="Find where SSE (Server-Sent Events) parsing is implemented. What function handles it and how does it work?",
        check="parse_sse",
        category="code_search",
    ),
    BenchmarkCase(
        name="count_test_files",
        prompt="How many test files are in the tests/ directory? List them and count the total number of test functions across all files.",
        check="test_",
        category="code_search",
    ),

    # Multi-step reasoning
    BenchmarkCase(
        name="trace_provider_flow",
        prompt="Trace the code path: when a user runs 'clawpy run \"hello\"', how does the prompt get from CLI to the Anthropic API? List each file and function in order.",
        check="cli",
        category="multi_step",
    ),
    BenchmarkCase(
        name="compare_providers",
        prompt="Read the anthropic.py and openai.py provider files. What are the key differences in how they handle streaming events? Be specific about the event mapping.",
        check="content_block",
        category="multi_step",
    ),

    # Web research
    BenchmarkCase(
        name="fetch_python_docs",
        prompt="Fetch https://docs.python.org/3/library/asyncio.html and summarize what asyncio is used for in 2-3 sentences.",
        check="asyncio",
        category="web_research",
    ),
]


def build_read_only_engine(provider_name: str, model: str, api_key: str, work_dir: str) -> Engine:
    """Build an engine with read-only tools only."""
    # Import provider to register
    if provider_name == "gemini":
        import clawpy.provider.gemini
    elif provider_name == "openai":
        import clawpy.provider.openai
    elif provider_name == "anthropic":
        import clawpy.provider.anthropic
    else:
        import clawpy.provider.openai

    from clawpy.provider.registry import create

    cfg = Config(
        provider=provider_name,
        model=model,
        work_dir=work_dir,
        permission_mode="bypass",
        max_tokens=16384,
    )

    provider_cfg = ProviderConfig(api_key=api_key, model=model)
    provider = create(provider_name, provider_cfg)

    fs = FileStateTracker()
    tools = ToolRegistry()
    tools.register(BashTool())
    tools.register(FileReadTool(file_state=fs))
    tools.register(GrepTool())
    tools.register(GlobTool())
    tools.register(ListFilesTool())
    tools.register(WebFetchTool())

    enforcer = PermissionEnforcer(mode=PermissionMode.BYPASS, work_dir=work_dir)

    engine = Engine(provider=provider, tools=tools, enforcer=enforcer, config=cfg)
    engine.set_system_prompt(build_system_prompt(work_dir, model))
    return engine


async def run_single_benchmark(
    engine: Engine, case: BenchmarkCase
) -> BenchmarkResult:
    """Run a single benchmark case."""
    engine.clear()
    start = time.time()
    tool_count = 0
    text_buf = ""

    def on_stream(event: StreamEvent) -> None:
        nonlocal tool_count, text_buf
        if event.type == EventType.TOOL_START:
            tool_count += 1
            if event.tool_call:
                print(f"    ⚡ {event.tool_call.name}", flush=True)
        if event.delta and event.delta.text:
            text_buf += event.delta.text

    try:
        result = await engine.run_turn(case.prompt, on_stream=on_stream)
        elapsed = time.time() - start

        # Get final answer
        answer = ""
        for msg in reversed(result.messages):
            if msg.role.value == "assistant":
                answer = msg.text_content()
                if answer:
                    break

        passed = case.check.lower() in answer.lower()

        return BenchmarkResult(
            case=case,
            passed=passed,
            answer=answer[:500],
            tool_calls=tool_count,
            iterations=len([m for m in result.messages if m.role.value == "assistant"]),
            input_tokens=result.usage.input_tokens,
            output_tokens=result.usage.output_tokens,
            elapsed_sec=elapsed,
        )
    except Exception as e:
        return BenchmarkResult(
            case=case,
            passed=False,
            answer="",
            tool_calls=tool_count,
            iterations=0,
            input_tokens=0,
            output_tokens=0,
            elapsed_sec=time.time() - start,
            error=str(e),
        )


async def main() -> None:
    parser = argparse.ArgumentParser(description="ClawPy Benchmark Runner")
    parser.add_argument("-p", "--provider", default="gemini")
    parser.add_argument("-m", "--model", default="gemini-2.5-pro")
    parser.add_argument("--cases", nargs="*", help="Run specific cases by name")
    parser.add_argument("--category", help="Run cases in a category")
    args = parser.parse_args()

    # Resolve API key
    key_env = {
        "gemini": "GEMINI_API_KEY",
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
    }
    api_key = os.environ.get(key_env.get(args.provider, ""), "")
    if not api_key:
        print(f"Error: Set {key_env.get(args.provider, 'API_KEY')} env var", file=sys.stderr)
        sys.exit(1)

    work_dir = str(Path(__file__).parent.parent)

    print(f"ClawPy Benchmark — {args.provider}:{args.model}")
    print(f"Work dir: {work_dir}")
    print(f"{'='*60}\n")

    # Filter cases
    cases = BENCHMARKS
    if args.cases:
        cases = [c for c in cases if c.name in args.cases]
    if args.category:
        cases = [c for c in cases if c.category == args.category]

    engine = build_read_only_engine(args.provider, args.model, api_key, work_dir)

    results: list[BenchmarkResult] = []
    for i, case in enumerate(cases):
        print(f"[{i+1}/{len(cases)}] {case.name} ({case.category})")
        result = await run_single_benchmark(engine, case)

        status = "✅ PASS" if result.passed else "❌ FAIL"
        if result.error:
            status = f"💥 ERROR: {result.error[:80]}"

        print(f"  {status} | {result.tool_calls} tools | "
              f"{result.elapsed_sec:.1f}s | "
              f"{result.input_tokens}↓ {result.output_tokens}↑")
        if not result.passed and not result.error:
            print(f"  Expected '{case.check}' in answer")
            print(f"  Answer: {result.answer[:200]}...")
        print()
        results.append(result)

    # Summary
    passed = sum(1 for r in results if r.passed)
    total = len(results)
    total_tokens = sum(r.input_tokens + r.output_tokens for r in results)
    total_time = sum(r.elapsed_sec for r in results)
    total_tools = sum(r.tool_calls for r in results)

    print(f"{'='*60}")
    print(f"Results: {passed}/{total} passed")
    print(f"Total tokens: {total_tokens:,}")
    print(f"Total time: {total_time:.1f}s")
    print(f"Total tool calls: {total_tools}")
    print(f"Provider: {args.provider}:{args.model}")

    # Save results
    output_file = Path(__file__).parent / "results" / f"{args.provider}_{args.model}_{int(time.time())}.json"
    output_file.parent.mkdir(exist_ok=True)
    output_file.write_text(json.dumps({
        "provider": args.provider,
        "model": args.model,
        "timestamp": time.time(),
        "summary": {"passed": passed, "total": total, "tokens": total_tokens, "time_sec": total_time},
        "results": [
            {
                "name": r.case.name,
                "category": r.case.category,
                "passed": r.passed,
                "tool_calls": r.tool_calls,
                "input_tokens": r.input_tokens,
                "output_tokens": r.output_tokens,
                "elapsed_sec": r.elapsed_sec,
                "error": r.error,
                "answer_preview": r.answer[:200],
            }
            for r in results
        ],
    }, indent=2))
    print(f"Results saved to: {output_file}")


if __name__ == "__main__":
    asyncio.run(main())
