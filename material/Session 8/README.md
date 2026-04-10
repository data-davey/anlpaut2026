# Session 8 — Building LLM Apps with APIs and RAG

**Date:** 13 April 2026

## Topics

- LLM API access with the OpenAI SDK
- Chat Completions vs Responses API
- streaming responses for interactive apps
- Provider compatibility: OpenAI, GitHub Models, and Ollama
- Retrieval-Augmented Generation (RAG)
- Vector stores: FAISS and OpenAI Vector Store
- simple UI demos with Gradio and Streamlit

## Learning Objectives

By the end of this session, students should be able to:

- call language models from Python using the OpenAI SDK
- explain the difference between Chat Completions and the Responses API
- implement streaming output with the Responses API
- understand how OpenAI-compatible endpoints make GitHub Models and Ollama easy to reference
- explain why PDF documents need parsing and chunking before retrieval
- build a minimal FAISS-based RAG pipeline over handbook and policy PDFs
- compare answers with and without retrieval grounding
- wrap model calls in a small Gradio demo
- build a streaming Streamlit RAG app

## Folder Structure

```text
material/Session 8/
├── README.md
├── data/
│   ├── README.md
│   ├── images/
│   ├── questions.json
│   └── pdfs/
├── helpers/
│   ├── pdf_utils.py
│   └── rag_utils.py
├── notebooks/
│   ├── 01_llm_api_access.ipynb
│   ├── 02_embeddings_and_similarity.ipynb
│   ├── 03_streaming_responses.ipynb
│   ├── 04_rag_with_pdfs_and_faiss.ipynb
│   ├── 05_gradio_chat_demo.ipynb
│   └── 06_tool_use.ipynb
├── 06_streamlit_rag_app.py
├── .streamlit/
│   └── secrets.toml.example
├── scratchpad.md
├── topics.md
└── vector_similarity.md
```

## Notebook Order

### `01_llm_api_access.ipynb`

This notebook introduces:

- OpenAI SDK setup
- Chat Completions
- Responses API
- structured output
- image and multimodal input
- provider swap patterns for GitHub Models and Ollama
- a short Claude comparison

### `02_embeddings_and_similarity.ipynb`

This notebook introduces:

- what embeddings are and why they are useful
- OpenAI embedding creation with the SDK
- cosine similarity for semantic comparison
- a tiny semantic search example
- the retrieval idea that later becomes RAG

### `03_streaming_responses.ipynb`

This notebook introduces:

- why streaming matters in user-facing apps
- how to iterate over Response API events
- how to accumulate streamed text in Python
- how the same pattern connects naturally to UI tools later in the session

### `04_rag_with_pdfs_and_faiss.ipynb`

This notebook builds a minimal RAG pipeline:

- parse PDF documents
- inspect extracted text
- chunk the text with overlap
- create embeddings
- build a FAISS index
- retrieve relevant chunks
- compare no-RAG vs RAG answers

### `05_gradio_chat_demo.ipynb`

This notebook introduces:

- a minimal chat UI using Gradio
- how to connect streaming model output to a lightweight interface
- how quickly an API call can become an interactive demo

### `06_tool_use.ipynb`

This notebook covers tool use and function calling:

- anatomy of a tool definition (JSON schema)
- a custom weather tool — the classic first example
- the 4-step agentic loop: request → detect → execute → feed back
- a `run_tool_loop` helper for multi-turn agentic conversations
- built-in tools: `web_search` and `code_interpreter`
- parallel tool calls — two tools in one turn
- RAG as a tool call — the FAISS index wrapped as a function the model can invoke

### `06_streamlit_rag_app.py`

This is the main app build for Session 8:

- a streaming chat interface in Streamlit
- retrieval over the Session 8 PDF corpus
- grounded answers with visible sources
- editable system prompt in the sidebar with a reset-to-default button
- a stronger end-to-end example than the Gradio demo

## Prerequisites

Activate the course virtual environment from the repo root:

```bash
source venv/bin/activate
```

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

The session is OpenAI SDK-first, but references multiple providers.

Core:

- `OPENAI_API_KEY`
- `OPENAI_ORG_ID`
- `OPENAI_PROJECT_ID`

Optional:

- `GITHUB_TOKEN` for GitHub Models
- `ANTHROPIC_API_KEY` for Claude examples
- Ollama running locally at `http://localhost:11434/v1`

## Streamlit Secrets (for deployment)

A secrets template is provided at `.streamlit/secrets.toml.example`. To use it locally or deploy to Streamlit Cloud:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# fill in your values — secrets.toml is gitignored
```

For Streamlit Cloud, paste the contents of the template into **App Settings → Secrets**.

## Running the Streamlit App

From the repo root:

```bash
streamlit run "material/Session 8/06_streamlit_rag_app.py"
```

## Dataset Notes

The PDF corpus uses generic handbook and benefits documents because they produce clearer retrieval-style questions than course notes.

See [README.md](/C:/git/mdsiprojects/anlpaut2026/material/Session%208/data/README.md) inside the `data/` folder for details.

## Important Note About `.old`

`material/Session 8/.old/` is archival reference material from earlier teaching material. It is not part of the new Session 8 deliverables and should not be included in future commits unless explicitly requested.

## Related References

- [topics.md](/C:/git/mdsiprojects/anlpaut2026/material/Session%208/topics.md)
- [scratchpad.md](/C:/git/mdsiprojects/anlpaut2026/material/Session%208/scratchpad.md)
- [vector_similarity.md](/C:/git/mdsiprojects/anlpaut2026/material/Session%208/vector_similarity.md)
