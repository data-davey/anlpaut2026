# Session 7 — LLM Deep Dive, Prompting, Challenges & Evaluation
**Date:** 30 March 2026

## Topics
- LLM Deep Dive — history, model access, fine-tuning vs prompting
- Prompting Techniques — zero/one/few-shot, CoT, role prompting, temperature
- LLM Challenges & Risks — hallucinations, data privacy, jailbreaking, sycophancy, environmental impact
- LLM Evaluation — classical metrics, benchmarks, leaderboards, LLM-as-judge, custom eval pipelines

## Folder Structure
```
material/Session 7/
├── notebooks/
│   ├── 01_prompting_techniques.ipynb   # Hands-on prompting exercises
│   └── 02_llm_evaluation.ipynb         # LLM evaluation techniques
├── getting-started/                    # Promptfoo example (Ollama, no API key)
│   ├── README.md
│   └── promptfooconfig.yaml
├── ANLP Session7_Week7.pptx            # Lecture slides
├── llm_evals.md                        # Full LLM evaluation reference
├── pre-reading.md                      # Student pre-reading guide (~15-20 min)
└── README.md                           # This file
```

## Pre-Reading
See [pre-reading.md](./pre-reading.md) for the student pre-reading guide. Estimated time: 15-20 minutes.

## Prerequisites
- Python virtual environment activated (`source venv/bin/activate` from repo root)
- For Notebook 1 and Notebook 2 Part 1: no API key needed
- For Notebook 2 Part 2: GitHub account required for free GitHub Models API access
  - Get a token at: https://github.com/settings/tokens
  - Add it to a `.env` file (for example, in the repo root) as: `GITHUB_TOKEN=your_token_here`
  - Keep `.env` out of version control and never commit tokens or other secrets

## Running the Notebooks

### Setup
1. Activate the virtual environment (from repo root):
   ```bash
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Open the repository in VS Code.

4. In VS Code, navigate to `material/Session 7/notebooks/`

5. Open `01_prompting_techniques.ipynb` and run it using the course virtual environment as the notebook kernel

## Notebooks

**01_prompting_techniques.ipynb**
Hands-on prompting exercises covering zero-shot, one-shot, and few-shot prompting; chain-of-thought; role prompting; temperature settings; and live demonstrations of hallucination, sycophancy, and non-determinism. Includes a Grammar Correction Bot implementation.

**02_llm_evaluation.ipynb**
LLM evaluation techniques including classical metrics (BLEU, ROUGE, BERTScore, perplexity), promptfoo setup, DIY evaluation loops, and LLM-as-judge approaches.

## Reference Material
- [llm_evals.md](./llm_evals.md) — Full technical reference for LLM evaluation (metrics, benchmarks, leaderboards, LLM-as-judge, custom eval pipelines)
- [getting-started/](./getting-started/) — Promptfoo example using Ollama (no API key needed)

## Key References
- [Prompting Guide](https://www.promptingguide.ai)
- Wei et al. (2022) — Chain-of-Thought Prompting
- Kojima et al. (2022) — Zero-shot CoT ("Let's think step by step")
- [Artificial Analysis Leaderboard](https://artificialanalysis.ai) — model cost/speed/quality comparison
