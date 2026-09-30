# Track D amendment 1 (2026-09-30), before any LLM result was scored > 0

Reason: in the first 4 LLM iterations (seed 1) all programs were rejected by the sandbox: 3x "forbidden name"
(the LLM used the conventional throw-away variable "_"), 1x "forbidden attribute: add" (set.add).
The feedback did not say which name was forbidden, so the LLM could not correct itself. This is a harness defect,
not a property of the LLM. Baseline arms (random, brute) are unaffected and are kept as run.

Changes (safety is unchanged: no imports, no dunder names or attributes, no file/network access, 20 s timeout):
1. Allow the bare name "_" (names starting with "_" followed by other characters stay forbidden).
2. Allow the set/dict methods add, update, discard, remove, get, keys, values, items.
3. Rejection feedback states the offending name/attribute.
4. The LLM arm restarts from iteration 0 for both seeds (the 4 rejected iterations are archived, not counted).
All other parts of TRACK_D_PLAN.md (budget, arms, stages, criteria) are unchanged.
