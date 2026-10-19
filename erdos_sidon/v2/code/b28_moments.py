"""Batch 28: factorial moments R_k (k=3..6) of window counts in dilates of Singer sets, fast histogram version of
b25m_moments.moments (same estimator: mean over sampled unit classes t and ALL shifts s of (Z)_k; R_k = F_k/H_k - 1)."""
import numpy as np
K = 6
def hyper(n, l, m, k):
    v = 1.0
    for i in range(k): v *= (n - i) * (l - i) / (m - i)
    return v
def moments(S, m, q, C, ts):
    n = len(S); l = C * q; per_t = np.zeros((len(ts), K + 1))
    zv = np.arange(64, dtype=float); ffz = np.ones((K + 1, 64))
    for k in range(1, K + 1): ffz[k] = ffz[k - 1] * (zv - (k - 1))
    for j, t in enumerate(ts):
        pos = np.sort((t * S) % m)
        # Z(s) = #pos in [s, s+l) for all s: count via searchsorted on doubled positions
        p2 = np.concatenate([pos, pos + m])
        s = np.arange(m)
        Z = np.searchsorted(p2, s + l, side="left") - np.searchsorted(p2, s, side="left")
        h = np.bincount(Z, minlength=64)[:64] / m
        per_t[j] = ffz @ h
    F = per_t.mean(axis=0)
    out = {f"R{k}": float(F[k] / hyper(n, l, m, k) - 1) for k in range(1, K + 1)}
    out |= {f"se_R{k}": float((per_t[:, k] / hyper(n, l, m, k)).std() / np.sqrt(len(ts))) for k in range(2, K + 1)}
    return out
