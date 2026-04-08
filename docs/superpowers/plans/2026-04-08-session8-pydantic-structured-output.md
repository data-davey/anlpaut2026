# Session 8 Pydantic Structured Output Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add two Pydantic-based structured output examples to the Session 8 API notebook and explain why they are useful alongside the existing JSON Schema example.

**Architecture:** Keep the current structured-output section intact, then layer two additional examples directly after it. The first uses `responses.parse(...)` for typed return values, and the second uses `responses.create(...)` plus Pydantic validation to preserve access to the raw response object while still enforcing a schema in Python.

**Tech Stack:** Jupyter notebook JSON, OpenAI Python SDK, Pydantic v2

---

### Task 1: Update dependencies

**Files:**
- Modify: `requirements.txt`

- [ ] Add `pydantic` as a direct dependency because the notebook will import it explicitly.

### Task 2: Extend the notebook imports and commentary

**Files:**
- Modify: `material/Session 8/notebooks/01_llm_api_access.ipynb`

- [ ] Add the required Pydantic imports to the main setup cell.
- [ ] Add a markdown explanation of why Python applications often prefer typed validated objects over raw JSON text.

### Task 3: Add the two Pydantic examples

**Files:**
- Modify: `material/Session 8/notebooks/01_llm_api_access.ipynb`

- [ ] Add a `responses.parse(...)` example that returns a validated Pydantic object and displays its fields.
- [ ] Add a `responses.create(...)` example that uses a Pydantic-generated JSON schema and then validates `output_text` with `model_validate_json(...)`.
- [ ] Add short commentary describing when each pattern is the better choice.

### Task 4: Verify the notebook

**Files:**
- Test: `material/Session 8/notebooks/01_llm_api_access.ipynb`

- [ ] Parse the notebook as JSON to confirm the edit is structurally valid.
- [ ] Confirm `pydantic` is present in `requirements.txt`.
