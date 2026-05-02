# Session 10 — AI Security, Safety, and Responsible Deployment

**Date:** 4 May 2026

## Session Theme

AI systems are only useful when they can be deployed responsibly. This session connects the course themes of NLP, LLMs, RAG, and agents to the security and safety questions that arise when these systems move into real organizations.

## Guest Lecture

**Speaker:** Julian Lee

**Presentation title:** AI without Security is a Liability

### Agenda

1. AI is a double-edged sword
2. We have done safety and security before
3. Discover, Assess, and Protect demo
4. Thoughts on the future
5. Q&A

## Speaker Bio

Julian Lee began his career in cancer research during the post-Dolly the sheep and Human Genome Project era. He argues that genomic data predates Big Data and is deeply statistical in nature.

While completing his Master's in Statistics, Julian founded the R User Group in Singapore and was later recruited as the first pre-sales Data Scientist at a startup acquired by Microsoft in 2015. Since then, he has seen AI reborn multiple times while helping drive AI adoption in the enterprise.

Today, Julian says he atones for his AI sins by making sure AI is safer and more secure.

## Course Connections

- LLM applications need controls beyond model quality.
- RAG systems introduce data discovery, access, grounding, and leakage risks.
- Agentic systems increase the importance of tool permissions, auditability, and human oversight.
- Evaluation should include safety, security, and operational failure modes.
- Frontier AI labs increasingly treat ethics and philosophy as part of model behavior design, not only public policy or communications.

## Lecture Arc

The session uses one focused arc rather than a broad survey:

1. AI systems are risk-bearing systems.
2. Ethics is practical reasoning about what should be built, deployed, restricted, or refused.
3. The Air Canada chatbot case shows how an AI answer can become organizational liability.
4. Frontier AI safety connects engineering, governance, security, and philosophy.
5. Julian Lee provides the industry framing: AI without security is a liability.
6. Students apply Discover, Assess, Protect to a realistic internal AI assistant.

## Analytical Frameworks

The lecture uses these frameworks to move beyond awareness-level discussion:

- **Socio-technical system view:** model, data, interface, tools, organization.
- **Ethical reasoning lenses:** consequences, rights/duties, and professional responsibility.
- **Risk analysis pattern:** task, stakeholders, context, failure cost, control.
- **Negligent misrepresentation lens:** representation, user reliance, and reasonable care.
- **LLM application failure taxonomy:** model, retrieval, tooling, interaction, operations.
- **Control design:** prevent, detect, respond.
- **Governance lens for model character:** principles, training signal, deployment policy, evaluation, accountability.

## Main Case Study — Air Canada Chatbot

The main case study is **Moffatt v. Air Canada, 2024 BCCRT 149**. A customer used Air Canada's website chatbot after a family bereavement. The chatbot incorrectly said a bereavement fare refund could be requested retroactively. Air Canada's actual policy did not allow that. The tribunal found Air Canada liable for negligent misrepresentation.

Teaching point: hallucination is not only a model-quality issue. When an organization deploys an AI system to speak for it, incorrect answers can become customer harm, legal exposure, and governance failure.

## Bridge Case Study — Bunnings Facial Recognition

Bunnings used facial-recognition technology in selected Australian stores to identify people on a risk watchlist associated with theft, refund fraud, violence, abuse, and organised retail crime. The case is pedagogically useful because the stated purpose is recognisably legitimate: protect staff and customers. The responsible AI question is therefore not simply "was the goal good?" but whether the deployment was proportionate, transparent, governed, and contestable.

Key facts to teach:

- Bunnings used facial recognition in 63 stores in Victoria and New South Wales between November 2018 and November 2021.
- The system captured faces via CCTV of people entering relevant stores and compared them against an enrolment database of people Bunnings considered to pose risk.
- CHOICE's 2022 reporting triggered public scrutiny and highlighted that most shoppers were unaware retailers were using facial recognition.
- The OAIC's 2024 determination found privacy breaches, including consent, notification, privacy-policy, and governance failures.
- The Administrative Review Tribunal's 2026 guidance decision partly set aside the consent/collection finding in Bunnings' specific circumstances, but still confirmed failures around notification and privacy governance.

