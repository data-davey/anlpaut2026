Week 7
30 March 2026
Session 7

topics:
- LLM Deep Dive
- Prompting Techniques
- LLM Challenges and Risks
- LLM Evaluation

## Notes

- Prompting notebook uses GitHub Models (OpenAI SDK, free with GitHub account) as a light API preview — full API coverage is Session 8
- Sentiment analysis is the consistent running example across all prompting content
- LLM Evaluation covers Tiers A–C: classical metrics → eval loop → LLM-as-judge

## Planned Notebooks

- `notebooks/01_prompting_techniques.ipynb` — zero/one/few-shot, CoT, role prompting, temperature, Grammar Correction Bot, LLM challenges demo
- `notebooks/02_llm_evaluation.ipynb` — BLEU, ROUGE, BERTScore, perplexity; DIY eval loop; LLM-as-judge; OpenAI Evals API (optional extension)

## References

- `llm_evals.md` — full LLM evaluation reference (metrics, benchmarks, leaderboards, eval tools, LLM-as-judge, custom eval pipeline)
- Wei et al. (2022) — Chain-of-Thought prompting
- Kojima et al. (2022) — Zero-shot CoT ("Let's think step by step")
- https://www.promptingguide.ai
