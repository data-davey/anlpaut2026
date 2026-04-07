# Session 8 — Building LLM Apps with APIs and RAG

**Date:** 13 April 2026

## Topics

- LLM API access with the OpenAI SDK
- Chat Completions vs Responses API
- Provider compatibility: OpenAI, GitHub Models, and Ollama
- Retrieval-Augmented Generation (RAG)
- Vector stores: FAISS and OpenAI Vector Store

## Learning Objectives

By the end of this session, students should be able to:

- call language models from Python using the OpenAI SDK
- explain the difference between Chat Completions and the Responses API
- understand how OpenAI-compatible endpoints make GitHub Models and Ollama easy to reference
- explain why PDF documents need parsing and chunking before retrieval
- build a minimal FAISS-based RAG pipeline over handbook and policy PDFs
- compare answers with and without retrieval grounding

## Folder Structure

```text
material/Session 8/
├── README.md
├── data/
│   ├── README.md
│   ├── questions.json
│   └── pdfs/
├── helpers/
│   ├── pdf_utils.py
│   └── rag_utils.py
├── notebooks/
│   ├── 01_llm_api_access.ipynb
│   └── 02_rag_with_pdfs_and_faiss.ipynb
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
- provider swap patterns for GitHub Models and Ollama
- a short Claude comparison

### `02_rag_with_pdfs_and_faiss.ipynb`

This notebook builds a minimal RAG pipeline:

- parse PDF documents
- inspect extracted text
- chunk the text with overlap
- create embeddings
- build a FAISS index
- retrieve relevant chunks
- compare no-RAG vs RAG answers

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

Optional:

- `GITHUB_TOKEN` for GitHub Models
- `ANTHROPIC_API_KEY` for Claude examples
- Ollama running locally at `http://localhost:11434/v1`

## Dataset Notes

The PDF corpus uses generic handbook and benefits documents because they produce clearer retrieval-style questions than course notes.

See [README.md](/C:/git/mdsiprojects/anlpaut2026/material/Session%208/data/README.md) inside the `data/` folder for details.

## Important Note About `.old`

`material/Session 8/.old/` is archival reference material from earlier teaching material. It is not part of the new Session 8 deliverables and should not be included in future commits unless explicitly requested.

## Related References

- [topics.md](/C:/git/mdsiprojects/anlpaut2026/material/Session%208/topics.md)
- [scratchpad.md](/C:/git/mdsiprojects/anlpaut2026/material/Session%208/scratchpad.md)
- [vector_similarity.md](/C:/git/mdsiprojects/anlpaut2026/material/Session%208/vector_similarity.md)

