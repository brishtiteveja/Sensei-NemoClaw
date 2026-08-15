# Benchmark Results Summary

> Last updated: 2026-04-06

## Gemini 2.5 Pro — Run 1

| Case | Category | Result | Tools | Time | Tokens |
|------|----------|--------|-------|------|--------|
| understand_provider_protocol | code_understanding | ✅ PASS | 1 (Read) | 13.0s | 3,403 |
| understand_permission_modes | code_understanding | ✅ PASS | 1 (Read) | 7.7s | 3,075 |
| understand_engine_loop | code_understanding | ✅ PASS | 1 (Read) | 19.1s | 7,720 |
| find_all_tools | code_search | ❌ FAIL | 3 (Glob, ListFiles×2) | 5.7s | 3,246 |
| find_sse_parser | code_search | ❌ FAIL | 4 (ListFiles, Grep×2, ListFiles) | 5.9s | 3,331 |
| count_test_files | code_search | ✅ PASS | 3 (ListFiles, Grep, Bash) | 11.6s | 3,645 |
| trace_provider_flow | multi_step | ❌ FAIL | 3 (ListFiles×3) | 6.0s | 2,112 |
| compare_providers | multi_step | ❌ FAIL | 3 (ListFiles×3) | 7.5s | 3,284 |
| fetch_python_docs | web_research | ✅ PASS | 1 (WebFetch) | 12.9s | 3,010 |

**Summary: 5/9 passed (56%) | 32,826 tokens | 89.6s | 20 tool calls**

### Observations

**Strengths:**
- Single-tool tasks work well (Read→explain, WebFetch→summarize)
- Code understanding is strong when given the right file
- Tool selection is generally correct (Read for files, Grep for search)

**Weaknesses:**
- Multi-step tasks: model stops early without producing final text answer
- Prefers ListFiles over Read/Grep for exploration (less effective)
- Some responses are empty (model generates tool calls but no text after results come back)
- Needs more aggressive system prompt to encourage multi-step reasoning

### Failure Analysis

| Failed Case | Root Cause |
|------------|-----------|
| find_all_tools | Used Glob/ListFiles but didn't read the files to find class names |
| find_sse_parser | Grep failed (ripgrep not in PATH), fell back to ListFiles which wasn't enough |
| trace_provider_flow | Only listed directories, never read any files to trace the actual code path |
| compare_providers | Same — listed dirs but never read anthropic.py or openai.py to compare |

**Key insight:** The model needs to be prompted more aggressively to "read files after finding them" rather than stopping at directory listings. The system prompt could be improved.

---

## Gemini 3 Pro Preview — Run 1

**Result: 0/9 passed (0%)**

All 9 cases: model calls one tool correctly, but after receiving the tool result, the second LLM call returns empty text. The agentic loop completes (tool result is fed back), but the model produces no text response.

**Root cause:** Gemini 3-pro-preview returns HTTP 400 when receiving tool results in the OpenAI-compat format. The tool-use → tool-result → follow-up pattern is broken for this model version.

| Metric | Value |
|--------|-------|
| Passed | 0/9 |
| Tokens | 9,771 |
| Time | 331s (one case hit 300s timeout) |
| Tool calls | 8 |

---

## Gemini 3.1 Pro Preview — Run 1

**Result: 0/9 passed (0%)**

Same issue as Gemini 3 Pro Preview — tools are called but no text follows.

| Metric | Value |
|--------|-------|
| Passed | 0/9 |
| Tokens | 11,001 |
| Time | 32.5s |
| Tool calls | 9 |

---

## Model Comparison

| Model | Passed | Tokens | Time | Tool Calls | Agentic Loop Works? |
|-------|--------|--------|------|------------|---------------------|
| **gemini-2.5-pro** | **5/9 (56%)** | 32,826 | 90s | 20 | ✅ Yes |
| gemini-3-pro-preview | 0/9 (0%) | 9,771 | 331s | 8 | ❌ Tool results rejected |
| gemini-3.1-pro-preview | 0/9 (0%) | 11,001 | 33s | 9 | ❌ Tool results rejected |

**Conclusion:** Only Gemini 2.5 Pro currently works with agentic tool-use via the OpenAI-compat endpoint. The newer Gemini 3.x preview models have breaking issues with tool result formatting. This may improve as these models exit preview.
