# Session 8 Materials Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build student-facing Session 8 materials that teach OpenAI SDK-based LLM app development, provider compatibility patterns, and a minimal PDF-based RAG pipeline with chunking and FAISS.

**Architecture:** Session 8 should have one coherent teaching arc: first learn the OpenAI SDK and compare Chat Completions vs Responses API, then apply that knowledge in a minimal RAG notebook over generic handbook/policy PDFs. Archived `.old` materials are reference-only inputs for design and selective dataset reuse, not sources to copy into new commits.

**Tech Stack:** Python, Jupyter notebooks, OpenAI SDK, Anthropic SDK, Ollama-compatible OpenAI client, `pypdf`, `sentence-transformers`, `faiss-cpu`, NumPy, pandas, python-dotenv

---

## File Structure

**Create:**
- `material/Session 8/README.md`
- `material/Session 8/notebooks/01_llm_api_access.ipynb`
- `material/Session 8/notebooks/02_rag_with_pdfs_and_faiss.ipynb`
- `material/Session 8/data/README.md`
- `material/Session 8/data/pdfs/` (small curated subset only)
- `material/Session 8/data/questions.json`
- `material/Session 8/helpers/pdf_utils.py`
- `material/Session 8/helpers/rag_utils.py`

**Modify:**
- `requirements.txt`
- `AGENTS.md` only if an additional standing instruction becomes necessary during implementation

**Reference Only, Do Not Commit New Content From:**
- `material/Session 8/.old/`

**Tests / Verification Targets:**
- Notebook execution checks for non-network cells
- Import smoke tests for helper modules
- Manual verification that `.old` files are not staged

---

## Chunk 1: Prepare Session 8 Scope, Dataset, and Dependencies

### Task 1: Curate the Session 8 PDF corpus

**Files:**
- Create: `material/Session 8/data/README.md`
- Create: `material/Session 8/data/pdfs/`
- Create: `material/Session 8/data/questions.json`
- Reference only: `material/Session 8/.old/data/documents/`

- [ ] **Step 1: Inspect the archived Session 8 PDF candidates**

Run: `Get-ChildItem "material/Session 8/.old/data/documents" | Select-Object Name, Length`

Expected: a list of generic handbook/policy-style documents that can support factual retrieval questions.

- [ ] **Step 2: Select a small, teachable subset of PDFs**

Selection criteria:
- 2-4 documents only
- generic handbook/policy/benefits content
- good support for retrieval questions like eligibility, coverage, procedures, and comparison
- avoid very noisy or non-text-heavy files

Expected output: a shortlist of PDFs to reuse as Session 8 teaching data.

- [ ] **Step 3: Copy only the selected PDFs into the new Session 8 dataset area**

Create this structure:

```text
material/Session 8/data/
├── README.md
└── pdfs/
```

Do **not** move or rename files inside `.old`; copy only the chosen PDFs into `material/Session 8/data/pdfs/`.

- [ ] **Step 4: Write the dataset README**

Document:
- what the PDFs are
- why they were chosen
- that they are used for chunking/retrieval scenarios
- that `.old` remains archival and excluded from future commits

- [ ] **Step 5: Create a small evaluation question set**

Write `material/Session 8/data/questions.json` with 6-10 questions:
- 3 simple fact lookup questions
- 2 comparison questions across chunks or documents
- 1-2 questions likely to produce weak unguided answers without retrieval
- 1 question that should return “not enough information”

Example schema:

```json
[
  {
    "id": "q1",
    "question": "What does the handbook say about ...?",
    "expected_signal": "Answer should mention ...",
    "source_docs": ["employee_handbook.pdf"]
  }
]
```

- [ ] **Step 6: Commit the dataset scaffold**

```bash
git add "material/Session 8/data"
git commit -m "session 8: curate pdf dataset for rag notebook"
```

### Task 2: Add Session 8 dependencies

**Files:**
- Modify: `requirements.txt`

- [ ] **Step 1: Write the failing dependency checklist**

Required Session 8 packages:
- `anthropic`
- `pypdf`
- `sentence-transformers`
- `faiss-cpu`

