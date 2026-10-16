# LANE B - standing sealed data collection (registered once; user decision 2026-10-15)
Purpose: keep Kaggle busy with data that will serve as BLIND test sets for future Lane A plans. Fixed rules, no hypothesis here.

## Sealing rules
1. Lane B outputs are pulled to math_explorer/lane_b/sealed/<kernel>/ and their SHA-256 is written to lane_b/LEDGER.md.
2. Before unsealing, Claude may only run lane_b/check_complete.py, which prints row counts, error rows and run times
   (never values of the statistics).
3. A sealed file is opened only after a Lane A plan that names the file and states frozen predictions has been uploaded to
   GitHub (commit + SHA verified). Opening is logged in LEDGER.md with that plan's commit.
4. Any accidental exposure is disclosed and the exposed items are removed from later blind tests (as for q 1427/1487 in B27).
5. Jobs are deterministic (fixed seeds, fixed lists) so any slice can be recomputed.

## B1 - Singer k = 3 exact data (kernel rama-lb1-singer; erdos/c3r_fast.py, same code as C3R-b)
Every prime q in [1500, 3000] with m = q^2+q+1 prime (17 q: 1559 ... 2969), Singer + 3 null sets, C in {2,3,4,5,8}.
Outputs per set: forbidden counts, D_all, D_mid, R3 for each C. Estimated 3.5 h (4 shards, slowest first).
## B2 - Bose dilate gaps beyond the blind range (kernels rama-lb2-bose-a, -b; erdos/b23a_gaps.py, same code as Batch 23)
Every 8th prime in (5881, 10000] (57 q: 5897 ... 9929), KINDS = bose, plus the q = 829 positive control (excess 10.2797).
Estimated 3-4 h per kernel (2 kernels x 4 shards).
## Later slices (each by a one-line amendment; same rules): B1 q in (3000, 4500]; B2 every 8th prime offset 1..7; BSD curve
data once the BSD code is reviewed.
