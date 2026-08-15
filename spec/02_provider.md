# 02 — Provider Abstraction & Multi-Model Support

## File: `src/clawpy/provider/`

## Provider Protocol

```python
@runtime_checkable
class Provider(Protocol):
    @property
    def name(self) -> str: ...
    async def stream(self, request: Request) -> AsyncIterator[StreamEvent]: ...
    async def send(self, request: Request) -> Response: ...
    def models(self) -> list[str]: ...
```

## Request / Response Types

### Request (provider-neutral)
```python
@dataclass(slots=True)
class Request:
    model: str
    system: str              # System prompt
    messages: list[Message]  # Conversation history
    tools: list[ToolSpec]    # Available tools
    max_tokens: int = 8192
    temperature: float | None = None
    stop_sequences: list[str] = field(default_factory=list)
```

### ToolSpec (sent to provider)
```python
@dataclass(frozen=True, slots=True)
class ToolSpec:
    name: str
    description: str
    input_schema: dict[str, Any]  # JSON Schema
```

## StreamEvent — The Streaming Protocol

```python
class EventType(Enum):
    DELTA        # Text or thinking chunk
    TOOL_START   # New tool call block
    TOOL_DELTA   # Tool input JSON chunk
    TOOL_END     # Tool call finalized
    MESSAGE_STOP # Response complete
    ERROR        # Error occurred
```

Event flow for a typical response with one tool call:
```
DELTA(text="I'll read the file.")
TOOL_START(tool_call=ToolCall(id="tc_1", name="Read", input={}))
TOOL_DELTA(delta=Delta(text='{"file_path":'))
TOOL_DELTA(delta=Delta(text=' "/tmp/foo.py"}'))
TOOL_END(tool_call=ToolCall(id="tc_1", name="Read", input={"file_path": "/tmp/foo.py"}))
MESSAGE_STOP(stop_reason=TOOL_USE, usage=Usage(input_tokens=150, output_tokens=42))
```

## SSE Parser (shared)

File: `provider/sse.py`

Both Anthropic and OpenAI use `text/event-stream` with `data: {...}\n\n` framing.
A single async generator handles both:

```python
async def parse_sse(response: httpx.Response) -> AsyncIterator[dict[str, Any]]:
    async for line in response.aiter_lines():
        if line.startswith("data: ") and line[6:] != "[DONE]":
            yield json.loads(line[6:])
```

For Anthropic (which uses `event:` fields):
```python
async def parse_sse_with_event(response) -> AsyncIterator[tuple[str, dict[str, Any]]]:
    # yields (event_type, data) tuples
```

## Provider Implementations

### Anthropic (`provider/anthropic.py`) — DONE

Direct Messages API via httpx. Key conversion:
- System prompt → `system` field (string or array)
- Messages → Anthropic content blocks (`text`, `tool_use`, `tool_result`)
- Streaming: `content_block_start/delta/stop` + `message_delta/stop`
- Tool JSON accumulated during `input_json_delta` events, parsed on `content_block_stop`

### OpenAI (`provider/openai.py`) — Phase 3

Chat Completions API. Key conversion (mirrors `openaiShim.ts`):

**Message conversion** (neutral → OpenAI):
- System prompt → `{role: "system", content: text}`
- ToolCall blocks → `{role: "assistant", tool_calls: [{id, type:"function", function:{name, arguments}}]}`
- ToolResult blocks → `{role: "tool", tool_call_id, content}`
- Thinking blocks → stripped (OpenAI doesn't support them)

**Tool conversion** (ToolSpec → OpenAI):
- `{type: "function", function: {name, description, parameters}}`
- Normalize: all properties added to `required` array (OpenAI strict mode)

**Stream mapping** (OpenAI SSE → StreamEvent):
State machine tracking:
- `content_started: bool`
- `active_tool_calls: dict[int, ToolCall]` (keyed by OpenAI `tc.index`)
- `tool_json_bufs: dict[int, str]`

Mapping:
- `delta.content` → `EventType.DELTA`
- `delta.tool_calls` with `id` + `name` → `EventType.TOOL_START`
- `delta.tool_calls` with only `arguments` → `EventType.TOOL_DELTA`
- `finish_reason == "tool_calls"` → close all blocks + `MESSAGE_STOP(TOOL_USE)`
- `finish_reason == "stop"` → `MESSAGE_STOP(END_TURN)`
- `finish_reason == "length"` → `MESSAGE_STOP(MAX_TOKENS)`

### Gemini (`provider/gemini.py`) — Phase 3

Uses OpenAI-compatible endpoint. Inherits from OpenAIProvider with:
- Base URL: `https://generativelanguage.googleapis.com/v1beta/openai`
- API key: `GEMINI_API_KEY`
- Model: `GEMINI_MODEL`

### Ollama (`provider/ollama.py`) — Phase 3

OpenAI-compatible local endpoint:
- Base URL: `http://localhost:11434/v1` (or `OLLAMA_BASE_URL`)
- No API key required
- Auto-discovery: check if Ollama is running at startup

### DeepSeek (`provider/deepseek.py`) — Phase 3

OpenAI-compatible with reasoning:
- Base URL: `https://api.deepseek.com/v1`
- API key: `DEEPSEEK_API_KEY`
- Reasoning tokens mapped to thinking blocks

## Provider Registry

```python
ProviderFactory = Callable[[ProviderConfig], Provider]
_registry: dict[str, ProviderFactory] = {}

def register(name: str, factory: ProviderFactory) -> None: ...
def create(name: str, cfg: ProviderConfig) -> Provider: ...
```

Each provider file calls `register()` at import time. The CLI imports provider
modules to trigger registration.

## Provider Auto-Detection

```python
def detect_provider() -> str:
    # 1. CLAWPY_PROVIDER env (explicit)
    # 2. CLAUDE_CODE_USE_OPENAI=1
    # 3. CLAUDE_CODE_USE_GEMINI=1
    # 4. ANTHROPIC_API_KEY set → anthropic
    # 5. OPENAI_API_KEY set → openai
    # 6. GEMINI_API_KEY set → gemini
    # 7. Default: anthropic
```