Optional only if actually used:
- `ollama`

- [ ] **Step 2: Add the minimal required packages to `requirements.txt`**

Keep the list narrow. Do not add Azure AI Search or Streamlit/Gradio dependencies for the core Session 8 deliverables.

- [ ] **Step 3: Run an import smoke test**

Run:

```bash
& .\venv\Scripts\Activate.ps1
python -c "import openai, anthropic, pypdf, sentence_transformers, faiss"
```

Expected: exit code 0.

- [ ] **Step 4: Commit the dependency update**

```bash
git add requirements.txt
git commit -m "session 8: add api and rag dependencies"
```

---

## Chunk 2: Build Shared Helpers for PDF Parsing and RAG

### Task 3: Implement focused PDF utilities

**Files:**
- Create: `material/Session 8/helpers/pdf_utils.py`
- Test via: direct import and simple script

- [ ] **Step 1: Write a failing smoke script for PDF extraction**

Create a short ad hoc check expectation:
- can load a PDF path
- can extract page text
- returns a list or structured records, not raw side effects

Expected failing condition: module/function does not yet exist.

- [ ] **Step 2: Implement minimal PDF parsing helpers**

Include only clear, educational functions such as:

```python
def extract_pdf_text(pdf_path: str) -> list[dict]:
    ...

def join_pages(page_records: list[dict]) -> str:
    ...
```

Requirements:
- preserve page numbers
- handle empty pages safely
- keep implementation readable for students

- [ ] **Step 3: Run the PDF helper smoke test**

Run:

```bash
& .\venv\Scripts\Activate.ps1
@'
from material.Session_8.helpers.pdf_utils import extract_pdf_text
'@
```

If import path issues arise due to folder spacing, use a direct script invocation instead of package import.

- [ ] **Step 4: Commit the PDF helper module**

```bash
git add "material/Session 8/helpers/pdf_utils.py"
git commit -m "session 8: add pdf extraction helpers"
```

### Task 4: Implement focused RAG utilities

**Files:**
- Create: `material/Session 8/helpers/rag_utils.py`

- [ ] **Step 1: Write the failing smoke checklist for chunking and retrieval helpers**

Needed functions:
- document chunking with overlap
- chunk metadata packaging
- cosine or dot-product helper if useful
- FAISS index creation/search wrapper
- prompt assembly for grounded answers

- [ ] **Step 2: Implement a minimal explicit chunker**

Prefer something students can read in one screen, for example:

```python
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:
    ...
```

Requirements:
- explain overlap clearly in comments
- avoid hiding chunking behind a large library abstraction
- include metadata fields for document name and chunk id

- [ ] **Step 3: Implement FAISS helpers**

Examples:

```python
def build_faiss_index(embeddings: np.ndarray):
    ...

def search_index(index, query_embedding: np.ndarray, top_k: int = 3):
    ...
```

- [ ] **Step 4: Implement grounded prompt assembly**

Example:

```python
def build_grounded_prompt(question: str, retrieved_chunks: list[dict]) -> str:
    ...
```

The prompt should:
- instruct the model to use provided context only
- say when to admit insufficient information
- include chunk/document references for teaching traceability

- [ ] **Step 5: Run a local helper smoke test**

Run a short script that:
- chunks a short string
- generates dummy embeddings with NumPy
- builds a FAISS index
- returns top-k ids

Expected: all helper functions execute without network calls.

- [ ] **Step 6: Commit the RAG helper module**

```bash
git add "material/Session 8/helpers/rag_utils.py"
git commit -m "session 8: add minimal rag helpers"
```

---

## Chunk 3: Build Notebook 1 for OpenAI SDK-First API Access

### Task 5: Create `01_llm_api_access.ipynb`

**Files:**
- Create: `material/Session 8/notebooks/01_llm_api_access.ipynb`
- Reference only: `material/Session 8/.old/01.1 OpenAI Responses API.ipynb`
- Reference only: `material/Session 8/.old/01.8 Local Models with ollama.ipynb`

- [ ] **Step 1: Write the notebook outline in markdown cells first**

