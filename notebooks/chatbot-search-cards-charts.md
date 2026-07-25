# LangGraph Chatbot — Search + HTML Cards + Charts

A single-file LangGraph demo that combines:

- **Web search** (DuckDuckGo, no API key)
- **Rich HTML info cards** rendered inline in chat
- **Matplotlib charts** (bar / line / pie / scatter) rendered inline in chat
- **Anthropic Claude** as the model
- **Gradio** as the chat UI

It's deliberately written as **one file with an explicit `StateGraph`** (not `create_react_agent`) so students can see the agent loop wired by hand.

---

## 1. Architecture

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────┐
│  Gradio chat UI │───▶│ LangGraph    │───▶│ Anthropic   │
│  (renders HTML) │    │ StateGraph   │    │ Claude Sonnet 5 │
└─────────────────┘    └──────┬───────┘    └─────────────┘
                              │
                       ┌──────▼──────┐
                       │  Tool node  │
                       ├─────────────┤
                       │ web_search   │  ← DuckDuckGo
                       │ display_card │  ← returns HTML string
                       │ display_chart│  ← returns HTML <img> (base64 PNG)
                       └─────────────┘
```

The graph itself is the canonical 4-node loop from the LangGraph docs:

```
START ──▶ llm_call ──▶ should_continue ──┬─▶ tool_node ──┐
              ▲                          │               │
              └──────────────────────────┘               │
                                         └─▶ END  ◀──────┘
```

`llm_call` produces an `AIMessage`. If it contains `tool_calls`, the graph routes to `tool_node`, executes them, appends `ToolMessage`s, and loops back. Otherwise it ends.

---

## 2. The "tools return HTML, UI sniffs HTML" pattern

The cute trick in this demo: **the UI does no formatting**. Both `display_card` and `display_chart` are LangChain tools that return an HTML string as their tool output. The Gradio `chat_fn` then walks the tool messages from this turn and pulls out anything starting with `<`:

```python
def _extract_html_cards(messages):
    return [m.content for m in messages
            if isinstance(m, ToolMessage) and m.content.lstrip().startswith("<")]
```

That's the entire "rendering pipeline". Consequences:

- **The LLM decides** when a card/chart is appropriate — it's a tool call, just like search.
- **Adding a new visual** = adding a new tool. No UI changes, no state fields.
- **Charts are PNG-in-base64** (`<img src="data:image/png;base64,..."/>`), so they slot into the same sniffer with zero special-casing.

This is the lesson worth pausing on in class: in LangGraph the LLM is the router, and tools are how you give it new "verbs" — including UI verbs.

---

## 3. The three tools

### `web_search(query, max_results=5)`
DuckDuckGo via the `ddgs` package. Returns a JSON array of `{title, url, snippet}`. No API key needed.

### `display_card(title, summary, bullets, source_url)`
Returns a styled HTML card (dark slate background, sky-blue accent stripe). All four user-provided fields are passed through `html.escape()` — the LLM is untrusted input and an unescaped `<script>` in a search snippet is an XSS hole.

### `display_chart(chart_type, title, labels, values, x_label, y_label)`
- `chart_type`: `"bar" | "line" | "pie" | "scatter"`
- Renders with matplotlib using a headless `Agg` backend (set **before** `import pyplot`).
- Saves to `BytesIO` → base64 → embeds as `<img>`.
- Same dark theme as cards but with a violet accent stripe so students can visually distinguish which tool fired.

---

## 4. Running it

### Prerequisites
- Python 3.12+
- [`uv`](https://github.com/astral-sh/uv) installed
- `ANTHROPIC_API_KEY` exported in your shell

### Run
```bash
uv run app.py
```

`uv` reads the inline script metadata at the top of `app.py`, builds an ephemeral venv, installs everything, and runs it. First run takes ~30s (mostly downloading gradio + matplotlib); subsequent runs are instant.

Open the URL Gradio prints — usually **http://127.0.0.1:7860**.

### Stop
```bash
lsof -ti:7860 | xargs kill
```

---

## 5. Demo prompts (in suggested teaching order)

1. **`What is LangGraph in one card?`**
   → Pure card, no search. Shows the simplest tool call.

2. **`Search for the latest news on Claude Sonnet 5 and summarize as a card`**
   → Chains `web_search` → `display_card`. Two trips through the agent loop.

3. **`Plot a bar chart of the populations of the 5 largest EU countries`**
   → Pure model knowledge → chart. Shows the chart tool in isolation.

4. **`Show me a line chart of GPT model release years vs context window size`**
   → Trend over time. Good moment to discuss when "line" beats "bar".

5. **`Search for Python web framework popularity and show me a pie chart`**
   → `web_search` → `display_chart`. Four trips through `llm_call`. Pause and walk students through the message trace.

6. **`Compare LangGraph vs LangChain in a card AND show me a bar chart of their GitHub stars`**
   → Two display tools fire in one assistant turn. Shows that `tool_calls` is a list, not a single value.

---

## 6. Key concepts to highlight in class

### The `add_messages` reducer
```python
class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
```
The `add_messages` annotation is a **reducer** — when a node returns `{"messages": [new_msg]}`, LangGraph **appends** to the existing list instead of overwriting. Without it, every node would clobber history. This is the single most important LangGraph idiom.

### Tool calls as the control signal
```python
def should_continue(state):
    last = state["messages"][-1]
    return "tool_node" if getattr(last, "tool_calls", None) else END
