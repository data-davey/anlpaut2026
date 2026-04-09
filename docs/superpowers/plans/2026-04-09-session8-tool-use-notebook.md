# Session 8 Tool Use Notebook Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create `material/Session 8/notebooks/06_tool_use.ipynb` — a self-contained teaching notebook covering tool/function calling with the OpenAI Responses API, from schema anatomy through built-in tools to RAG-as-a-tool.

**Architecture:** Follows the style of `01_llm_api_access.ipynb` and `03_streaming_responses.ipynb` — markdown headers, `# Requires OPENAI_API_KEY / Skip this cell` guards, `make_openai_client` / `require_env` helpers reused from notebook 01. Sections progress from concept → simple custom tool → agentic loop → built-in tools → parallel calls → RAG bridge. No Azure dependency anywhere.

**Tech Stack:** Python 3, `openai`, `python-dotenv`, `requests` (for wttr.in weather), `faiss-cpu`, `numpy`, `pdfplumber` (reused from notebook 04 for the RAG-as-tool section)

---

## File Structure

- **Create:** `material/Session 8/notebooks/06_tool_use.ipynb`
  - All notebook content lives here. No helper modules needed — all functions are defined inline for teachability.
- **Reference (read-only):** `material/Session 8/notebooks/01_llm_api_access.ipynb` — for `make_openai_client`, `require_env`, `session8_dir` helpers to copy verbatim into this notebook's setup cell
- **Reference (read-only):** `material/Session 8/helpers/rag_utils.py` — for `load_and_chunk_pdfs`, `build_faiss_index`, `search_index` to reuse in the RAG-as-tool section
- **Reference (read-only):** `material/Session 8/.old/01.5 Tools and Functions.ipynb` — source of the weather tool pattern and agentic loop

---

## Task 1: Notebook scaffold and setup cell

**Files:**
- Create: `material/Session 8/notebooks/06_tool_use.ipynb`

- [ ] **Step 1: Create the notebook file**

Create `material/Session 8/notebooks/06_tool_use.ipynb` with the following cells in order. Use `nbformat` or write the JSON directly. The notebook must be valid `.ipynb` format (nbformat 4).

Cell 0 — markdown:
```markdown
# Session 8 — Tool Use and Function Calling

LLMs are excellent at reasoning but cannot act on the world directly. Tool use (also called function calling) gives the model a way to request external actions — fetching live data, running calculations, searching a document store — and incorporate the results into its answer.

This notebook covers:
1. Anatomy of a tool definition (JSON schema)
2. A custom weather tool — the classic first example
3. The agentic loop step by step
4. Built-in tools: `web_search` and `code_interpreter`
5. Parallel tool calls — two tools in one turn
6. RAG as a tool call — the model decides when to retrieve
```

Cell 1 — markdown:
```markdown
## Learning Goals

- understand the JSON schema format for tool definitions
- implement the four-step agentic loop (request → detect → execute → feed back)
- use built-in OpenAI tools without writing a Python function
- define multiple tools and handle parallel calls
- refactor the RAG pipeline from notebook 04 so the model controls retrieval
```

Cell 2 — code (setup):
```python
import json
import os
import requests
from pathlib import Path

from dotenv import load_dotenv
from IPython.display import Markdown, display
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ORG_ID = os.getenv("OPENAI_ORG_ID")
OPENAI_PROJECT_ID = os.getenv("OPENAI_PROJECT_ID")

print("OpenAI key present:", bool(OPENAI_API_KEY))


def make_openai_client(api_key=None, base_url=None):
    kwargs = {}
    if api_key:
        kwargs["api_key"] = api_key
    if base_url:
        kwargs["base_url"] = base_url
    if api_key == OPENAI_API_KEY and not base_url:
        if OPENAI_ORG_ID:
            kwargs["organization"] = OPENAI_ORG_ID
        if OPENAI_PROJECT_ID:
            kwargs["project"] = OPENAI_PROJECT_ID
    return OpenAI(**kwargs)


def require_env(name: str):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def session8_dir() -> Path:
    cwd = Path.cwd()
    if cwd.name == "notebooks":
        return cwd.parent
    candidate = cwd / "material" / "Session 8"
    if candidate.exists():
        return candidate
    return cwd
```

