# Addendum 2026-10-15: Singer-set moment route (Batch 27 and Lane B1)

Supports the note "Gaps in dilates of Bose sets, moments of dilated Singer sets, and the excess in Erdős's Sidon problem: numerical evidence" (Version 1, 16 October 2026), Section 3. Upload location: erdos_sidon/addendum_2026-10-15/.

- `code/c3r_fast.py` - exact third factorial moment R3 over ALL dilations via the ratio identity, ratio counts N(rho), D_all, D_mid
  (checked against the direct all-unit average `code/c3r_a.py` to 1e-14).
- `code/b27_analyze.py` - registered verdicts of Batch 27 (plan `plans/PLAN_BATCH27_2026-10-15.md`, registered on GitHub before computing).
- `data/res_*.jsonl` - Batch 27 output (18 blind Singer q in 293..1373, 54 nulls, q=41 control); `data/b27_analyze.log` verdicts.
- `data/laneB1/res_*.jsonl` - sealed Lane B1 data (Singer q 1559..2969, 51 nulls), opened only after the frozen plan
  `plans/FROZEN_B1_DMID_2026-10-15.md` (SHA-256 0143ae4b... recorded in `plans/LEDGER.md` before opening); verdicts in
  `data/B1_DMID_result.log`.
- `data/c3r_a.jsonl` - ratio-height decomposition for q 41..173.
Computations designed and run with AI assistance (Anthropic Claude). Code MIT, data CC BY 4.0 (as the main release).
- `code/relations_ratio_ci.py` - mean per-q Bose/random ratio of 3-term relation counts and its percentile bootstrap interval
  (Section 2), run on `../data/relations_k3` of the main release: 0.9832, 95% [0.963, 1.000].
