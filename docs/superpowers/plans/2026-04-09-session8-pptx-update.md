# Session 8 PPTX Update Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update `material/Session 8/ANLP Session8_Week9.PPTX` to align with Session 8 teaching materials by removing off-topic slides and adding missing core content.

**Architecture:** Use a Python script (`update_pptx.py`) with `python-pptx` to audit the existing slide deck, delete off-topic slides, and insert new slides with correct content and styling that matches the deck's existing theme.

**Tech Stack:** Python 3, `python-pptx`, existing PPTX file at `material/Session 8/ANLP Session8_Week9.PPTX`

---

## File Structure

- **Create:** `material/Session 8/update_pptx.py` — main script, runs all tasks in sequence
- **Create:** `material/Session 8/audit_slides.py` — one-time script to print slide index, title, and first body text for all 68 slides
- **Output:** `material/Session 8/ANLP Session8_Week9_UPDATED.PPTX` — final file (overwrite existing)

---

## Task 1: Audit Existing Slide Structure

**Files:**
- Create: `material/Session 8/audit_slides.py`

- [ ] **Step 1: Write audit script**

```python
# material/Session 8/audit_slides.py
from pptx import Presentation

pptx_path = "material/Session 8/ANLP Session8_Week9.PPTX"
prs = Presentation(pptx_path)

for i, slide in enumerate(prs.slides):
    title = ""
    body = ""
    for shape in slide.shapes:
        if shape.has_text_frame:
            text = shape.text_frame.text.strip()
            if not title and shape.shape_type == 13 or "title" in shape.name.lower():
                title = text[:80]
            elif not body:
                body = text[:80]
    if not title:
        # fallback: first text shape
        for shape in slide.shapes:
            if shape.has_text_frame:
                title = shape.text_frame.text.strip()[:80]
                break
    print(f"Slide {i+1:3d}: {title!r}")
    if body and body != title:
        print(f"         {body!r}")
```

- [ ] **Step 2: Run audit script**

```bash
cd /c/git/mdsiprojects/anlpaut2026
python "material/Session 8/audit_slides.py"
```

Expected: 68 lines, one per slide, with title and body excerpt. Confirm:
- Slides 23–40 are prompt engineering (few-shot, CoT, role prompting, etc.)
- Slide 14 is MCP
- Slide 36 is Fine-Tuning
- Slides 46, 50, 61–66 are Azure-heavy
- Slides 58–59 are references

> **Note:** If slide numbers differ from PPTX_REVIEW.md estimates, adjust the slide indices in subsequent tasks accordingly.

---

## Task 2: Delete Off-Topic Slides

**Files:**
- Create: `material/Session 8/update_pptx.py`

python-pptx has no `delete_slide` API. Use XML manipulation:

```python
def delete_slide(prs, index):
    """Delete slide at 0-based index."""
    xml_slides = prs.slides._sldIdLst
    slide = prs.slides[index]
    # remove from slide list
    xml_slides.remove(xml_slides[index])
    # remove slide part from package
    slide_part = slide.part
    prs.part.drop_rel(slide_part.partname)
```

> **Delete in reverse index order** so earlier indices stay valid as slides are removed.

- [ ] **Step 1: Create update_pptx.py with delete helper and delete phase**

Adjust the slide indices below based on the audit output from Task 1. These are 1-based from the review; convert to 0-based for the script.