- [ ] **Step 2: Verify the notebook opens without errors**

```bash
cd /c/git/mdsiprojects/anlpaut2026
jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=30 \
  "material/Session 8/notebooks/06_tool_use.ipynb" \
  --output /tmp/06_tool_use_check.ipynb 2>&1 | head -20
```

The setup cell and markdown cells should execute without error. API calls come in later tasks — skip via `# Skip this cell` guard for now.

- [ ] **Step 3: Commit scaffold**

```bash
git add "material/Session 8/notebooks/06_tool_use.ipynb"
git commit -m "session 8: add tool use notebook scaffold and setup cell"
```

---

## Task 2: Anatomy of a tool definition + weather tool

**Files:**
- Modify: `material/Session 8/notebooks/06_tool_use.ipynb`

- [ ] **Step 1: Add the anatomy section (markdown + annotated schema cell)**

Append these cells:

Cell — markdown:
```markdown
## 1. Anatomy of a Tool Definition

Every tool is a Python dict that follows the OpenAI JSON schema format. The model reads `description` to decide when to call the tool, and `parameters` to know what arguments to pass.
```

Cell — code:
```python
# Annotated tool schema — nothing executes here, just for reading

weather_tool = {
    "type": "function",           # always "function" for custom tools
    "name": "get_weather",        # must match the Python function name you will call
    "description": (
        "Returns current weather conditions for a city. "
        "Call this whenever the user asks about weather or temperature."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "City name, e.g. Sydney, Paris, New York",
            },
            "units": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
                "description": "Temperature unit to return.",
            },
        },
        "required": ["location", "units"],
        "additionalProperties": False,
    },
    "strict": True,   # model must fill all required fields; no extra fields allowed
}

print(json.dumps(weather_tool, indent=2))
```

- [ ] **Step 2: Add the Python implementation of the weather tool**

Cell — markdown:
```markdown
## 2. Custom Tool: Weather

`get_weather` calls the free wttr.in API — no API key needed. The function signature must match the `name` and `parameters` in the schema above.
```

Cell — code:
```python
def get_weather(location: str, units: str = "celsius") -> dict:
    """Fetch current weather from wttr.in (free, no API key required)."""
    unit_char = "m" if units == "celsius" else "u"
    url = f"https://wttr.in/{requests.utils.quote(location)}?format=j1&{unit_char}"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        current = data["current_condition"][0]
        temp = current["temp_C"] if units == "celsius" else current["temp_F"]
        desc = current["weatherDesc"][0]["value"]
        return {
            "location": location,
            "temperature": int(temp),
            "units": units,
            "description": desc,
        }
    except Exception as e:
        return {"error": str(e), "location": location}


# Quick smoke test — confirm the function works before wiring it to the model
result = get_weather("Sydney", "celsius")
print(result)
```

- [ ] **Step 3: Verify output**

Running the cell should print something like:
```
{'location': 'Sydney', 'temperature': 22, 'units': 'celsius', 'description': 'Partly cloudy'}
```

If wttr.in is unavailable the function returns `{'error': '...', 'location': 'Sydney'}` — that is fine, the error path is intentional.

- [ ] **Step 4: Commit**

```bash
git add "material/Session 8/notebooks/06_tool_use.ipynb"
git commit -m "session 8: tool use notebook — anatomy section and weather tool"
```

---

## Task 3: The agentic loop — step by step

**Files:**
- Modify: `material/Session 8/notebooks/06_tool_use.ipynb`

- [ ] **Step 1: Add the four-step loop cells**

