"""Test the survivors + F1 against Gamma(1/3), Gamma(1/4) family constants (lead from a Cohen hit: pi^2/Gamma(2/3)^3) - PSLQ [1,x,c,xc] <= 1e6 and [1,x,c,xc,d,xd] for pairs c,d"""
import json, itertools
import mpmath as mp
mp.mp.dps = 110
g3, g4, pi, s3, s2 = mp.gamma(mp.mpf(1)/3), mp.gamma(mp.mpf(1)/4), mp.pi, mp.sqrt(3), mp.sqrt(2)
K3 = g3**3 * s3 / pi
K4 = g4**2 / mp.sqrt(pi)
C = {"K3=G(1/3)^3 sqrt3/pi": K3, "1/K3": 1/K3, "K3^2": K3**2, "pi^2/K3^2": pi**2/K3**2, "pi/K3": pi/K3,
     "K4=G(1/4)^2/sqrt(pi)": K4, "pi/K4^2": pi/K4**2, "K4^2": K4**2, "pi s3": pi*s3, "pi/s3": pi/s3, "log3": mp.log(3)}
T = json.load(open("bf_runs/track_a/survivors.json"))
T.append({"a": [-3, 10, 4], "b": [0, 0, 16, -8, -3], "x80": "F1"})
import bf_search as BF
res = []
for t in T:
    x = BF.cf_mp(t["a"], t["b"], 4000, 130); mp.mp.dps = 110
    hit = None
    for name, c in C.items():
        r = mp.pslq([1, x, c, x * c], maxcoeff=10**6, maxsteps=10**5)
        if r and (r[2] or r[3]) and (r[1] or r[3]):
            hit = (name, r); break
    if not hit:
        for (n1, c1), (n2, c2) in itertools.combinations(list(C.items())[:5], 2):
            r = mp.pslq([1, x, c1, x * c1, c2, x * c2], maxcoeff=10**4, maxsteps=10**5)
            if r and r[1:].count(0) < 4 and any(r[2:]):
                hit = (n1 + " & " + n2, r); break
    res.append({"a": t["a"], "b": t["b"], "hit": hit and [hit[0], [int(v) for v in hit[1]]]})
    if hit: print(t["a"], t["b"], hit, flush=True)
json.dump(res, open("bf_runs/track_a/gamma_hits.json", "w"), indent=0)
print("explained", sum(1 for r in res if r["hit"]), "/", len(res))
