Week 10
20 April 2026
Session 9

topics:
- Agentic RAG (bridge from Session 8)
- AI Agents — concepts, the augmented LLM, workflows vs. agents (Anthropic framework)
- Agentic workflow patterns (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer)
- Model Context Protocol (MCP) — what it is, why it matters, current industry adoption
- Multi-Agent Frameworks — OpenAI Agents SDK (hands-on); LangGraph, CrewAI, Microsoft Agent Framework (conceptual positioning)
- Industry state — production agents in 2026, failure modes, compound accuracy problem
- Hands-on: Build an agent with tools using OpenAI Agents SDK

## Notes

- Open with Agentic RAG — positions agents as a natural extension of the RAG pipeline from Session 8
- Core conceptual reference: Anthropic "Building Effective Agents" — https://www.anthropic.com/engineering/building-effective-agents
- MCP is a must-cover topic: introduced by Anthropic Nov 2024, donated to Linux Foundation (AAIF) Apr 2026, 97M monthly downloads, 10,000+ public MCP servers; industry has effectively adopted it as the standard tool-connectivity layer
- OpenAI Agents SDK for hands-on: lightweight, code-first, teaches the concepts without over-abstracting; formerly known as Swarm (renamed March 2025)
- FAISS reused from Session 8 if RAG pattern needed in hands-on
- `responses api and vector store.md` §4 (OpenAI Agent SDK) belongs here; §1–3 and §5–8 belong to Session 8
- AutoGen is now in maintenance mode — migrate references to Microsoft Agent Framework 1.0 (GA April 2026)

## Planned Notebooks

refer to [README.md](/material/Session%209/README.md)

## Industry State (2026) — Lecture Context

### The Shift: From Demos to Production

The period from late 2024 to early 2026 marks the most significant transition in applied AI: agents moved from research curiosity to shipping infrastructure.

- Gartner: 40% of enterprise applications will include task-specific AI agents by end of 2026 (up from <5% in 2025)
- Global agentic AI market: $9.14B in 2026, projected to $139B by 2034

### Key Milestones (late 2024 → April 2026)

| Date | Milestone |
|------|-----------|
| Nov 2024 | Anthropic introduces **Model Context Protocol (MCP)** as open standard |
| Jan 2025 | **OpenAI Operator** launches: browser-based autonomous agent |
| Mar 2025 | **OpenAI Agents SDK** released (successor to Swarm), alongside Responses API |
| Apr 2025 | **Google Agent2Agent (A2A)** protocol announced; 50+ partners |
| Jul 2025 | Operator integrated into **ChatGPT Agent Mode** |
| Oct 2025 | Microsoft merges AutoGen + Semantic Kernel → **Microsoft Agent Framework** |
| Feb 2026 | Claude and Codex available as agents in GitHub Copilot for all plan tiers |
| Mar 2026 | Anthropic ships production-ready **desktop agent** (Mac); Perplexity Deep Research generates PPTX/spreadsheets |
| Apr 2026 | Anthropic launches **Claude Managed Agents**; MCP donated to Agentic AI Foundation (Linux Foundation) |

### Notable Production Examples

**GitHub Copilot Workspace (coding agent)**: Developer opens an issue; the agent proposes a plan, writes code, runs tests, opens a PR. Multi-model: Claude for reasoning, Codex for code synthesis. Most widely deployed coding agent by user count.

**Salesforce Agentforce 2dx**: Handles order status, billing disputes, returns, and scheduling autonomously with tool-call access to CRM, payment systems, and scheduling APIs. Architecture: orchestrator LLM + worker tool calls to backend systems.

**OpenAI / Perplexity Deep Research**: Multi-step autonomous research — browses dozens of sources, synthesises, returns a structured report (or deliverable). Canonical example of the "single turn for the user, 20–50 operations internally" pattern.

### Failure Modes — What Practitioners Talk About

**Compound accuracy problem**: A 10-step workflow where each step is 85% accurate succeeds only ~20% of the time (0.85^10 ≈ 0.20). Even best models complete only ~24% of real-world tasks on first attempt (APEX-Agents 2026 benchmark).

**Hallucination propagation**: Unlike single-shot hallucination, agents act on their own hallucinated outputs — cascading failures across downstream tool calls.

**Context drift**: Early objectives become diluted as the context window fills over long-running tasks.

**Tool misuse**: Agents call tools in wrong order, wrong parameters, without checking pre-conditions. Quality of tool *descriptions* (not just implementation) is a major reliability determinant.

### The Three Emerging Standard Protocols

| Protocol | Origin | Purpose |
|----------|--------|---------|
| **MCP** | Anthropic → Linux Foundation | Tool/context connectivity (the "USB-C for LLMs") |
| **A2A** | Google → Linux Foundation | Agent-to-agent communication and discovery |
| **AG-UI** | Community | Human-in-the-loop front-end streaming interface |

### Dominant Production Patterns

- **Orchestrator-workers**: default architecture for complex tasks; each sub-agent operates in a smaller, better-defined context
- **Specialised routing**: classify intent, delegate to specialist (billing, support, returns) — dominant in customer service
- **Human-in-the-loop (HITL)**: remains essential for high-stakes decisions; the 2026 practitioner consensus is that HITL is correct system design, not a failure
- **Evaluator-optimizer**: one agent generates, another evaluates and requests revision — common in content pipelines and coding agent loops

## Framework Landscape (2026)

