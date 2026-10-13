"""Test the hypothesis "disguised low-degree formula" (e.g. contraction): is x of a mystery PCF a Mobius transform of a low-degree PCF value
(a deg 1, b deg 2, |coefficients| <= C)? Uses bf_search.cf_eval_vec (float) + hashing, then a 60-digit confirmation."""
import itertools, json, math, sys
import numpy as np
import mpmath as mp
sys.argv = [sys.argv[0]]
import bf_search as B

C, R = 6, 4
rng = range(-C, C + 1)
Bs = np.array([b for b in itertools.product(rng, repeat=3) if any(b)], dtype=float)
table = {}
for a in itertools.product(rng, repeat=2):
    if a[1] == 0:
        continue
    v, conv = B.cf_eval_vec(a, Bs, 300)
    for i in np.nonzero(conv)[0]:
        x = v[i]
        if 1e-6 < abs(x) < 1e6:
            table.setdefault(round(float(x), 7), []).append((a, tuple(int(t) for t in Bs[i])))
print("low-degree table", len(table), flush=True)
T = json.load(open("bf_runs/test_fr/mystery_irreducible.json"))
res, explained = [], 0
Rr = range(-R, R + 1)
for m in T:
    x = float(m["x80"][:25]); hit = None
    for p, q, r, s in itertools.product(Rr, Rr, Rr, Rr):
        if p * s - q * r == 0:
            continue
        den = r + s * x
        if abs(den) < 1e-9:
            continue
        y = (p + q * x) / den
        for key in (round(y, 7), round(y + 1e-7, 7), round(y - 1e-7, 7)):
            for a2, b2 in table.get(key, []):
                mp.mp.dps = 60
                yy = B.cf_mp(list(a2), list(b2), 3000, 60)
                X = mp.mpf(m["x80"])
                if abs((p + q * X) / (r + s * X) - yy) < mp.mpf(10) ** -40:
                    hit = {"mobius": [p, q, r, s], "low_a": a2, "low_b": b2}
                    break
            if hit: break
        if hit: break
    explained += bool(hit)
    res.append(dict(m, lowdeg=hit))
    print(m["a"], m["b"], "->", hit, flush=True)
json.dump(res, open("bf_runs/test_fr/mystery_lowdeg.json", "w"), indent=0)
print("explained", explained, "/", len(T))
