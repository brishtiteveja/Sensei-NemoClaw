# 01 — Core Types & Message Format

## File: `src/clawpy/types.py`

All types use `dataclass(slots=True)` for memory efficiency. Frozen where immutable.

## Role

```python
class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
```

## ContentType

```python
class ContentType(str, Enum):
    TEXT = "text"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    THINKING = "thinking"
    IMAGE = "image"
```

## Core Types

### ToolCall
```python
@dataclass(frozen=True, slots=True)
class ToolCall:
    id: str          # Provider-assigned ID (e.g. "toolu_abc123")
    name: str        # Tool name (e.g. "Bash", "Read")
    input: dict[str, Any]  # Parsed JSON input from model
```

### ToolResult
```python
@dataclass(frozen=True, slots=True)
class ToolResult:
    tool_call_id: str  # Matches ToolCall.id
    content: str       # Tool output text
    is_error: bool = False
```

### ContentBlock
```python
@dataclass(slots=True)
class ContentBlock:
    type: ContentType
    text: str = ""
    tool_call: ToolCall | None = None
    tool_result: ToolResult | None = None
    thinking: str = ""
    image: ImageData | None = None
```

Union-style: exactly one payload field is meaningful per `type`. This mirrors:
- OpenClaude TS: content blocks in `ToolUseBlockParam` / `TextBlock` / etc.
- claw-code Rust: `ContentBlock` enum with 7 variants
- claurst Rust: untagged serde enum

### Message
```python
@dataclass(slots=True)
class Message:
    role: Role
    content: list[ContentBlock]
    id: str = ""

    def text_content(self) -> str: ...
    def tool_calls(self) -> list[ToolCall]: ...
    def tool_results(self) -> list[ToolResult]: ...
```

## Message Flow Patterns

### User text message
```
Message(role=USER, content=[ContentBlock(type=TEXT, text="List files")])
```

### Assistant with tool call
```
Message(role=ASSISTANT, content=[
    ContentBlock(type=TEXT, text="I'll list the files."),
    ContentBlock(type=TOOL_CALL, tool_call=ToolCall(id="tc_1", name="Bash", input={"command": "ls"})),
])
```

### Tool result (sent as user message)
```
Message(role=USER, content=[
    ContentBlock(type=TOOL_RESULT, tool_result=ToolResult(tool_call_id="tc_1", content="file1.py\nfile2.py")),
])
```

### Assistant with thinking
```
Message(role=ASSISTANT, content=[
    ContentBlock(type=THINKING, thinking="Let me analyze the directory structure..."),
    ContentBlock(type=TEXT, text="Here are the files..."),
])
```

## Provider Conversion

Each provider converts to/from these neutral types:

| Neutral type | Anthropic API | OpenAI API |
|-------------|---------------|------------|
| `ContentBlock(TEXT)` | `{type: "text", text}` | `{role: "assistant", content: text}` |
| `ContentBlock(TOOL_CALL)` | `{type: "tool_use", id, name, input}` | `tool_calls: [{id, function: {name, arguments}}]` |
| `ContentBlock(TOOL_RESULT)` | `{type: "tool_result", tool_use_id, content}` | `{role: "tool", tool_call_id, content}` |
| `ContentBlock(THINKING)` | `{type: "thinking", thinking}` | stripped (not supported) |

## Read-File State Tracking

The engine maintains a `read_file_state: dict[str, FileState]` mapping file paths to their
last-read state (mtime, content hash). This enables:
- **Read-before-write enforcement**: FileEdit/FileWrite check the file exists in state
- **Staleness detection**: Reject edits if file modified since last read
- **Dedup**: Return "file_unchanged" if same content re-read

```python
@dataclass(slots=True)
class FileState:
    path: str
    mtime: float
    content_hash: str
    line_count: int
```
