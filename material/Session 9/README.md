# Session 9 — AI Agents

**Date:** 20 April 2026

## Topics Covered

- AI Agents — what they are and how they differ from standard LLM workflows
- Multi-agent frameworks — orchestrating multiple agents to solve complex tasks
- Hands-on exercises — building and running agents using popular frameworks

## Key Concepts

| Concept | Description |
|---------|-------------|
| Augmented LLM | An LLM extended with tools, retrieval, and memory as the core agent building block |
| Workflows | Predefined sequences of LLM/tool calls with fixed paths |
| Agents | Model-directed tool use where the LLM decides the next action |
| Prompt chaining | Breaking a task into sequential LLM calls, passing outputs as inputs |
| Routing | Classifying inputs and directing them to specialised sub-tasks |
| Parallelization | Running independent sub-tasks concurrently to reduce latency |
| Orchestrator-workers | A central orchestrator delegates sub-tasks to worker agents |
| Evaluator-optimizer | One agent generates output, another evaluates and requests improvements |

## Reference Reading

- [Building Effective Agents — Anthropic](https://www.anthropic.com/engineering/building-effective-agents)

## How to Run

1. Activate the virtual environment:

```bash
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Open the notebooks in this folder with Jupyter:

```bash
jupyter notebook
```

## Folder Structure

```
session-9-ai-agents/
├── README.md          # This file
└── topics.md          # Session topic notes and reference material
```
