# Session 8 PPTX Review — Gaps & Inconsistencies

## Executive Summary

The PPTX has **68 slides** but diverges significantly from the Session 8 topics and notebook content. Key issues:

1. **Prompt engineering dominates** (18 slides) — this is Session 7 material, not Session 8
2. **Critical Session 8 topics are missing** — FAISS, streaming, vector similarity, PDF parsing, provider swap pattern
3. **Azure overrepresented** (~10% of slides) for optional enterprise content
4. **Core hands-on examples not covered visually** — Gradio, Streamlit, FAISS index building
5. **No RAG quality evaluation** — how do we know RAG works?

---

## Detailed Gaps & Inconsistencies

### 🔴 CRITICAL MISALIGNMENTS

#### 1. **Prompt Engineering (Slides 23–40: 18 slides)**

**Issue:** These are Session 7 topics, not Session 8.

**Expected in Session 8:** LLM API access and RAG pipeline design.

**What's covered:**
- Start with clear instructions, prime the output, prompt chaining, few-shot learning, CoT, role prompting, temperature, etc.

**What should happen:**
- Cut this section entirely, OR
- Keep 2–3 slides as a brief recap ("Review from Session 7"), then pivot to API access
- Free up 15+ slides for Session 8 core content

**Recommendation:** Remove slides 23–40 and replace with:
- Provider swap pattern (OpenAI → Claude → Ollama code examples)
- Streaming response walkthrough
- FAISS index building
- RAG pipeline evaluation

---

#### 2. **Azure Services Overweight (Slides 46, 50, 61–66: ~8 slides + references)**

**Issue:** Topics mark Azure AI Search as optional enterprise reference, not part of hands-on.

**What's covered:**
- Azure AI Search architecture
- Vector database capabilities
- Azure Portal, hierarchy, products
- "Optional: Create Azure Subscription"

**Problem:** Takes ~12% of slide real estate but students don't build with it.

**Recommendation:**
- Reduce to 1–2 reference slides (e.g., "Enterprise Vector Stores: Azure AI Search as an alternative")
- Move bulk Azure setup instructions to supplementary docs, not main PPTX
- Reallocate slides to core Session 8 content

---

### 🟡 MAJOR GAPS

#### 3. **Provider Swap Pattern (MISSING)**

**Notebook Coverage:** 01_llm_api_access.ipynb shows OpenAI, Claude, Ollama with base_url/model swaps

**PPTX Coverage:** OpenAI only; no mention of Claude or Ollama

**What's Missing:**
- Slide showing provider URLs (api.openai.com vs. api.anthropic.com vs. localhost:8000)
- Code comparison: how to swap between OpenAI, Claude, and Ollama
- Why students might choose each (cost, latency, self-hosted)

**Recommendation:** Add 2–3 slides after SDK setup showing the provider swap pattern with code snippets

---

#### 4. **FAISS Vector Store (MISSING)**

**Topics:** "Vector Stores: FAISS and OpenAI Vector Store"

**Notebook:** 04_rag_with_pdfs_and_faiss.ipynb is entirely FAISS-focused (25 cells)

**PPTX Coverage:** 
- Slide 50: Generic "Vector database built for enterprise scale"
- No FAISS-specific content
- No index types (flat vs. IVF vs. HNSW)
- No in-memory vs. managed service trade-offs

**What's Missing:**
- What is FAISS and why students use it (fast local similarity search)
- Index types and speed/accuracy trade-offs
- When to use FAISS vs. OpenAI Vector Store vs. enterprise solutions (Azure AI Search)
- Visualization of how FAISS index works

**Recommendation:** Add 2–3 slides explaining FAISS and its role in the hands-on RAG pipeline

---

#### 5. **Streaming Responses (MISSING)**

**Topics:** "Streaming Responses for apps"

**Notebook:** 03_streaming_responses.ipynb is dedicated to this (16 cells)

**PPTX Coverage:** Zero explicit coverage of streaming

