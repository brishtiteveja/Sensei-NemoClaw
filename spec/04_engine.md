# 04 — Engine: Agentic Loop, Token Budget, Auto-Compact

## File: `src/clawpy/engine/`

This is the heart of ClawPy — the agentic loop that streams responses,
executes tools, and manages context window.

## Engine Class

```python
class Engine:
    provider: Provider
    tools: ToolRegistry
    enforcer: PermissionEnforcer
    config: Config
    messages: list[Message]
    system_prompt: str
    read_file_state: dict[str, FileState]  # Track read files for edit/write enforcement
    total_usage: Usage
```

## run_turn() — The Agentic Loop

```python
async def run_turn(self, user_input: str, on_stream: Callback | None) -> TurnResult:
```

**Loop structure** (mirrors `query.ts`):
```
for iteration in range(MAX_ITERATIONS):    # MAX_ITERATIONS = 50
    1. Build Request
    2. Stream response → assemble assistant Message
    3. Extract tool calls
    4. If no tools or end_turn → return
    5. Execute tools (permission check + run)
    6. Append results as user message
    7. Check token budget
    8. Check auto-compact threshold
    9. Continue loop
```

## Stream Consumer — State Machine

```python
async def _consume_stream(self, request, on_stream) -> tuple[Message, StopReason, Usage]:
```

State variables (mirrors `openaiStreamToAnthropic()` in openaiShim.ts):
```python
text_buf: str = ""                          # Accumulated text
thinking_buf: str = ""                      # Accumulated thinking
completed_tool_calls: list[ToolCall] = []   # Finalized tools
active_tools: dict[str, ToolCall] = {}      # id → partial ToolCall
tool_json_bufs: dict[str, str] = {}         # id → accumulated JSON string
current_tool_id: str | None = None
stop_reason: StopReason = StopReason.END_TURN
total_usage: Usage = Usage()
```

Event handling:
- `DELTA` → append to text_buf or thinking_buf
- `TOOL_START` → register in active_tools, init JSON buffer
- `TOOL_DELTA` → append to tool_json_bufs[current_tool_id]
- `TOOL_END` → parse JSON, finalize ToolCall, move to completed
- `MESSAGE_STOP` → extract stop_reason + usage
- `ERROR` → log, append error text

## Token Budget Management

From claurst spec and OpenClaude's `query/tokenBudget.ts`:

```python
COMPLETION_THRESHOLD = 0.9      # Stop at 90% of context window
DIMINISHING_THRESHOLD = 500     # Stop if <500 token delta after 3+ continuations
MAX_CONTEXT_TOKENS = 200_000    # Default context window

@dataclass(slots=True)
class TokenBudget:
    context_window: int = MAX_CONTEXT_TOKENS
    continuation_count: int = 0
    last_delta_tokens: int = 0

    def should_continue(self, current_tokens: int) -> bool:
        """Check if we should continue the loop."""
        if current_tokens >= self.context_window * COMPLETION_THRESHOLD:
            return False
        if (self.continuation_count >= 3
            and self.last_delta_tokens < DIMINISHING_THRESHOLD):
            return False
        return True
```

## Auto-Compact

Triggered when context approaches limit. From claurst spec:

```python
AUTOCOMPACT_TRIGGER = 0.90      # Trigger at 90% of context window
KEEP_RECENT_MESSAGES = 10       # Keep last 10 messages after compact
MAX_COMPACT_FAILURES = 3        # Circuit breaker

async def auto_compact(self) -> None:
    """Summarize older messages to free context space."""
    if not self._should_compact():
        return

    # Take all messages except last KEEP_RECENT_MESSAGES
    old_messages = self.messages[:-KEEP_RECENT_MESSAGES]
    recent_messages = self.messages[-KEEP_RECENT_MESSAGES:]

    # Ask the model to summarize the old conversation
    summary = await self._summarize_messages(old_messages)

    # Replace history with: summary message + recent messages
    self.messages = [
        text_message(Role.USER, f"[Conversation summary]\n{summary}"),
        text_message(Role.ASSISTANT, "Understood, I'll continue from this context."),
        *recent_messages,
    ]
```

## Recovery Paths

From OpenClaude's `query.ts`:

1. **Max output tokens**: If response hits `max_tokens`, retry up to 3 times
   with escalating `max_tokens` (8K → 16K → 64K)
2. **Prompt too long**: Trigger reactive compact, retry
3. **Rate limit**: Exponential backoff with `Retry-After` header

```python
async def _handle_recovery(self, error: Exception, iteration: int) -> bool:
    """Returns True if recovery succeeded and loop should continue."""
    if isinstance(error, MaxTokensError) and self._max_tokens_retries < 3:
        self.config.max_tokens = min(self.config.max_tokens * 2, 64000)
        self._max_tokens_retries += 1
        return True
    if isinstance(error, PromptTooLongError):
        await self.auto_compact()
        return True
    return False
```

## Tool Execution

```python
async def _execute_tools(self, calls: list[ToolCall]) -> list[ToolResult]:
    batches = self._partition_tool_calls(calls)
    results: list[ToolResult] = []
    for batch in batches:
        if len(batch) == 1:
            results.append(await self._run_single_tool(batch[0]))
        else:
            # All read-only → concurrent
            coros = [self._run_single_tool(tc) for tc in batch]
            results.extend(await asyncio.gather(*coros))
    return results
```

### Partition Logic
```
[Read, Grep, Glob, Bash(ls), Edit, Read, Read]
 ╰───── concurrent ─────╯   ╰serial╯ ╰concurrent╯
```

Consecutive read-only tools form a concurrent batch.
Any non-read-only tool forms a serial batch of 1.

## TurnResult

```python
@dataclass(slots=True)
class TurnResult:
    messages: list[Message]     # Full updated history
    stop_reason: StopReason
    usage: Usage
    error: str | None = None    # Non-fatal error/warning
```