```python
# material/Session 8/update_pptx.py
import copy
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

INPUT_PATH = "material/Session 8/ANLP Session8_Week9.PPTX"
OUTPUT_PATH = "material/Session 8/ANLP Session8_Week9_UPDATED.PPTX"

prs = Presentation(INPUT_PATH)

def delete_slide(prs, index):
    """Delete slide at 0-based index."""
    xml_slides = prs.slides._sldIdLst
    slide_part = prs.slides[index].part
    xml_slides.remove(xml_slides[index])
    slide_part_name = slide_part.partname
    rId = None
    for r in prs.part.rels.values():
        if r._target._partname == slide_part_name:
            rId = r.rId
            break
    if rId:
        prs.part.drop_rel(rId)

# -------------------------------------------------------
# SLIDES TO DELETE (1-based from PPTX_REVIEW.md)
# Convert to 0-based indices and sort DESCENDING so
# deletion of later slides doesn't shift earlier indices.
# -------------------------------------------------------
# Adjust these after confirming with audit output:
slides_to_delete_1based = (
    list(range(61, 67)) +   # Azure setup tutorial (slides 61-66)
    list(range(23, 41)) +   # Prompt Engineering section (slides 23-40)
    [36] +                   # Fine-tuning slide (inside 23-40 range, covered above)
    [14]                     # MCP slide
)
# Deduplicate and sort descending
slides_to_delete_0based = sorted(set(s - 1 for s in slides_to_delete_1based), reverse=True)

for idx in slides_to_delete_0based:
    if idx < len(prs.slides):
        print(f"Deleting slide at 0-based index {idx}")
        delete_slide(prs, idx)

print(f"Slides remaining: {len(prs.slides)}")
prs.save(OUTPUT_PATH)
print(f"Saved to {OUTPUT_PATH}")
```

- [ ] **Step 2: Run deletion phase**

```bash
cd /c/git/mdsiprojects/anlpaut2026
python "material/Session 8/update_pptx.py"
```

Expected output:
```
Deleting slide at 0-based index 65
Deleting slide at 0-based index 64
...
Slides remaining: 48
Saved to material/Session 8/ANLP Session8_Week9_UPDATED.PPTX
```

- [ ] **Step 3: Open UPDATED.PPTX in PowerPoint and visually confirm**

- Prompt engineering block (was ~slides 23–40) is gone
- Azure setup section (was ~slides 61–66) is gone
- MCP and fine-tuning slides are gone
- Slides before 23 are intact

---

## Task 3: Reduce Azure Section to 1 Reference Slide

After deleting slides 61–66, confirm slide 46 (Azure AI Search architecture) survives. Edit its content to serve as a single "Enterprise Vector Stores" reference slide.

- [ ] **Step 1: Append Azure consolidation to update_pptx.py**

Find the Azure AI Search slide by searching for its title text and update body:

```python
# Append to update_pptx.py (run on OUTPUT_PATH now)
prs = Presentation(OUTPUT_PATH)

AZURE_TITLE = "Enterprise Vector Stores: Azure AI Search"
AZURE_BODY = (
    "For production at scale:\n"
    "• Azure AI Search — managed vector + keyword hybrid search\n"
    "• Supports BM25 + semantic + RRF out of the box\n"
    "• Full setup guide: aka.ms/azure-ai-search-docs\n\n"
    "Not required for this course — FAISS covers the same concepts locally."
)

for slide in prs.slides:
    for shape in slide.shapes:
        if shape.has_text_frame and "azure" in shape.text_frame.text.lower():
            tf = shape.text_frame
            # Replace with consolidated content
            if "title" in shape.name.lower() or shape.shape_type == 13:
                tf.paragraphs[0].runs[0].text = AZURE_TITLE
            else:
                for para in tf.paragraphs:
                    for run in para.runs:
                        run.text = ""
                tf.paragraphs[0].runs[0].text = AZURE_BODY
            break

prs.save(OUTPUT_PATH)
print("Azure slide consolidated.")
```

- [ ] **Step 2: Run and verify**

```bash
python "material/Session 8/update_pptx.py"
```

Open UPDATED.PPTX and confirm the Azure slide now reads as a brief reference, not a multi-slide tutorial.

---

## Task 4: Add Provider Swap Pattern Slides (2 slides)

Insert after the SDK setup section (approximately slide 15 in updated deck — confirm position by looking for "SDK" or "Getting Started" slide).

- [ ] **Step 1: Add slide helper and provider swap slides to update_pptx.py**