| Framework | Style | Best For | Notes |
|-----------|-------|----------|-------|
| **OpenAI Agents SDK** | Agents + handoffs; Python-first | Fast prototyping with OpenAI models | Recommended for this course |
| **LangGraph** | Graph / state machine (nodes + edges + checkpointing) | Complex conditional workflows; regulated environments | Used by Klarna, Uber, J.P. Morgan, LinkedIn |
| **CrewAI** | Role-based "crews"; declarative task assignment | Structured multi-agent teamwork | ~40% faster to set up than LangGraph for standard workflows |
| **Microsoft Agent Framework 1.0** | AutoGen + Semantic Kernel; async event-driven | .NET/Python enterprise; Azure-native | GA April 2026; AutoGen now in maintenance mode |

## OpenAI Agents SDK — Core Primitives

| Primitive | Description |
|-----------|-------------|
| `Agent` | An LLM with instructions, tools, and optional output schema |
| `Runner` | Executes an agent and manages the agentic loop |
| `Tools` | Python functions decorated as tools; agent decides when to call them |
| `Handoffs` | One-way delegation — agent transfers control to another agent |
| `Agents as Tools` | An agent called *as a tool* by another agent; caller retains control |
| `Guardrails` | Input/output validators running in parallel with agent execution |
| `Tracing` | Built-in; captures LLM calls, tool calls, handoffs, guardrail events |

### Known Limitations (Inherited from Swarm)

- Stateless architecture: no built-in persistent memory; context must be re-injected each turn
- Handoff stickiness: agents can get stuck in a handoff loop if not carefully designed
- Model lock-in: optimised for OpenAI models; switching providers requires work
- Guardrail reliability: probabilistic, not guaranteed

## Model Context Protocol (MCP)

### What It Is

MCP is an open standard (JSON-RPC-based) defining a universal interface so AI models (clients) can connect to data sources and tools (servers). Analogy: **"USB-C for language models"** — one standard plug for any context source.

### The Problem It Solves

Before MCP: M applications × N tools = M×N custom integrations. MCP collapses this to M+N — each application implements the client once, each tool implements the server once.

### Adoption (April 2026)

- 97 million monthly SDK downloads
- 10,000+ active public MCP servers
- Supported by: ChatGPT, Claude, Cursor, GitHub Copilot, VS Code, Replit, AWS, Google Cloud, Azure
- Donated to Agentic AI Foundation (Linux Foundation, April 2026) — co-founders: Anthropic, Block, OpenAI; supporters: Google, Microsoft, AWS

### For Students

MCP is increasingly the standard wiring for production agents. Understanding it is analogous to understanding REST for web APIs — any agent that needs access to external tools will likely integrate via MCP. A student who can define and serve an MCP tool can plug it into Claude, ChatGPT, Cursor, and VS Code with the same implementation.

## Workflow Patterns (from Anthropic article)

| Pattern | Description |
|---|---|
| Augmented LLM | LLM extended with tools, retrieval, and memory — the core building block |
| Prompt chaining | Sequential LLM calls; output of one is input of next |
| Routing | Classify input and direct to a specialised sub-task |
| Parallelization | Run independent sub-tasks concurrently |
| Orchestrator-workers | Central orchestrator delegates to worker agents |
| Evaluator-optimizer | One agent generates, another evaluates and requests improvement |

## References

- Anthropic. "Building Effective Agents." https://www.anthropic.com/engineering/building-effective-agents
- OpenAI Agents SDK docs. https://openai.github.io/openai-agents-python/
- OpenAI. "A Practical Guide to Building Agents." https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
- Anthropic. "Donating MCP and Establishing the Agentic AI Foundation." https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation
- Model Context Protocol. https://en.wikipedia.org/wiki/Model_Context_Protocol
- Google. "Agent2Agent Protocol." https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/
- Asai, A. et al. (2023). "Self-RAG." ICLR 2024.
- Trivedi, H. et al. (2023). "IRCoT." ACL.
- `responses api and vector store.md` §4 — OpenAI Agents SDK code reference
- Session 8 FAISS notebooks — reused for Agentic RAG hands-on

# Article images
![The augmented LLM](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2Fd3083d3f40bb2b6f477901cc9a240738d3dd1371-2401x1000.png&w=3840&q=75)
_Figure: The augmented LLM_
![Prompt chaining workflow](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F7418719e3dab222dccb379b8879e1dc08ad34c78-2401x1000.png&w=3840&q=75)
_Figure: Prompt chaining workflow_
![Routing workflow](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F5c0c0e9fe4def0b584c04d37849941da55e5e71c-2401x1000.png&w=3840&q=75)
_Figure: Routing workflow_
![Parallelization workflow](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F406bb032ca007fd1624f261af717d70e6ca86286-2401x1000.png&w=3840&q=75)
_Figure: Parallelization workflow_
![Orchestrator-workers workflow](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F8985fc683fae4780fb34eab1365ab78c7e51bc8e-2401x1000.png&w=3840&q=75)
_Figure: Orchestrator-workers workflow_
![Evaluator-optimizer workflow](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F14f51e6406ccb29e695da48b17017e899a6119c7-2401x1000.png&w=3840&q=75)
_Figure: Evaluator-optimizer workflow_
![Autonomous agent](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F58d9f10c985c4eb5d53798dea315f7bb5ab6249e-2401x1000.png&w=3840&q=75)
_Figure: Autonomous agent_

# Article summary (Building effective agents)
- Distinguishes workflows (predefined tool/LLM paths) from agents (model-directed tool use).
- Recommends starting simple, adding agentic complexity only when it improves outcomes and justifies latency/cost.
- Advises minimal abstraction: frameworks help but can hide prompts and invite unnecessary complexity.
- Defines the augmented LLM (tools, retrieval, memory) as the core building block.
- Describes common workflow patterns: prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer.
- Positions agents for open-ended tasks needing flexible steps, with strong tool design, guardrails, and sandbox testing.
- Emphasizes transparent planning, clear agent-computer interfaces, and iterative evaluation.
- Highlights practical use cases in customer support and coding agents (testable feedback loops).
