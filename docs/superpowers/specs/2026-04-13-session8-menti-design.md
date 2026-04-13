# Menti Presentation Design — Session 8

**Date:** 2026-04-13
**Session:** 8 (Week 9) — Building LLM Apps with APIs and RAG
**Purpose:** Opening engagement activity. Warm up recall from Session 7, bridge to today's problem, tease Session 8 concepts.

---

## Context

- Students received the Session 8 materials over the weekend; many will have read ahead.
- Session 7 covered: prompting techniques (CoT, few-shot, role prompting), LLM challenges/risks, LLM evaluation (BLEU, ROUGE, BERTScore, LLM-as-judge).
- Session 8 covers: LLM API access, embeddings & vector similarity, streaming, RAG pipeline (chunk → embed → FAISS → retrieve → generate), tool use, Gradio/Streamlit apps.

---

## Design Decisions

- **6 questions total:** 2 Session 7 recall, 1 bridge, 2 Session 8 teasers, 1 creative closer.
- **Tone:** Gentle warm-up for recall; curiosity-sparker for teasers.
- **Format:** 4× multiple choice, 2× word cloud.
- **Structure:** Knowledge Chain — each question flows into the next, ending with an imaginative closer.

---

## Questions

### Q1 — Multiple Choice *(Session 7 recall: prompting)*

> "When you add 'Think step by step' to a prompt, which technique are you using?"

- Role prompting
- Few-shot prompting
- **Chain-of-thought** ✓
- Temperature tuning

---

### Q2 — Multiple Choice *(Session 7 recall: evaluation)*

> "Which evaluation method uses a language model to score another model's output?"

- BLEU score
- BERTScore
- **LLM-as-judge** ✓
- Perplexity

---

### Q3 — Multiple Choice *(Bridge: prompting → the RAG problem)*

> "A well-crafted prompt gives an LLM the context it needs to answer well. What's the problem when that context lives in a 500-page document?"

- The LLM can't read PDFs
- **You can't paste a 500-page document into every prompt** ✓
- The model needs to be fine-tuned first
- You'd need a bigger temperature

*Note: this question is the key bridge — it surfaces the problem RAG solves before the concept is introduced.*

---

### Q4 — Word Cloud *(Session 8 tease: RAG)*

> "Today we build a system that automatically retrieves the right document sections and feeds them to an LLM. What do you think this technique is called?"

*Expected responses: RAG, retrieval, semantic search, document search, grounding, augmented generation...*

---

### Q5 — Word Cloud *(Session 8 tease: embeddings)*

> "To find 'similar' documents, we convert sentences into lists of numbers. What do you call this numerical representation of text?"

*Expected responses: embeddings, vectors, encodings, features, representations...*

---

### Q6 — Multiple Choice *(Creative closer)*

> "If you could drop ANY set of documents into a chatbot and ask it questions — what would you build?"

- A chatbot over my own research / thesis
- A company policy & HR handbook assistant
- A product manual / technical docs helper
- Something completely different (share in chat!)

---

## Intended Flow

```
S7 recall (Q1) → S7 recall (Q2) → Bridge: surfaces the problem (Q3)
→ Tease the solution: RAG (Q4) → Tease the mechanism: embeddings (Q5)
→ Make it personal: what would you build? (Q6)
```

This arc takes students from "here's what we know" to "here's why today matters" to "here's how it connects to me."
