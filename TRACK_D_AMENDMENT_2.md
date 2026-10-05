# Track D amendment 2 (2026-10-05)

Problem: from LLM seed 1 iteration 37 every request fails with Groq HTTP 413: the prompt (system text + feedback with
the 3 best previous programs) exceeds the free-tier per-minute token limit (8,000 tokens), so the request can never
succeed. This is a harness defect (prompt growth), not a property of the LLM.

Change (applies to all remaining LLM iterations of both seeds; completed iterations are kept as they are):
- Feedback includes the aggregate statistics of the last 8 iterations (unchanged) and only the single best previous
  program, truncated to its first 3,000 characters.
Everything else in TRACK_D_PLAN.md and amendment 1 is unchanged (arms, budget, evaluation, criteria).
