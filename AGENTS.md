# ANLP AUT 2026 — Codex Instructions

## Purpose

This repository is instructional for students studying **Advanced Natural Language Processing (ANLP)**, covering topics such as:
- Traditional and modern NLP techniques
- Large Language Models (LLMs)
- AI Agents and agentic workflows
- Other advanced NLP concepts and applications

All code and notebooks are written to be clear, well-commented, and educational.

---

## Language

This is a **Python-only** repository. No other programming languages are to be used.

---

## Python Environment

Always use the virtual environment created for this course. Activate it before running any code:

```bash
source venv/bin/activate
```

---

## Dependencies & Packages

- Any new package introduced in code **must be added to `requirements.txt`** immediately.
- Keep `requirements.txt` up to date — it is the single source of truth for project dependencies.
- Install packages within the active venv only:

```bash
pip install <package>
pip freeze > requirements.txt  # or manually add the package with its version
```

---

## Notebooks

- Use **Jupyter notebooks** (`.ipynb`) when appropriate, especially for:
  - Explaining concepts step by step
  - Demonstrating NLP techniques interactively
  - Visualizing data, model outputs, or results
  - Creating instructional walkthroughs for students
- Notebooks should be well-structured with markdown cells that explain each step before the code that implements it.
- Pure utility/helper code that is reused across notebooks should live in `.py` modules.

---

## Sessions & Branch Workflow

Each session has its own **folder under `material/`** and its own **git branch**. All work for a session must be done in the corresponding branch and folder.

| Session | Date | Branch | Folder | Topics |
|---------|------|--------|--------|--------|
| Session 6 | 23 Mar 2026 | `session-6` | `material/Session 6/` | Transformers, BERT, Language Models, LLM intro, Generative AI tools |
| Session 7 | 30 Mar 2026 | `session-7` | `material/Session 7/` | LLM deep dive, prompting, LLM challenges & risks, LLM evaluation |
| Session 8 | 13 Apr 2026 | `session-8` | `material/Session 8/` | Building LLM apps with OpenAI, Codex & Ollama APIs, RAG pattern |
| Session 9 | 20 Apr 2026 | `session-9` | `material/Session 9/` | AI Agents, multi-agent frameworks, hands-on exercises |
| Session 10 | TBD | `session-10` | `material/Session 10/` | Ethics in NLP, NLP for social good, AI-augmented thinking, AI security (guest speaker) |

### Branch workflow

```bash
# Start work on a session
git checkout -b session-<N>

# Work inside the session folder only
cd material/Session <N>/

# Commit and push
git add .
git commit -m "session <N>: <description>"
git push -u origin session-<N>
```

- Never commit session work directly to `main`.
- Open a PR from the session branch into `main` when the session material is complete.

### Concept folders

Occasionally, standalone folders may be created under `material/` outside of sessions to explore or explain specific concepts in more depth. These are not tied to a session and do not follow the session naming convention. They should still have their own branch (e.g. `concept-<topic>`) and a `README.md` describing the concept covered.

---

## Code Style & Instructional Quality

- Write code that is **readable and educational** — students will learn from it.
- Add comments where logic is not immediately obvious.
- Prefer clarity over cleverness.
- Each session folder must contain a `README.md` explaining what the session covers and how to run the code/notebooks.