Required sections:
- Session purpose and learning goals
- environment variables and API keys
- OpenAI SDK setup
- Chat Completions example
- Responses API example
- structured output example
- provider swap pattern
- minimal Claude contrast
- recap

- [ ] **Step 2: Add a setup section that matches course conventions**

Requirements:
- use the course venv language, not a standalone repo setup
- explain required env vars for OpenAI, GitHub Models, Ollama, and optional Claude
- clearly mark optional sections

- [ ] **Step 3: Implement a minimal Chat Completions example**

Learning objective:
- students see the legacy-but-common message array format

Code should show:
- `OpenAI()` client
- `chat.completions.create(...)`
- `messages=[...]`
- one small deterministic example

- [ ] **Step 4: Implement the Responses API example**

Learning objective:
- students understand `instructions` vs `input`

Code should show:
- `client.responses.create(...)`
- a simpler equivalent task to the Chat Completions example
- short markdown comparison of the two APIs

- [ ] **Step 5: Implement one structured output example**

Use JSON schema or a simple structured response pattern.

Goal:
- demonstrate that app-building often requires machine-readable outputs, not just free text.

- [ ] **Step 6: Implement the provider swap pattern**

Teach one reusable pattern:
- OpenAI native call
- GitHub Models via OpenAI-compatible client config
- Ollama via local `base_url`

The notebook should explicitly note:
- OpenAI SDK is the primary teaching interface
- GitHub Models and Ollama are compatibility variants
- model names and auth differ, but client usage is similar

- [ ] **Step 7: Add a short Claude comparison section**

Only one minimal example.

Goal:
- show that Claude is relevant, but avoid splitting the notebook into provider-specific tracks.

- [ ] **Step 8: Add interpretation cells**

Students should leave knowing:
- when to use Chat Completions vs Responses API
- why OpenAI-compatible endpoints are useful
- that “same SDK” does not mean “all providers are identical”

- [ ] **Step 9: Run a partial execution check**

Execute non-network or environment-check cells only.

Expected:
- notebook structure is valid
- imports work
- any live API calls are clearly marked and easy to skip without breaking the notebook

- [ ] **Step 10: Commit notebook 1**

```bash
git add "material/Session 8/notebooks/01_llm_api_access.ipynb"
git commit -m "session 8: add llm api access notebook"
```

---

## Chunk 4: Build Notebook 2 for PDF-Based RAG with FAISS

### Task 6: Create `02_rag_with_pdfs_and_faiss.ipynb`

**Files:**
- Create: `material/Session 8/notebooks/02_rag_with_pdfs_and_faiss.ipynb`
- Reference only: `material/Session 8/.old/01.3 Embeddings.ipynb`
- Reference only: `material/Session 8/.old/04.1 Simlpe RAG Process.ipynb`
- Reference: `material/Session 8/vector_similarity.md`

- [ ] **Step 1: Write the notebook outline in markdown cells first**

Required sections:
- why RAG exists
- why PDFs need preprocessing
- load and inspect PDFs
- extract text
- chunking
- embeddings
- FAISS indexing
- retrieval
- grounded generation
- no-RAG vs RAG comparison
- limitations and production notes

- [ ] **Step 2: Implement PDF loading and extraction**

Use `pdf_utils.py`.

Show:
- which PDFs are loaded
- sample extracted text
- why extraction quality matters

- [ ] **Step 3: Implement chunking as an explicit teaching section**

Use `rag_utils.py`.

Must explain:
- what a chunk is
- why overlap exists
- why chunk size affects retrieval quality

Add a cell that prints example chunks and metadata.

- [ ] **Step 4: Implement embeddings over chunks**

Recommended primary path:
- OpenAI embeddings via SDK, because Session 8 is OpenAI-first

Recommended fallback:
- sentence-transformers for local/offline conceptual continuity if network/API access is unavailable

The notebook must explain which path is core and which is fallback.

- [ ] **Step 5: Implement FAISS indexing and retrieval**

Use a simple flat index.

Show:
- matrix shape of embeddings
- building the index
- retrieving top-k chunks for one question
- printing retrieved chunk text and metadata

- [ ] **Step 6: Implement grounded answer generation**