```python
# Helper to add a new slide using the blank layout (index 6) and title+body layout (index 1)
def add_content_slide(prs, title_text, body_text, insert_after_index=None):
    """Add a slide with a title and body text box. Returns the new slide."""
    slide_layout = prs.slide_layouts[1]  # Title and Content
    slide = prs.slides.add_slide(slide_layout)

    # Set title
    slide.shapes.title.text = title_text

    # Set body
    body_shape = slide.placeholders[1]
    tf = body_shape.text_frame
    tf.word_wrap = True
    tf.text = body_text

    if insert_after_index is not None:
        # Move the new slide (currently at end) to desired position
        xml_slides = prs.slides._sldIdLst
        # The new slide is the last entry
        new_entry = xml_slides[-1]
        xml_slides.remove(new_entry)
        xml_slides.insert(insert_after_index + 1, new_entry)

    return slide


# --- Provider Swap Pattern: Slide 1 ---
PROVIDER_SWAP_1_TITLE = "Provider Swap Pattern"
PROVIDER_SWAP_1_BODY = (
    "All major LLM APIs follow the OpenAI chat format.\n"
    "Swap provider by changing base_url and model:\n\n"
    "# OpenAI\n"
    "client = OpenAI(api_key=OPENAI_KEY)\n\n"
    "# Anthropic (Claude) — via openai-compatible endpoint\n"
    "client = OpenAI(base_url='https://api.anthropic.com/v1', api_key=CLAUDE_KEY)\n\n"
    "# Ollama (local)\n"
    "client = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')"
)

# --- Provider Swap Pattern: Slide 2 ---
PROVIDER_SWAP_2_TITLE = "Choosing a Provider"
PROVIDER_SWAP_2_BODY = (
    "Provider       | Cost       | Latency  | Use case\n"
    "---------------|------------|----------|--------------------------\n"
    "OpenAI GPT-4o  | $$         | Fast     | Production apps\n"
    "Claude Sonnet  | $$         | Fast     | Long context, reasoning\n"
    "Ollama (local) | Free       | Varies   | Offline, privacy, testing\n\n"
    "→ The swap pattern means you can prototype locally and deploy to cloud with 2 lines changed."
)

# Insert after SDK setup slides (~slide index 14, 0-based)
# Adjust insert_after_index after confirming new slide order
prs = Presentation(OUTPUT_PATH)
add_content_slide(prs, PROVIDER_SWAP_1_TITLE, PROVIDER_SWAP_1_BODY, insert_after_index=14)
add_content_slide(prs, PROVIDER_SWAP_2_TITLE, PROVIDER_SWAP_2_BODY, insert_after_index=15)
prs.save(OUTPUT_PATH)
print("Provider swap slides added.")
```

- [ ] **Step 2: Run and verify slides appear after SDK section**

```bash
python "material/Session 8/update_pptx.py"
```

Re-run `audit_slides.py` (pointing at OUTPUT_PATH) to confirm new slides appear at the right position.

---

## Task 5: Add Streaming Responses Slides (2 slides)

- [ ] **Step 1: Add streaming slides to update_pptx.py**

