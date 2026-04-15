# Session 9 — AI Agents

**Date:** 20 April 2026

## Topics

- Agentic RAG — bridge from Session 8
- AI Agents — the augmented LLM, workflows vs. agents
- Workflow patterns — prompt chaining, routing, parallelization, evaluator-optimizer
- Model Context Protocol (MCP) — universal wiring for agent tools
- Multi-Agent Frameworks — OpenAI Agents SDK (hands-on); LangGraph/CrewAI/MAF (conceptual)
- Industry state 2026 — production examples, compound accuracy problem, failure modes

## Reference Reading

- [Building Effective Agents — Anthropic](https://www.anthropic.com/engineering/building-effective-agents)
- [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/)
- [A Practical Guide to Building Agents — OpenAI](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)

## Notebooks

### `notebooks/01_agents_concepts.ipynb`

Covers concepts with working code examples:
1. Agentic RAG — iterative retrieve → generate → check → rewrite loop over a FAISS index
2. LLM vs. Agent — same task, static call vs. agent with tools
3. Workflow patterns — prompt chaining, routing, parallelization, evaluator-optimizer
4. MCP — concept, the M×N problem, and a minimal FastMCP server

### `notebooks/02_agent_with_tools.ipynb`

Hands-on with the OpenAI Agents SDK:
1. Hello Agent — `Agent`, `Runner.run_sync()`, basic loop
2. Tool-using agent — `@function_tool`: calculator, date, FAISS search
3. True agentic RAG — LLM controls its own retrieval loop
4. Trace inspection — `result.new_items` + OpenAI Platform tracing
5. Orchestrator-workers — `agent.as_tool()` for specialist delegation
6. Handoffs — `handoff(agent)` for permanent control transfer
7. Reflection exercise — why tool descriptions matter

### `notebooks/03_beyond_basics.ipynb` *(optional — technical depth)*

SDK patterns for real-world implementations:
1. Multi-turn conversations — `to_input_list()`, streaming REPL
2. State management — `context=` parameter, `RunContextWrapper`
3. Lifecycle hooks — minimal `RunHooks` with `on_agent_start` / `on_agent_end`
4. Deterministic vs stochastic orchestration — evaluator-optimizer both ways with the SDK
5. SDK reference — `handoff_description`, `tool_use_behavior`, `final_output_as()`, `ModelSettings`

### `notebooks/04_agent_gradio_app.ipynb` *(optional — capstone)*

Agent-powered Gradio app with streaming and human-in-the-loop:
1. Agent with safe tools + high-stakes `send_course_announcement` requiring approval
2. Gradio `gr.Blocks` layout — chatbot, input, conditional HITL approval panel
3. Streaming responses via `Runner.run_streamed()` + `ResponseTextDeltaEvent`
4. HITL checkpoint pattern — agent calls `request_approval`, UI shows Approve/Reject
5. Multi-turn continuation via `to_input_list()` across approval cycles

## Setup

Activate the course virtual environment and install dependencies:

```bash
source venv/bin/activate       # macOS/Linux
# or
.\venv\Scripts\Activate.ps1    # Windows PowerShell

pip install -r requirements.txt
```

Required environment variables (in `.env` or shell):

```
OPENAI_API_KEY=...
OPENAI_ORG_ID=...
OPENAI_PROJECT_ID=...
```

## Folder Structure

```
material/Session 9/
├── README.md
├── topics.md               — full topic notes with 2026 industry research
├── scratchpad.md           — planning notes (gitignored)
├── responses api and vector store.md  — §4: OpenAI Agents SDK reference
├── notebooks/
│   ├── 01_agents_concepts.ipynb       — core session (required)
│   ├── 02_agent_with_tools.ipynb      — core session (required)
│   ├── 03_beyond_basics.ipynb         — optional: SDK depth
│   └── 04_agent_gradio_app.ipynb      — optional: Gradio + HITL capstone
└── .old/                   — reference material from previous term
```