Use retrieved chunks to build a context prompt, then generate an answer.

Requirements:
- include chunk or document references in displayed output
- instruct the model to admit uncertainty when context is insufficient

- [ ] **Step 7: Add the no-RAG vs RAG comparison**

Use 3-5 questions from `material/Session 8/data/questions.json`.

For each:
- ask the model without retrieval
- ask with retrieval
- compare answer quality and grounding

Goal:
- make the value of chunking and retrieval visible, not abstract

- [ ] **Step 8: Add short conceptual extension cells**

Must mention, but not fully implement:
- OpenAI Vector Store as a managed alternative
- hybrid search as production baseline
- Agentic RAG as Session 9 preview

- [ ] **Step 9: Run a local-only execution check**

Execute all cells that do not require live model access.

Expected:
- parsing, chunking, FAISS, and prompt assembly work end-to-end locally

- [ ] **Step 10: Commit notebook 2**

```bash
git add "material/Session 8/notebooks/02_rag_with_pdfs_and_faiss.ipynb"
git commit -m "session 8: add pdf rag notebook"
```

---

## Chunk 5: Write the Student-Facing Session README

### Task 7: Create `material/Session 8/README.md`

**Files:**
- Create: `material/Session 8/README.md`

- [ ] **Step 1: Write the Session 8 overview**

Cover:
- APIs, RAG, vector stores, and minimal app-building
- how Session 7 leads into Session 8
- how Session 8 leads into Session 9

- [ ] **Step 2: Document prerequisites and environment setup**

Include:
- course venv activation
- installing `requirements.txt`
- required env vars
- optional provider-specific configuration

- [ ] **Step 3: Document notebook order and learning objectives**

Explicitly list:
- `01_llm_api_access.ipynb`
- `02_rag_with_pdfs_and_faiss.ipynb`

Explain what each notebook teaches and what students should notice.

- [ ] **Step 4: Document the PDF dataset**

Include:
- why generic handbook/policy PDFs were chosen
- how they support retrieval-style questioning
- a reminder that `.old` is archival only

- [ ] **Step 5: Add run notes and caveats**

Cover:
- some cells require API keys/network access
- Ollama is optional and local
- notebook execution can be partial in offline environments

- [ ] **Step 6: Commit the README**

```bash
git add "material/Session 8/README.md"
git commit -m "session 8: add session readme"
```

---

## Chunk 6: Final Verification and Commit Hygiene

### Task 8: Verify deliverables and archive exclusion

**Files:**
- Verify: `material/Session 8/README.md`
- Verify: `material/Session 8/notebooks/01_llm_api_access.ipynb`
- Verify: `material/Session 8/notebooks/02_rag_with_pdfs_and_faiss.ipynb`
- Verify: `material/Session 8/data/`
- Verify: `material/Session 8/.old/` remains unstaged for new content

- [ ] **Step 1: Run a final git status check**

Run:

```bash
git status --short
```

Expected:
- only intended Session 8 files are modified/staged.

- [ ] **Step 2: Run a `.old` exclusion check**

Run:

```bash
git status --short -- "material/Session 8/.old"
```

Expected: no staged `.old` files intended for commit.

- [ ] **Step 3: Run helper smoke tests**

Run:

```bash
& .\venv\Scripts\Activate.ps1
python -c "from pathlib import Path; print(Path('material/Session 8').exists())"
```

And add equivalent import checks for helper modules.

- [ ] **Step 4: Run notebook structure checks**

Use a lightweight validation approach:
- open notebook JSON
- ensure all cells parse
- execute local-only sections where feasible

- [ ] **Step 5: Review against Session 8 learning objectives**

Confirm the materials teach:
- OpenAI SDK usage
- Chat Completions vs Responses API
- compatibility with GitHub Models and Ollama
- PDF parsing and chunking
- embeddings and FAISS retrieval
- RAG vs no-RAG comparison
- OpenAI Vector Store / Agentic RAG conceptually

- [ ] **Step 6: Commit the final verification-safe state**

```bash
git add "material/Session 8" requirements.txt
git commit -m "session 8: complete core teaching materials"
```