```python
STREAMING_1_TITLE = "Streaming Responses"
STREAMING_1_BODY = (
    "Problem: Waiting 5–10s for full LLM response feels broken to users.\n\n"
    "Solution: Stream tokens as they arrive — same as ChatGPT's typing effect.\n\n"
    "# Non-streaming (waits for full response)\n"
    "response = client.chat.completions.create(model=MODEL, messages=msgs)\n"
    "print(response.choices[0].message.content)\n\n"
    "# Streaming (yields tokens progressively)\n"
    "stream = client.chat.completions.create(model=MODEL, messages=msgs, stream=True)\n"
    "for chunk in stream:\n"
    "    delta = chunk.choices[0].delta.content or ''\n"
    "    print(delta, end='', flush=True)"
)

STREAMING_2_TITLE = "Streaming in Gradio & Streamlit"
STREAMING_2_BODY = (
    "Gradio — use a generator function:\n"
    "def chat(message, history):\n"
    "    stream = client.chat.completions.create(..., stream=True)\n"
    "    partial = ''\n"
    "    for chunk in stream:\n"
    "        partial += chunk.choices[0].delta.content or ''\n"
    "        yield partial  # Gradio renders each yield\n\n"
    "Streamlit — write to a placeholder:\n"
    "with st.chat_message('assistant'):\n"
    "    placeholder = st.empty()\n"
    "    full = ''\n"
    "    for chunk in stream:\n"
    "        full += chunk.choices[0].delta.content or ''\n"
    "        placeholder.markdown(full)"
)

prs = Presentation(OUTPUT_PATH)
# Insert near the end of API section, before RAG content (~slide 20, 0-based)
# Adjust after auditing
add_content_slide(prs, STREAMING_1_TITLE, STREAMING_1_BODY, insert_after_index=18)
add_content_slide(prs, STREAMING_2_TITLE, STREAMING_2_BODY, insert_after_index=19)
prs.save(OUTPUT_PATH)
print("Streaming slides added.")
```

- [ ] **Step 2: Run and verify**

```bash
python "material/Session 8/update_pptx.py"
```

---

## Task 6: Add Vector Similarity Slides (2 slides)

- [ ] **Step 1: Add vector similarity slides**

```python
VECTOR_SIM_1_TITLE = "How Embeddings Work"
VECTOR_SIM_1_BODY = (
    "Text → Embedding model → Dense vector (e.g., 1536 floats)\n\n"
    "• Similar meaning → vectors point in similar directions\n"
    "• 'King' - 'Man' + 'Woman' ≈ 'Queen' (classic example)\n\n"
    "Why vectors?\n"
    "• Fast to compare (dot product)\n"
    "• Language-agnostic similarity\n"
    "• Captures semantic meaning, not just keywords\n\n"
    "API call:\n"
    "response = client.embeddings.create(input='your text', model='text-embedding-3-small')\n"
    "vector = response.data[0].embedding  # list of 1536 floats"
)

VECTOR_SIM_2_TITLE = "Cosine Similarity & Dot Product"
VECTOR_SIM_2_BODY = (
    "Cosine similarity: cos(θ) = (A · B) / (|A| × |B|)\n"
    "Range: -1 (opposite) → 0 (unrelated) → 1 (identical)\n\n"
    "L2 normalization: divide each vector by its length\n"
    "  → Normalized vectors: dot product = cosine similarity\n"
    "  → FAISS and OpenAI embeddings are already normalized\n\n"
    "import numpy as np\n"
    "def cosine_sim(a, b):\n"
    "    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))\n\n"
    "Rule of thumb: similarity > 0.85 = highly related text"
)

prs = Presentation(OUTPUT_PATH)
# Insert before FAISS/RAG section (~slide 22, 0-based)
add_content_slide(prs, VECTOR_SIM_1_TITLE, VECTOR_SIM_1_BODY, insert_after_index=21)
add_content_slide(prs, VECTOR_SIM_2_TITLE, VECTOR_SIM_2_BODY, insert_after_index=22)
prs.save(OUTPUT_PATH)
print("Vector similarity slides added.")
```

- [ ] **Step 2: Run and verify**

```bash
python "material/Session 8/update_pptx.py"
```

---

## Task 7: Add FAISS Vector Store Slides (2 slides)

- [ ] **Step 1: Add FAISS slides**

