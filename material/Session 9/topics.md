Week 10
20 April 2026
Session 9

topics:
- Agentic RAG (bridge from Session 8)
- AI Agents (augmented LLM, workflow patterns — Anthropic framework)
- Multi-Agent Frameworks (OpenAI Agents SDK hands-on; LangGraph/CrewAI conceptually)
- Hands-on: Build a simple agent with tools

## Notes

- Open with Agentic RAG recap — positions agents as a natural extension of the RAG pipeline from Session 8
- Core reference: Anthropic "Building Effective Agents" — https://www.anthropic.com/engineering/building-effective-agents
- `responses api and vector store.md` in this folder is split-use: §1–3 and §5–8 (Responses API, Vector Stores) belong to Session 8; §4 (OpenAI Agents SDK) belongs here
- Multi-agent frameworks: cover OpenAI Agents SDK hands-on; describe LangGraph and CrewAI conceptually so students can evaluate them independently

## Workflow Patterns (from Anthropic article)

| Pattern | Description |
|---|---|
| Augmented LLM | LLM extended with tools, retrieval, and memory — the core building block |
| Prompt chaining | Sequential LLM calls; output of one is input of next |
| Routing | Classify input and direct to a specialised sub-task |
| Parallelization | Run independent sub-tasks concurrently |
| Orchestrator-workers | Central orchestrator delegates to worker agents |
| Evaluator-optimizer | One agent generates, another evaluates and requests improvement |

## Planned Notebooks

- `notebooks/01_agents_concepts.ipynb` — Agentic RAG recap; implement each Anthropic workflow pattern as a short code example
- `notebooks/02_agent_with_tools.ipynb` — OpenAI Agents SDK: build an agent with 2–3 tools; orchestrator-workers demo; reflection on tool description quality

## References

- Anthropic. "Building Effective Agents." https://www.anthropic.com/engineering/building-effective-agents
- Asai, A. et al. (2023). "Self-RAG." ICLR 2024.
- Trivedi, H. et al. (2023). "IRCoT." ACL.
- `responses api and vector store.md` §4 — OpenAI Agents SDK code reference

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
![High-level flow of a coding agent](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F4b9a1f4eb63d5962a6e1746ac26bbc857cf3474f-2400x1666.png&w=3840&q=75)
_Figure: High-level flow of a coding agent_

# Article summary (Building effective agents)
- Distinguishes workflows (predefined tool/LLM paths) from agents (model-directed tool use).
- Recommends starting simple, adding agentic complexity only when it improves outcomes and justifies latency/cost.
- Advises minimal abstraction: frameworks help but can hide prompts and invite unnecessary complexity.
- Defines the augmented LLM (tools, retrieval, memory) as the core building block.
- Describes common workflow patterns: prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer.
- Positions agents for open-ended tasks needing flexible steps, with strong tool design, guardrails, and sandbox testing.
- Emphasizes transparent planning, clear agent-computer interfaces, and iterative evaluation.
- Highlights practical use cases in customer support and coding agents (testable feedback loops).