Cell — markdown:
```markdown
## 3. The Agentic Loop

Tool use works in four steps:

1. **Request** — send the user message plus the tool list to the model
2. **Detect** — check if the model returned a `function_call` in `response.output`
3. **Execute** — call the matching Python function with the model's arguments
4. **Feed back** — append the result as `function_call_output` and call the model again

The model then produces a final answer that incorporates the tool result.
```

Cell — markdown:
```markdown
### Step 1 — Send the request with tools
```

Cell — code:
```python
# Requires OPENAI_API_KEY
# Skip this cell if you do not have live API access.

client = make_openai_client(api_key=require_env("OPENAI_API_KEY"))

input_messages = [
    {"role": "user", "content": "What is the weather like in Tokyo right now? Use celsius."}
]

response = client.responses.create(
    model="gpt-4o-mini",
    tools=[weather_tool],
    input=input_messages,
    tool_choice="auto",   # model decides whether to call a tool
)

print("Output types:", [item.type for item in response.output])
```

Cell — markdown:
```markdown
### Step 2 — Detect the function call

The model signals it wants to call a tool by including a `function_call` item in `response.output`. We inspect the output list and find it.
```

Cell — code:
```python
# Requires OPENAI_API_KEY
# Skip this cell if you do not have live API access.

tool_call = None
for item in response.output:
    if item.type == "function_call":
        tool_call = item
        break

if tool_call:
    print("Function to call:", tool_call.name)
    print("Arguments (JSON string):", tool_call.arguments)
    print("Call ID:", tool_call.call_id)
else:
    print("Model did not request a tool call.")
```

Cell — markdown:
```markdown
### Step 3 — Execute the function locally

We parse the JSON arguments and call the matching Python function.
```

Cell — code:
```python
# Requires OPENAI_API_KEY
# Skip this cell if you do not have live API access.

if tool_call:
    args = json.loads(tool_call.arguments)
    print("Parsed arguments:", args)

    # Dispatch: call the function whose name matches tool_call.name
    tool_result = get_weather(**args)
    print("Tool result:", tool_result)
```

Cell — markdown:
```markdown
### Step 4 — Feed the result back and get the final answer

We append the model's tool call output and a `function_call_output` message, then call the model again.
```

Cell — code:
```python
# Requires OPENAI_API_KEY
# Skip this cell if you do not have live API access.

if tool_call:
    # Append the model's tool call items to the conversation
    input_messages = input_messages + list(response.output)

    # Append our tool result
    input_messages.append({
        "type": "function_call_output",
        "call_id": tool_call.call_id,
        "output": json.dumps(tool_result),
    })

    # Second model call — now it has the tool result
    final_response = client.responses.create(
        model="gpt-4o-mini",
        tools=[weather_tool],
        input=input_messages,
        tool_choice="auto",
    )

    display(Markdown(final_response.output_text))
```

- [ ] **Step 2: Add the clean reusable loop helper**

Cell — markdown:
```markdown
### Clean Helper: `run_tool_loop`

The four steps above always follow the same pattern. We can wrap them in a reusable function.
```

Cell — code:
```python
# Map of tool name -> callable Python function
TOOL_REGISTRY = {
    "get_weather": get_weather,
}


def run_tool_loop(
    user_message: str,
    tools: list,
    registry: dict,
    model: str = "gpt-4o-mini",
    max_rounds: int = 5,
) -> str:
    """
    Run the agentic tool loop until the model stops calling tools or max_rounds is reached.

    Returns the final text response.
    """
    client = make_openai_client(api_key=require_env("OPENAI_API_KEY"))
    messages = [{"role": "user", "content": user_message}]

    for round_num in range(max_rounds):
        response = client.responses.create(
            model=model,
            tools=tools,
            input=messages,
            tool_choice="auto",
        )

        # Collect any function calls in this response
        calls = [item for item in response.output if item.type == "function_call"]

        if not calls:
            # No tool calls — model is done
            return response.output_text

        # Append the model's output to keep the conversation history intact
        messages = messages + list(response.output)

        # Execute each tool call and append results
        for call in calls:
            fn = registry.get(call.name)
            if fn is None:
                result = {"error": f"Unknown tool: {call.name}"}
            else:
                result = fn(**json.loads(call.arguments))

            messages.append({
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": json.dumps(result),
            })

    return "Max tool rounds reached without a final answer."
```