```python
FAISS_1_TITLE = "FAISS: Fast Local Vector Search"
FAISS_1_BODY = (
    "FAISS (Facebook AI Similarity Search)\n"
    "• In-memory vector index — no server required\n"
    "• Searches millions of vectors in milliseconds\n"
    "• Used in this course as the hands-on local vector store\n\n"
    "Building an index:\n"
    "import faiss, numpy as np\n"
    "dim = 1536  # embedding dimension\n"
    "index = faiss.IndexFlatL2(dim)   # exact search, L2 distance\n"
    "index.add(np.array(embeddings).astype('float32'))\n\n"
    "Querying:\n"
    "distances, indices = index.search(query_vec, k=5)  # top-5 chunks"
)

FAISS_2_TITLE = "FAISS vs. OpenAI Vector Store vs. Azure AI Search"
FAISS_2_BODY = (
    "Feature          | FAISS       | OpenAI VS    | Azure AI Search\n"
    "-----------------|-------------|--------------|----------------\n"
    "Setup            | pip install | API call     | Azure portal\n"
    "Persistence      | Manual save | Managed      | Managed\n"
    "Scale            | Single node | Cloud        | Enterprise\n"
    "Cost             | Free        | Per GB       | Per unit\n"
    "Hybrid retrieval | Manual      | Via API      | Built-in\n\n"
    "→ Use FAISS for learning and prototyping.\n"
    "→ Use OpenAI VS or Azure for production managed deployments."
)

prs = Presentation(OUTPUT_PATH)
# Insert after vector similarity slides
add_content_slide(prs, FAISS_1_TITLE, FAISS_1_BODY, insert_after_index=24)
add_content_slide(prs, FAISS_2_TITLE, FAISS_2_BODY, insert_after_index=25)
prs.save(OUTPUT_PATH)
print("FAISS slides added.")
```

- [ ] **Step 2: Run and verify**

```bash
python "material/Session 8/update_pptx.py"
```

---

## Task 8: Add PDF Chunking Strategy Slide (1 slide)

- [ ] **Step 1: Add chunking slide**

```python
CHUNKING_TITLE = "PDF Chunking Strategy"
CHUNKING_BODY = (
    "Why chunk? LLMs have token limits — can't send entire PDFs as context.\n\n"
    "Chunk size trade-offs:\n"
    "• Too small (< 100 tokens): loses context, misses multi-sentence answers\n"
    "• Too large (> 1000 tokens): dilutes relevance, wastes context window\n"
    "• Sweet spot: 300–500 tokens with 50-token overlap\n\n"
    "Overlap: repeat last N tokens of each chunk in the next → avoids split answers\n\n"
    "Tools: PyPDF2, pdfplumber (better table/layout handling), Markitdown\n\n"
    "Common mistake: splitting mid-sentence or mid-table → garbled chunks\n"
    "Fix: split on paragraph boundaries, not character count"
)

prs = Presentation(OUTPUT_PATH)
# Insert before RAG pipeline slide (~slide 28, 0-based)
add_content_slide(prs, CHUNKING_TITLE, CHUNKING_BODY, insert_after_index=27)
prs.save(OUTPUT_PATH)
print("Chunking slide added.")
```

- [ ] **Step 2: Run and verify**

```bash
python "material/Session 8/update_pptx.py"
```

---

## Task 9: Add Gradio + Streamlit App Walkthrough Slides (3 slides)

- [ ] **Step 1: Add app walkthrough slides**

