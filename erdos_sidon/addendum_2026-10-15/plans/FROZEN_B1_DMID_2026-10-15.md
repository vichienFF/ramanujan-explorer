# Frozen predictions before opening sealed Lane B1 (rama-lb1-singer) - 2026-10-15
Data to open: lane_b/sealed/rama-lb1-singer/out/res_0..3.jsonl (SHA in LEDGER.md). Not opened before this file's SHA is recorded.
Question (Erdos #30 / C9 moment route, step (b)): do the mid-height ratio-count deviations D_mid of Singer sets decay with q?
B27 (seen) gave exponent -0.13 (se 0.165) on q 293..1373 - the registered q^-1/2 test failed on noise (orbit structure, ~8 values/q).

Tests (Singer sets only; nulls reported descriptively):
 T-a  slope of log D_mid vs log q over B27 (18 q) + B1 (17 q) together lies in [-0.75, -0.25].
      G2 (resid sd 0.27, 35 q): P(pass | true -0.5) 0.998; P(pass | -0.3) 0.73; P(pass | -0.1) 0.03; P(pass | 0) 0.001.
 T-b  boundedness: max over the 17 B1 q of sqrt(q) * D_mid <= 2.5 (B27 range 0.58..1.84).
 T-c  replication of B27 T1 on B1: C*M_C within [-1.5 - 3 sigma_C, -1.5 + 0.1 + 3 sigma_C] for >= 4 of 5 C
      (M_C = mean of q*R3 over Singer sets, sigma_C = sd of q*R3 over B1 nulls / sqrt(17)).
 Controls: forbidden counts 0 for all Singer sets, > 0 for all nulls; D_all exponent (B1 alone) within [-0.65, -0.35].
Verdicts by these rules only; anything else POST-HOC.