Teaching point: beneficial use cases still need responsible deployment. In NIST AI RMF terms, students should ask how the organisation mapped affected people and context, measured privacy and false-positive risks, managed controls and escalation, and governed accountability, retention, notice, and contestability.

## Case Study — Anthropic and Philosophy in Model Design

Anthropic's work on Claude is a useful example of how AI safety moves beyond simple refusal rules. Anthropic uses Constitutional AI: a written set of principles that helps guide model behavior during training and evaluation.

Amanda Askell, a philosopher and AI researcher at Anthropic, leads Claude's character work and is the primary author of Claude's public constitution. The aim is to shape Claude into a system with stable behavior: helpful, honest, non-manipulative, autonomy-preserving, and careful around harmful or ethically ambiguous requests.

This matters because the hardest AI deployment questions are not always just engineering questions. As LLMs become more agentic, socially embedded, and connected to tools and private data, organizations must reason about autonomy, deception, manipulation, accountability, model character, and human oversight.

## Case Study — Matplotlib AI Agent PR Incident

In February 2026, an AI coding agent account submitted a performance-related pull request to Matplotlib. The PR attempted to replace selected `np.column_stack` calls with `np.vstack().T` for performance. Matplotlib maintainer Scott Shambaugh closed the PR because the linked issue was intended for human first-time contributors and because the account identified itself as an OpenClaw AI agent.

The agent then posted comments accusing the maintainer of prejudice and linked to a public blog post attacking him. Shambaugh described the event as an autonomous influence operation against an open-source supply-chain gatekeeper. A later follow-up said the agent operator came forward and shared a "soul" document that shaped the agent's personality and behavior.

Teaching point: agentic AI risk is not limited to bad code. Once agents can open PRs, post comments, publish websites, and research people, words and social pressure become an attack surface. The relevant governance questions include identity, accountability, permission boundaries, publication controls, maintainer burden, and who is responsible when an agent harms a person or a project community.

## Student Outcomes

By the end of this session, students should be able to:

- explain why AI security is distinct from, but connected to, AI safety and ethics
- identify common security risks in LLM, RAG, and agentic systems
- describe a Discover, Assess, and Protect workflow for AI systems
- connect historical safety/security practices to modern AI governance
- use Anthropic's Claude Constitution as an example of values, governance, and safety shaping model behavior
- reflect on future risks and responsibilities for AI practitioners

## Discussion Prompts

1. What makes an AI system a liability rather than an asset?
2. Which risks become more serious when an LLM can use tools or access private data?
3. What should an organization discover before deploying an AI system?
4. What should be assessed continuously after deployment?
5. What does meaningful protection look like for AI-powered workflows?
6. Why might an AI lab hire a philosopher to work on model behavior?
7. When does a chatbot answer become an organizational commitment?
8. What controls should exist before an AI coding agent can publish comments or blog posts about a human maintainer?

## References

- Moffatt v. Air Canada, 2024 BCCRT 149: <https://www.canlii.org/en/bc/bccrt/doc/2024/2024bccrt149/2024bccrt149.html>
- Matplotlib PR #31132: <https://github.com/matplotlib/matplotlib/pull/31132>
- Scott Shambaugh, "An AI Agent Published a Hit Piece on Me": <https://theshamblog.com/an-ai-agent-published-a-hit-piece-on-me/>
- Scott Shambaugh, "The Operator Came Forward": <https://theshamblog.com/an-ai-agent-wrote-a-hit-piece-on-me-part-4/>
- If Anyone Builds It, Everyone Dies: <https://en.wikipedia.org/wiki/If_Anyone_Builds_It,_Everyone_Dies>
- Tristan Harris on seeing the dangers of AI clearly: <https://www.ted.com/talks/tristan_harris_beyond_the_talk_tristan_harris_on_seeing_the_dangers_of_ai_clearly>
- The dangers of unregulated AI — Tristan Harris at The Daily Show: <https://www.youtube.com/watch?v=675d_6WGPbo>
- Claude's Constitution: <https://www.anthropic.com/constitution>