```python
GRADIO_TITLE = "Gradio Chat Demo (05_gradio_chat_demo.ipynb)"
GRADIO_BODY = (
    "Gradio wraps any Python function in a web UI in 5 lines:\n\n"
    "import gradio as gr\n\n"
    "def chat(message, history):\n"
    "    stream = client.chat.completions.create(\n"
    "        model=MODEL, messages=[{'role':'user','content':message}],\n"
    "        stream=True)\n"
    "    partial = ''\n"
    "    for chunk in stream:\n"
    "        partial += chunk.choices[0].delta.content or ''\n"
    "        yield partial\n\n"
    "gr.ChatInterface(chat).launch()\n\n"
    "→ Open http://127.0.0.1:7860 — streaming chat UI in your browser"
)

STREAMLIT_1_TITLE = "Streamlit RAG App — Architecture"
STREAMLIT_1_BODY = (
    "06_streamlit_rag_app.py wires all Session 8 components together:\n\n"
    "1. Upload PDFs via sidebar → pdfplumber extracts text\n"
    "2. Text split into chunks → OpenAI embeddings → FAISS index\n"
    "   (@st.cache_resource: index built once, reused across queries)\n"
    "3. User question → embed question → FAISS top-5 chunks\n"
    "4. Retrieved chunks + question → LLM → streamed answer\n"
    "5. Answer displayed token-by-token with st.empty() placeholder\n\n"
    "This is a complete end-to-end RAG pipeline with a production-quality UI."
)

STREAMLIT_2_TITLE = "Streamlit RAG App — Running It"
STREAMLIT_2_BODY = (
    "Prerequisites:\n"
    "  pip install streamlit openai faiss-cpu pdfplumber\n"
    "  export OPENAI_API_KEY=sk-...\n\n"
    "Run:\n"
    "  streamlit run 'material/Session 8/06_streamlit_rag_app.py'\n\n"
    "→ Open http://localhost:8501 in your browser\n"
    "→ Upload a PDF from data/pdfs/\n"
    "→ Ask a question about the PDF content\n\n"
    "Key features to demo:\n"
    "• FAISS index caches after first build (fast re-queries)\n"
    "• Streaming answer appears progressively\n"
    "• Sidebar lets you swap provider/model"
)

prs = Presentation(OUTPUT_PATH)
# Insert near end, before references
add_content_slide(prs, GRADIO_TITLE, GRADIO_BODY, insert_after_index=35)
add_content_slide(prs, STREAMLIT_1_TITLE, STREAMLIT_1_BODY, insert_after_index=36)
add_content_slide(prs, STREAMLIT_2_TITLE, STREAMLIT_2_BODY, insert_after_index=37)
prs.save(OUTPUT_PATH)
print("App walkthrough slides added.")
```

- [ ] **Step 2: Run and verify**

```bash
python "material/Session 8/update_pptx.py"
```

---

## Task 10: Add RAG Evaluation Slide (1 slide)

- [ ] **Step 1: Add RAG evaluation slide**

```python
RAG_EVAL_TITLE = "How Do You Know RAG Is Working?"
RAG_EVAL_BODY = (
    "Without context (base LLM):\n"
    "Q: What is the dental coverage limit per year?\n"
    "A: 'I don't have information about your specific plan...' ✗\n\n"
    "With RAG (retrieved PDF chunk):\n"
    "Q: What is the dental coverage limit per year?\n"
    "A: 'According to your Benefits Guide, the annual dental limit is $1,500...' ✓\n\n"
    "Evaluation signals:\n"
    "• Grounded answer: cites or reflects document content\n"
    "• Retrieval quality: top-5 chunks include the answer sentence\n"
    "• Chunk distance: query embedding ↔ answer chunk cosine sim > 0.80\n\n"
    "questions.json in data/ has 20 Q&A pairs for testing the pipeline."
)

prs = Presentation(OUTPUT_PATH)
add_content_slide(prs, RAG_EVAL_TITLE, RAG_EVAL_BODY, insert_after_index=38)
prs.save(OUTPUT_PATH)
print("RAG evaluation slide added.")
```

- [ ] **Step 2: Run and verify**

```bash
python "material/Session 8/update_pptx.py"
```

---

## Task 11: Expand Hybrid Retrieval Slide

- [ ] **Step 1: Find and expand the hybrid retrieval slide**