Cell — code:
```python
# Requires OPENAI_API_KEY
# Skip this cell if you do not have live API access.

answer = run_tool_loop(
    user_message="What is the weather in London and Paris? Give me celsius for both.",
    tools=[weather_tool],
    registry=TOOL_REGISTRY,
)
display(Markdown(answer))
```

- [ ] **Step 3: Commit**

```bash
git add "material/Session 8/notebooks/06_tool_use.ipynb"
git commit -m "session 8: tool use notebook — agentic loop step by step and run_tool_loop helper"
```

---

## Task 4: Built-in tools

**Files:**
- Modify: `material/Session 8/notebooks/06_tool_use.ipynb`

- [ ] **Step 1: Add built-in tools section**

Cell — markdown:
```markdown
## 4. Built-in Tools

OpenAI provides built-in tools you can enable with a single dict — no Python function required. The model calls them server-side and returns the result inline.

The two most useful for teaching:
- `web_search` — live web retrieval
- `code_interpreter` — the model writes and executes Python in a sandbox
```

Cell — markdown:
```markdown
### `web_search`

Just declare `{"type": "web_search"}` in the tools list. No schema needed, no Python function to write.
```

Cell — code:
```python
# Requires OPENAI_API_KEY
# Skip this cell if you do not have live API access.

client = make_openai_client(api_key=require_env("OPENAI_API_KEY"))

web_response = client.responses.create(
    model="gpt-4o-mini",
    tools=[{"type": "web_search"}],
    input="What were the main AI announcements from the last week?",
)

display(Markdown(web_response.output_text))
```

Cell — markdown:
```markdown
### `code_interpreter`

The model writes Python, executes it in a sandboxed environment, and returns the result. Useful for maths, data transformation, or anything a small script can solve.
```

Cell — code:
```python
# Requires OPENAI_API_KEY
# Skip this cell if you do not have live API access.

client = make_openai_client(api_key=require_env("OPENAI_API_KEY"))

code_response = client.responses.create(
    model="gpt-4o-mini",
    tools=[{"type": "code_interpreter", "container": {"type": "auto"}}],
    input=(
        "Calculate the compound interest on $10,000 invested at 7% annual rate "
        "for 20 years. Show the formula and the result."
    ),
)

display(Markdown(code_response.output_text))
```

Cell — markdown:
```markdown
### Key difference from custom tools

| | Custom tool | Built-in tool |
|---|---|---|
| Python function needed? | Yes | No |
| Runs where? | Your machine | OpenAI servers |
| Can access internet? | If your function does | Yes (web_search) |
| Can run code? | If your function does | Yes (code_interpreter) |
```

- [ ] **Step 2: Commit**

```bash
git add "material/Session 8/notebooks/06_tool_use.ipynb"
git commit -m "session 8: tool use notebook — built-in tools (web_search, code_interpreter)"
```

---

## Task 5: Parallel tool calls

**Files:**
- Modify: `material/Session 8/notebooks/06_tool_use.ipynb`

- [ ] **Step 1: Add a second tool and parallel calls section**

Cell — markdown:
```markdown
## 5. Parallel Tool Calls

When multiple tools are registered, the model may call several in a single turn. This is called parallel tool calling and it saves a round-trip for questions that need two independent lookups.
```

Cell — code:
```python
def get_current_date() -> dict:
    """Return today's date — no external API needed."""
    from datetime import date
    today = date.today()
    return {
        "date": today.isoformat(),
        "day_of_week": today.strftime("%A"),
    }


date_tool = {
    "type": "function",
    "name": "get_current_date",
    "description": "Returns today's date and day of the week. Call this when the user asks what day or date it is.",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False,
    },
    "strict": True,
}

# Smoke test
print(get_current_date())
```