```
The router doesn't read the AI's text — it checks for structured `tool_calls` on the last message. The LLM emits tool calls as a side-channel alongside its natural-language reply, and *that* is what drives the graph. Once students see this, the whole "agent loop" demystifies: it's just `while llm.wants_to_call_a_tool: run_tool`.

### Why explicit `StateGraph` over `create_react_agent`
The prebuilt is one line and hides everything. Building the loop by hand once means the prebuilt becomes a black box you actually understand instead of a magic incantation. After this demo, switching to `create_react_agent` is a comfort upgrade, not a leap of faith.

### Why headless matplotlib
```python
import matplotlib
matplotlib.use("Agg")  # MUST be before `import pyplot`
import matplotlib.pyplot as plt
```
`Agg` is the file-only renderer. Without it, matplotlib tries to open a Tk window on import in some environments and crashes the server. Standard "render to bytes, never display" pattern.

---

## 7. Extending it

Some natural next steps for student exercises:

| Exercise | What it teaches |
|---|---|
| Add a `fetch_url` tool that downloads and summarizes a webpage | Tool composition + content cleaning |
| Add conversation memory with a `MemorySaver` checkpointer | LangGraph persistence (`docs/persistence.md`) |
| Stream tokens to the UI instead of waiting for full responses | LangGraph streaming (`docs/streaming.md`) |
| Add a `display_table` tool that returns an HTML `<table>` | Reinforces the "tools-return-HTML" pattern |
| Make the chart colors a parameter the LLM picks per call | Schema design — what should the model control? |
| Replace the explicit graph with `create_react_agent` and diff the behavior | Understand what the prebuilt hides |

---

## 8. File reference

The full app lives in a single ~310-line file. Key sections:

| Lines | Section |
|---|---|
| top | `uv` inline script metadata (deps) |
| imports | matplotlib `Agg` set **before** `pyplot` |
| `web_search` | DuckDuckGo tool |
| `display_card` + `render_info_card` | HTML card tool + renderer |
| `display_chart` | Matplotlib → base64 PNG → `<img>` |
| `State` + `SYSTEM_PROMPT` | Graph state and the prompt that teaches the LLM when to use each tool |
| `llm_call` / `tool_node` / `should_continue` | The three node functions |
| `builder = StateGraph(State)` ... `agent = builder.compile()` | Graph wiring |
| `chat_fn` + `_extract_html_cards` | Gradio bridge |
| `main()` | Launch |

---

## 9. Source app

The original working file is at:

```
~/Desktop/projects/oreilly-live-trainings/tmp-langgraph/langgraph-local-docs/chatbot/app.py
```

Copy it next to this guide if you want a fully self-contained module:

```bash
cp ~/Desktop/projects/oreilly-live-trainings/tmp-langgraph/langgraph-local-docs/chatbot/app.py \
   ~/Desktop/projects/oreilly-live-trainings/oreilly-langgraph/notebooks/
```