```python
prs = Presentation(OUTPUT_PATH)

HYBRID_BODY = (
    "Hybrid retrieval combines two signals:\n\n"
    "1. BM25 (keyword): exact match, handles rare terms\n"
    "   score = tf(term) × idf(term)  (TF-IDF variant)\n\n"
    "2. Semantic (vector): catches paraphrases, synonyms\n"
    "   score = cosine_similarity(query_vec, chunk_vec)\n\n"
    "Reciprocal Rank Fusion (RRF) blends them:\n"
    "   RRF(d) = Σ 1 / (k + rank_in_system(d))   [k=60 typical]\n"
    "   → Documents ranked high in BOTH systems win\n\n"
    "Result: fewer missed answers than either method alone.\n"
    "Used in: Azure AI Search (built-in), OpenAI VS, Elasticsearch 8+"
)

for slide in prs.slides:
    for shape in slide.shapes:
        if shape.has_text_frame and "hybrid" in shape.text_frame.text.lower():
            if "title" not in shape.name.lower():
                tf = shape.text_frame
                tf.clear()
                tf.text = HYBRID_BODY
                print(f"Updated hybrid slide: {slide.slide_id}")
                break

prs.save(OUTPUT_PATH)
print("Hybrid retrieval slide expanded.")
```

- [ ] **Step 2: Run and verify**

```bash
python "material/Session 8/update_pptx.py"
```

---

## Task 12: Organize References Slide

- [ ] **Step 1: Find and replace references slides**

```python
prs = Presentation(OUTPUT_PATH)

REFS_BODY = (
    "Embeddings & Vector Search\n"
    "• OpenAI Embeddings: platform.openai.com/docs/guides/embeddings\n"
    "• FAISS: github.com/facebookresearch/faiss/wiki\n"
    "• Sentence Transformers: sbert.net\n\n"
    "RAG & Retrieval\n"
    "• RAG paper (Lewis 2020): arxiv.org/abs/2005.11401\n"
    "• Hybrid RRF: learn.microsoft.com/azure/search/hybrid-search-ranking\n\n"
    "Frameworks & Tools\n"
    "• Gradio: gradio.app/docs\n"
    "• Streamlit: docs.streamlit.io\n\n"
    "Providers\n"
    "• OpenAI API: platform.openai.com/docs\n"
    "• Claude API: docs.anthropic.com\n"
    "• Ollama: ollama.ai/docs"
)

for slide in prs.slides:
    for shape in slide.shapes:
        if shape.has_text_frame and "reference" in shape.text_frame.text.lower():
            if "title" not in shape.name.lower():
                shape.text_frame.clear()
                shape.text_frame.text = REFS_BODY
                print(f"Updated references slide: {slide.slide_id}")
                break

prs.save(OUTPUT_PATH)
print("References slide updated.")
```

- [ ] **Step 2: Run, verify, and commit**

```bash
python "material/Session 8/update_pptx.py"
```

Open `ANLP Session8_Week9_UPDATED.PPTX` in PowerPoint and do a full walkthrough:
- Deck flows: SDK → Provider Swap → Streaming → Embeddings → FAISS → Chunking → RAG Pipeline → Gradio → Streamlit → RAG Eval → Hybrid Retrieval → References
- No prompt engineering section (slides 23–40 gone)
- No Azure setup tutorial (slides 61–66 gone)
- MCP and fine-tuning slides gone
- All 7 learning outcomes from PPTX_REVIEW.md are now covered

```bash
git add "material/Session 8/ANLP Session8_Week9_UPDATED.PPTX" "material/Session 8/update_pptx.py"
git commit -m "session 8: update PPTX — remove off-topic slides, add core Session 8 content"
```

---

## Summary of Changes

| Action | Slides | Count |
|--------|--------|-------|
| Remove prompt engineering | 23–40 | -18 |
| Remove Azure setup | 61–66 | -6 |
| Remove MCP + fine-tuning | 14, 36 | -2 |
| Add provider swap pattern | new | +2 |
| Add streaming responses | new | +2 |
| Add vector similarity | new | +2 |
| Add FAISS + comparison | new | +2 |
| Add PDF chunking | new | +1 |
| Add Gradio + Streamlit | new | +3 |
| Add RAG evaluation | new | +1 |
| Expand hybrid retrieval | existing | 0 |
| Consolidate Azure to 1 slide | existing | 0 |
| **Net total** | | **~63 slides** |
