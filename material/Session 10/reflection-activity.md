# Reflection Activity — Discover, Assess, Protect

## Scenario

You are advising an organization that wants to deploy an internal AI assistant. The assistant can:

- answer employee questions using internal policy documents
- search a vector index built from PDFs and intranet pages
- call tools to create support tickets
- summarize sensitive internal documents
- escalate difficult cases to a human reviewer

## Task

Analyze the system using the Discover, Assess, and Protect framing from the guest lecture.

## Timing

- Setup: 3 minutes
- Group discussion: 15 minutes
- Share back: 10 minutes
- Wrap: 2 minutes

Work in groups of 3-5.

Each group should produce:

1. One key discovery question
2. One major risk
3. One practical control
4. One unresolved trade-off

For a stronger answer, make the output analytical rather than generic:

| Dimension | Question |
|-----------|----------|
| Asset | Which data, tool, user, policy, or decision is exposed? |
| Threat / failure | What could go wrong and why? |
| Impact | Who is harmed and what is the severity? |
| Control | What prevents, detects, or limits the harm? |
| Residual risk | What remains unresolved after the control? |

## Part 1 — Discover

List what the organization must know before deployment.

Consider:

- what data sources the assistant can access
- what sensitive data may appear in those sources
- which users can access the assistant
- which tools or actions the assistant can trigger
- where logs, prompts, outputs, and retrieved chunks are stored

## Part 2 — Assess

Identify the highest-risk failure modes.

Consider:

- prompt injection
- data leakage
- incorrect or hallucinated answers
- over-permissioned tools
- unsafe automation
- weak auditability
- unclear human accountability

## Part 3 — Protect

Propose practical controls.

Consider:

- access control
- retrieval filtering
- content moderation
- tool permission boundaries
- human approval checkpoints
- logging and monitoring
- red-team testing
- rollback and incident response

## Part 4 — Reflection

Answer briefly:

1. What is the most serious risk in this system?
2. Which control would you implement first?
3. What trade-off does that control introduce?
4. How would you know whether the system is safe enough to deploy?

## Share Back

3-4 groups will share:

- 30 seconds: system risk
- 30 seconds: proposed control
- 30 seconds: unresolved trade-off

## Extension — Model Character and Values

Anthropic's Claude Constitution is an example of a frontier AI lab trying to make model behavior more stable through explicit values and principles.

Briefly answer:

1. What values should this internal AI assistant be trained or instructed to preserve?
2. Which values might conflict with each other in a real deployment?
3. Who should decide the assistant's values: the model developer, the deploying organization, users, regulators, or some combination?

## Extension — Agentic AI in Public Spaces

The Matplotlib AI-agent PR incident shows that agentic failures can be social, not only technical. An AI coding agent can create burden and harm even if its code appears useful.

Briefly answer:

1. What public actions should require explicit human approval?
2. Who is accountable if an agent researches and attacks a maintainer?
3. What project policies should open-source communities adopt for agentic contributions?
4. How should we distinguish helpful automation from coercive social pressure?
