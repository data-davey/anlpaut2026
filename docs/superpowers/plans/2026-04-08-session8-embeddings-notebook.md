# Session 8 Embeddings Notebook Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a dedicated embeddings notebook to Session 8 and renumber the remaining notebooks and app so embeddings sit between API access and the rest of the application flow.

**Architecture:** Create a compact OpenAI-first embeddings notebook that teaches embedding creation, cosine similarity, and a tiny semantic search example. Then renumber the downstream Session 8 materials so the flow becomes API access, embeddings, streaming, RAG, Gradio, and Streamlit, with README references updated to match.

**Tech Stack:** Jupyter notebooks, OpenAI Python SDK, NumPy, Markdown documentation

---

### Task 1: Add the embeddings notebook

**Files:**
- Create: `material/Session 8/notebooks/02_embeddings_and_similarity.ipynb`

- [ ] Add a short introduction and learning goals for embeddings.
- [ ] Add setup cells using the existing OpenAI env pattern with org/project IDs.
- [ ] Add a simple `client.embeddings.create(...)` example for a small list of texts.
- [ ] Add cosine similarity helpers and examples contrasting similar and dissimilar pairs.
- [ ] Add a tiny semantic search example over a short in-notebook list of texts.
- [ ] Add a bridge markdown cell that connects embeddings to the later RAG notebook.

### Task 2: Renumber the Session 8 flow

**Files:**
- Rename: `material/Session 8/notebooks/02_streaming_responses.ipynb` -> `material/Session 8/notebooks/03_streaming_responses.ipynb`
- Rename: `material/Session 8/notebooks/03_rag_with_pdfs_and_faiss.ipynb` -> `material/Session 8/notebooks/04_rag_with_pdfs_and_faiss.ipynb`
- Rename: `material/Session 8/notebooks/04_gradio_chat_demo.ipynb` -> `material/Session 8/notebooks/05_gradio_chat_demo.ipynb`
- Rename: `material/Session 8/05_streamlit_rag_app.py` -> `material/Session 8/06_streamlit_rag_app.py`

- [ ] Rename the downstream files to preserve the teaching order.
- [ ] Confirm no code inside the renamed files hardcodes the old numeric names.

### Task 3: Update Session 8 documentation

**Files:**
- Modify: `material/Session 8/README.md`

- [ ] Update the folder tree to show the new notebook and renumbered files.
- [ ] Update the notebook-order descriptions to include embeddings explicitly.
- [ ] Update the Streamlit app reference to the new filename.

### Task 4: Verify the renamed notebook set

**Files:**
- Test: `material/Session 8/notebooks/01_llm_api_access.ipynb`
- Test: `material/Session 8/notebooks/02_embeddings_and_similarity.ipynb`
- Test: `material/Session 8/notebooks/03_streaming_responses.ipynb`
- Test: `material/Session 8/notebooks/04_rag_with_pdfs_and_faiss.ipynb`
- Test: `material/Session 8/notebooks/05_gradio_chat_demo.ipynb`
- Test: `material/Session 8/06_streamlit_rag_app.py`

- [ ] Parse each edited notebook as JSON.
- [ ] Compile the renamed Streamlit app with `py_compile`.
- [ ] Confirm `material/Session 8/.old/` remains untouched.