**What's Missing:**
- Why streaming matters for UX (don't wait 5 seconds for full response)
- Comparison: non-streaming vs. streaming responses
- Generator pattern and event loops in Python
- How to integrate streaming into Gradio/Streamlit apps

**Recommendation:** Add 2–3 slides showing the streaming pattern and why it improves app feel

---

#### 6. **Vector Similarity Concepts (MISSING)**

**Notebook:** 02_embeddings_and_similarity.ipynb covers embeddings, cosine similarity, dot product

**Reference:** vector_similarity.md has full mathematical breakdown

**PPTX Coverage:** 
- Slide 49: "Vector search and vector databases" (generic)
- Slide 51: "How do I get started with Vector search?" (setup only, not concepts)
- No explanation of cosine similarity, dot product, or L2 normalization

**What's Missing:**
- How embeddings work (text → vector)
- Cosine similarity formula and intuition
- Why L2 normalization matters
- Why dot product ≈ cosine similarity when vectors are normalized

**Recommendation:** Add 1–2 slides explaining vector similarity with worked examples

---

#### 7. **PDF Parsing & Chunking Strategies (WEAK)**

**Notebook:** 04_rag_with_pdfs_and_faiss.ipynb covers PDF extraction, chunking, overlap

**PPTX Coverage:** 
- Slide 57: "Use Markitdown + markdown-chunker for chunking or langchain data ch[unking]"
- Single sentence, no context on *why* chunking matters or how to choose chunk size/overlap

**What's Missing:**
- Chunk size trade-offs (too small = lost context; too large = diluted relevance)
- Overlap between chunks (why it helps multi-span answers)
- PDF parsing libraries (PyPDF2, pdfplumber, Markitdown)
- Common mistakes (e.g., splitting mid-sentence, losing metadata)

**Recommendation:** Add 1–2 slides on chunking strategy and code example

---

#### 8. **Gradio Chat Demo Walkthrough (WEAK)**

**Notebook:** 05_gradio_chat_demo.ipynb is a minimal but complete example (9 cells)

**PPTX Coverage:** 
- Slide 18: "Chat app using gradio: > 2.1 chatapp_gradio.ipynb"
- One reference slide, no walkthrough

**What's Missing:**
- How to connect a chat API to Gradio UI
- Key components: ChatInterface, message state, streaming integration
- Running the notebook and seeing live results

**Recommendation:** Add 1 slide with Gradio code snippet showing connect-API-to-UI pattern

---

#### 9. **Streamlit RAG App (MISSING)**

**Deliverable:** 06_streamlit_rag_app.py is the main build (100+ lines)

**PPTX Coverage:** 
- Slide 19: "https://share.streamlit.io/ Reference: https://blog.streamlit.io/hos[ting]"
- Generic Streamlit reference, no Session 8 app walkthrough

**What's Missing:**
- Architecture of the RAG app (load PDFs → build FAISS index → stream answers)
- How to run it (`streamlit run 06_streamlit_rag_app.py`)
- Key features: caching with @st.cache_resource, sidebar configuration, streaming responses
- Why it combines everything (API + embeddings + FAISS + streaming + UI)

**Recommendation:** Add 1–2 slides showing the app architecture and how to run it

---

#### 10. **RAG Pipeline Evaluation (MISSING)**

**Notebook:** 04_rag_with_pdfs_and_faiss.ipynb likely shows RAG vs. non-RAG comparison

**PPTX Coverage:** 
- Slide 43: "Anatomy of the workflow" (just the pipeline, no evaluation)
- No metrics or how to measure retrieval quality

**What's Missing:**
- How do you know if RAG is working? (answer correctness, retrieval relevance)
- RAG vs. non-RAG side-by-side: does adding context actually help?
- Why chunking/embedding/retrieval quality matters for final answer

**Recommendation:** Add 1 slide showing RAG quality evaluation (e.g., metrics, before/after comparison)

---

#### 11. **OpenAI Vector Store (LIGHT)**

**Topics:** "FAISS and OpenAI Vector Store" — two equal options

**Notebook:** 04 uses FAISS; integration notes may reference OpenAI Vector Store

**PPTX Coverage:** 
- No dedicated OpenAI Vector Store coverage
- Only mentioned passingly in Azure AI Search context

**What's Missing:**
- When to use OpenAI Vector Store (managed service, works with Responses API)
- How it differs from FAISS (managed vs. local, ecosystem lock-in vs. flexibility)
- Quick code example showing file_search tool in Responses API

**Recommendation:** Add 1 slide comparing FAISS vs. OpenAI Vector Store (trade-offs)

---

#### 12. **Hybrid Retrieval (INCOMPLETE)**

**Slide 48:** "Hybrid retrieval brings out the best of keyword and vector search"

**Problem:** Statement without explanation or code.

**Topics.md context:**
- Hybrid (BM25 + semantic + RRF) is the "recommended production baseline"
- Has mathematical formulas and reasoning

**What's Missing:**
- Why combine BM25 and semantic search?
- Reciprocal Rank Fusion (RRF) formula and intuition
- When hybrid outperforms single-method retrieval
- Code example or diagram of the RRF fusion process

**Recommendation:** Expand slide 48 to 2 slides: why hybrid works + RRF fusion diagram

---

### 🟢 MINOR ISSUES

#### 13. **MCP (Model Context Protocol) Slide 14**

**Problem:** Mentioned in intro, not connected to Session 8 hands-on.

**Issue:** Takes a slide but adds no learning outcome for this session.

**Recommendation:** Cut or move to Session 9 when agents are introduced.

---

#### 14. **Fine-Tuning Slide 36**

**Slide:** "Fine-Tuning with Chain-of-Thought"

**Problem:** Fine-tuning is a Session 6+ topic, not Session 8. Belongs with prompt engineering section.

**Recommendation:** Remove or merge into cut Section (slides 23–40).

---

#### 15. **References Slide Quality**

**Slides 58–59:** References and links

**Problem:** Links are bare URLs without context or hierarchy.

**Recommendation:** Organize by topic (embedding models, RAG papers, vector DB docs) with short descriptions.

---

## Summary of Recommended Changes

### Remove (free up ~20 slides):
- **Slides 23–40** (Prompt Engineering — Session 7 recap, not Session 8 core)
- **Slides 61–66** (Azure setup tutorial — move to supplementary docs)
- **Slides 14, 36** (MCP, fine-tuning — not Session 8 scope)
- Consolidate references (Slides 58–59)

### Add/Expand:
- **Provider Swap Pattern** (OpenAI ↔ Claude ↔ Ollama): 2 slides
- **FAISS Vector Store**: 2 slides (what it is, index types, when to use)
- **Streaming Responses**: 2 slides (why + generator pattern)
- **Vector Similarity**: 1–2 slides (cosine similarity, dot product intuition)
- **PDF Chunking Strategy**: 1 slide (chunk size, overlap, tools)
- **Gradio Demo**: 1 slide (connect API to UI)
- **Streamlit RAG App**: 2 slides (architecture + how to run)
- **RAG Evaluation**: 1 slide (metrics, RAG vs. non-RAG)
- **FAISS vs. OpenAI Vector Store**: 1 slide (trade-offs)
- **Hybrid Retrieval Deep Dive**: 1 slide (RRF fusion diagram)

### Estimate:
- Remove: ~20 slides
- Add: ~15 slides
- **New total: ~63 slides** (leaner, more focused)

---

## Alignment with Learning Outcomes

**Session 8 should enable students to:**

1. ✅ Explain how modern LLMs are accessed via API — **COVERED** (SDK slides 4–15)
2. ✅ Use OpenAI, Claude, Ollama clients interchangeably — **MISSING** (provider swap pattern)
3. ✅ Build embeddings and understand vector similarity — **WEAK** (no similarity concepts)
4. ✅ Understand streaming for better UX — **MISSING** (no streaming section)
5. ✅ Implement a RAG pipeline end-to-end — **WEAK** (no FAISS, no chunking strategy, no evaluation)
6. ✅ Build a working Gradio or Streamlit app — **WEAK** (no walkthroughs)
7. ✅ Compare retrieval approaches (lexical vs. semantic vs. hybrid) — **INCOMPLETE** (hybrid mentioned, not explained)

**Current PPTX covers 1 & 7 (partially). Missing 2–6.**

---

## Next Steps

1. **Cut** Prompt Engineering section (slides 23–40)
2. **Cut** Azure setup section (keep 1 reference slide)
3. **Cut** MCP and fine-tuning slides
4. **Add** Provider swap pattern (2 slides)
5. **Add** Streaming walkthrough (2 slides)
6. **Add** FAISS vector store (2 slides)
7. **Add** Vector similarity concepts (1 slide)
8. **Add** PDF chunking strategy (1 slide)
9. **Add** Gradio + Streamlit app walkthroughs (3 slides)
10. **Add** RAG evaluation + FAISS vs. OpenAI (2 slides)
11. **Expand** Hybrid retrieval explanation (1 slide)
12. **Reorganize** references by topic

**Estimated time to update:** 1–2 hours