Cell — code:
```python
# Requires OPENAI_API_KEY
# Skip this cell if you do not have live API access.

TOOL_REGISTRY_V2 = {
    "get_weather": get_weather,
    "get_current_date": get_current_date,
}

answer = run_tool_loop(
    user_message=(
        "What day is it today, and what is the weather in Melbourne right now in celsius?"
    ),
    tools=[weather_tool, date_tool],
    registry=TOOL_REGISTRY_V2,
)

display(Markdown(answer))
```

Cell — markdown:
```markdown
The model may issue both `get_weather` and `get_current_date` calls in the same response turn. The `run_tool_loop` helper handles this naturally because it loops over all `function_call` items before making the next model call.
```

- [ ] **Step 2: Commit**

```bash
git add "material/Session 8/notebooks/06_tool_use.ipynb"
git commit -m "session 8: tool use notebook — parallel tool calls"
```

---

## Task 6: RAG as a tool call

**Files:**
- Modify: `material/Session 8/notebooks/06_tool_use.ipynb`
- Reference: `material/Session 8/helpers/rag_utils.py` — read to understand `load_and_chunk_pdfs`, `build_faiss_index`, `search_index` signatures

- [ ] **Step 1: Read rag_utils.py to confirm the exact function signatures**

```bash
cat "material/Session 8/helpers/rag_utils.py"
```

Note the exact parameter names for `load_and_chunk_pdfs`, `build_faiss_index`, and `search_index`. Use those exact names in the cells below.

- [ ] **Step 2: Add the RAG-as-tool section**

Cell — markdown:
```markdown
## 6. RAG as a Tool Call

In notebook 04, context is always injected into the prompt — the model never chooses to retrieve. That works but it has two problems:
- Every query pays the embedding + search cost, even when no retrieval is needed
- The model cannot say "I already know this, I do not need to look it up"

Wrapping the FAISS search as a tool lets the model decide when retrieval adds value.
```

Cell — code:
```python
import sys
sys.path.insert(0, str(session8_dir()))

from helpers.rag_utils import load_and_chunk_pdfs, build_faiss_index, search_index

# Build the index once from the sample PDFs
pdf_dir = session8_dir() / "data" / "pdfs"
pdf_paths = list(pdf_dir.glob("*.pdf"))
print(f"PDFs found: {[p.name for p in pdf_paths]}")

chunks = load_and_chunk_pdfs(pdf_paths)
print(f"Chunks created: {len(chunks)}")

faiss_index, chunk_texts = build_faiss_index(chunks)
print("FAISS index ready.")
```

Cell — code:
```python
def search_hr_docs(query: str, top_k: int = 4) -> str:
    """
    Search the HR document knowledge base (FAISS index built above).
    Returns top_k relevant text chunks joined as a single string.
    """
    results = search_index(faiss_index, chunk_texts, query, top_k=top_k)
    return "\n\n---\n\n".join(results)


search_tool = {
    "type": "function",
    "name": "search_hr_docs",
    "description": (
        "Search the HR document knowledge base for information about employee benefits, "
        "health plans, dental coverage, PTO policy, and similar HR topics. "
        "Call this tool when the user asks a question that requires specific policy details."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query derived from the user's question.",
            },
            "top_k": {
                "type": "integer",
                "description": "Number of document chunks to retrieve. Default is 4.",
            },
        },
        "required": ["query"],
        "additionalProperties": False,
    },
    "strict": True,
}

# Smoke test — confirm search works before wiring to the model
snippet = search_hr_docs("dental coverage annual limit")
print(snippet[:300])
```

Cell — code:
```python
# Requires OPENAI_API_KEY
# Skip this cell if you do not have live API access.

TOOL_REGISTRY_RAG = {
    "search_hr_docs": search_hr_docs,
}

# Question that needs retrieval
answer_retrieval = run_tool_loop(
    user_message="What is the annual dental coverage limit in our health plan?",
    tools=[search_tool],
    registry=TOOL_REGISTRY_RAG,
)
display(Markdown("### Answer with retrieval\n" + answer_retrieval))
```

