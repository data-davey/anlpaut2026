# Session 8 Streaming Provider Examples Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend the Session 8 streaming notebook with provider-specific streaming examples for Ollama and GitHub Models.

**Architecture:** Keep the existing OpenAI Responses API examples as the main path, then add one short Ollama subsection using the OpenAI-compatible Responses API and one short GitHub Models subsection using streaming chat completions. The notebook should make the API difference explicit in markdown and code comments.

**Tech Stack:** Jupyter notebooks, OpenAI Python SDK, Ollama OpenAI-compatible endpoint, GitHub Models inference endpoint

---

### Task 1: Extend the streaming notebook

**Files:**
- Modify: `material/Session 8/notebooks/03_streaming_responses.ipynb`

- [ ] Add provider-specific setup values needed for GitHub Models and optional Ollama configuration.
- [ ] Add an `## Streaming with Ollama` subsection using `client.responses.create(..., stream=True)`.
- [ ] Add an `## Streaming with GitHub Models` subsection using `client.chat.completions.create(..., stream=True)`.
- [ ] Add short commentary explaining why the two provider examples do not use the same API surface.

### Task 2: Verify notebook integrity

**Files:**
- Test: `material/Session 8/notebooks/03_streaming_responses.ipynb`

- [ ] Parse the edited notebook as JSON.
- [ ] Confirm `.old` remains untouched.
