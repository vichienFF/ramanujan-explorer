# Amendment to PLAN_K4_FOLLOWUP (e551c1d): "Planck step" - register before running (2026-10-06)

Condition: run only if T1 (P1) and T2 (P2) hold. Status 2026-10-06: P1 holds (10/10 bins, p*/sqrt(N) 0.089-0.112),
P2 holds (0/400 shuffles) -> condition met. Data: rank-1 beta_p, se_p per 50k bin from k4_followup_t123.json (logN25k).

Idea (Planck 1900): two regimes, each described by a known law, joined by one formula with few constants; the constants
must then predict something measured independently.
- Small-p regime: first-order approximate functional equation, beta_p ~ A W_r(x)/p, x = 2 pi p / sqrt(N) (positive).
- Large-p regime (rank 1): beta_p < 0, not explained at first order.

Step 1 (fit, Cremona N < 500k only): candidate families with at most 2 free constants, e.g.
  beta_p * p = A [W_1(x) - lambda W_1(mu x)] ,  beta_p * p = A [E1(x) - lambda e^(-x)] , plus forms found by symbolic
  regression (PySR, if installed with approval) restricted to <= 2 constants and complexity <= 12.
  Fixed settings: target y = p*beta_p, inputs x = 2 pi p / sqrt(N_mid) (and log p), weights 1/(p*se_p)^2;
  PySR 1.5.9, operators + - * / exp log, maxsize 20, niterations 300, populations 30, random_state 1, deterministic.
  Split: fit on bins N in [0,50k),[100k,150k),...,[400k,450k) (even bins); score on the 5 odd bins.
  Selection: lowest weighted held-out error among formulas with <= 2 fitted constants; ties -> lower BIC.
  The winner and its constants are written down and registered BEFORE step 2.
Step 2 (independent prediction, the "Millikan test"): with constants frozen, predict beta_p and p*/sqrt(N) for the T4
  height-ordered family (N 1e6-1e7). Success: predicted p* within 20% of observed in >= 70% of N-bins, and RMS error of
  beta_p*p below that of the first-order AFE baseline.
Step 3 (meaning): if the constants are stable, check whether they match a known quantity (e.g. the BSD component that
  carries the negative part in T3, Tamagawa/torsion statistics, or a random-matrix prediction for odd orthogonal families).
Controls: the same fitting pipeline applied to rank 0 and to shuffled data must not produce a sign-changing law.