Cell — code:
```python
# Requires OPENAI_API_KEY
# Skip this cell if you do not have live API access.

# Question that does NOT need retrieval — model should answer from general knowledge
answer_no_retrieval = run_tool_loop(
    user_message="What does the acronym RAG stand for?",
    tools=[search_tool],
    registry=TOOL_REGISTRY_RAG,
)
display(Markdown("### Answer without retrieval\n" + answer_no_retrieval))
```

Cell — markdown:
```markdown
Notice that the model calls `search_hr_docs` for the dental question but answers directly for the RAG acronym question. The model reasons about when retrieval is needed.

### Why this matters

| Pattern | Who controls retrieval? | Cost |
|---|---|---|
| Notebook 04 (always inject) | Developer (always) | Always pays embedding + search |
| Tool call (this notebook) | Model (as needed) | Pays only when retrieval helps |

For production RAG apps, combining both patterns is common: use tool calling for the main flow, with a fallback injected context for critical baseline information.
```

- [ ] **Step 3: Add a final recap cell**

Cell — markdown:
```markdown
## Recap

- Tools are JSON schemas that tell the model what functions exist and when to call them.
- The agentic loop has four steps: request → detect → execute → feed back.
- `run_tool_loop` encapsulates the loop for reuse.
- Built-in tools (`web_search`, `code_interpreter`) need no Python function.
- The model handles parallel calls naturally when multiple tools are registered.
- RAG-as-a-tool lets the model decide when to retrieve, reducing unnecessary embedding cost.

**Next:** `06_streamlit_rag_app.py` combines RAG, streaming, and a Streamlit UI into a complete deployable app.
```

- [ ] **Step 4: Run the full notebook to verify**

```bash
cd /c/git/mdsiprojects/anlpaut2026
jupyter nbconvert --to notebook --execute \
  --ExecutePreprocessor.timeout=120 \
  "material/Session 8/notebooks/06_tool_use.ipynb" \
  --output /tmp/06_tool_use_executed.ipynb 2>&1 | tail -10
```

Expected: cells that require API keys execute without error (they make real API calls). Cells guarded with `# Skip this cell if you do not have live API access.` may be skipped manually or via a kernel that skips on error.

- [ ] **Step 5: Commit**

```bash
git add "material/Session 8/notebooks/06_tool_use.ipynb"
git commit -m "session 8: tool use notebook — RAG as a tool call and final recap"
```

---

## Self-Review

### Spec coverage

| Requirement | Task |
|---|---|
| JSON schema anatomy | Task 2 |
| Custom weather tool (no API key) | Task 2 |
| Agentic loop step by step | Task 3 |
| `run_tool_loop` clean helper | Task 3 |
| Built-in `web_search` | Task 4 |
| Built-in `code_interpreter` | Task 4 |
| Parallel tool calls | Task 5 |
| RAG as a tool call | Task 6 |
| Model choosing whether to retrieve | Task 6 |
| Notebook style matches existing notebooks | Tasks 1–6 |
| No Azure dependency | All tasks |

### Placeholder scan

No TBD, TODO, or "similar to" references. All code blocks are complete and self-contained.

### Type consistency

- `run_tool_loop` defined in Task 3 — `tools: list`, `registry: dict`, returns `str`. Used unchanged in Tasks 5 and 6.
- `TOOL_REGISTRY` (Task 3) extended to `TOOL_REGISTRY_V2` (Task 5) and `TOOL_REGISTRY_RAG` (Task 6) — separate dicts, no mutation of shared state.
- `weather_tool`, `date_tool`, `search_tool` — all follow the same schema shape with `type`, `name`, `description`, `parameters`, `strict`.
- `search_hr_docs` signature: `(query: str, top_k: int = 4) -> str` — matches the tool schema's `required: ["query"]` with `top_k` optional.
