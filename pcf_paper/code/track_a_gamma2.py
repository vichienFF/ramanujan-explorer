"""Wide test: x = Mobius of c with c = Gamma(1/3)^(3j) pi^i sqrt3^h or Gamma(1/4)^(2j) pi^i sqrt2^h (j != 0, |j| <= 2, |i| <= 4, h in {0,1})
+ Mobius of two constants [1,x,c1,xc1,c2,xc2] (c from a natural set of 8) - targets: 345 survivors + the 23 earlier cases (incl. F1) - x recomputed to 130 digits"""
import itertools, json
import mpmath as mp
import bf_search as BF
mp.mp.dps = 110
g3, g4, pi = mp.gamma(mp.mpf(1)/3), mp.gamma(mp.mpf(1)/4), mp.pi
C = {}
for j in (-2, -1, 1, 2):
    for i in range(-4, 5):
        for h in (0, 1):
            C[f"G13^{3*j} pi^{i} s3^{h}"] = g3**(3*j) * pi**i * mp.sqrt(3)**h
            C[f"G14^{2*j} pi^{i} s2^{h}"] = g4**(2*j) * pi**i * mp.sqrt(2)**h
NAT = {"K3": g3**3*mp.sqrt(3)/pi, "1/K3": pi/(g3**3*mp.sqrt(3)), "K3^2/pi^2": (g3**3*mp.sqrt(3)/pi)**2/pi**2, "pi s3": pi*mp.sqrt(3),
       "pi/s3": pi/mp.sqrt(3), "log3": mp.log(3), "pi^2": pi**2, "L2chi3": (mp.zeta(2, mp.mpf(1)/3) - mp.zeta(2, mp.mpf(2)/3))/9}
T = [dict(t, src="survivor") for t in json.load(open("bf_runs/track_a/hyp_targets_k0.json")) + json.load(open("bf_runs/track_a/hyp_targets_k1.json")) + json.load(open("bf_runs/track_a/hyp_targets_k2.json"))]
T += [{"a": t[0], "b": t[1], "src": "known23"} for t in json.load(open("bf_runs/test_fr/final_candidates_23.json"))]
res = []
for t in T:
    x = BF.cf_mp(t["a"], t["b"], 4000, 130); mp.mp.dps = 110
    hit = None
    for name, c in C.items():
        r = mp.pslq([1, x, c, x*c], maxcoeff=10**5, maxsteps=10**5)
        if r and (r[2] or r[3]) and (r[1] or r[3]):
            hit = [name, [int(v) for v in r]]; break
    if not hit:
        for (n1, c1), (n2, c2) in itertools.combinations(NAT.items(), 2):
            r = mp.pslq([1, x, c1, x*c1, c2, x*c2], maxcoeff=10**4, maxsteps=10**5)
            if r and (r[1] or r[3] or r[5]) and (r[2] or r[3]) and (r[4] or r[5]):
                hit = [n1 + " & " + n2, [int(v) for v in r]]; break
    res.append({"a": t["a"], "b": t["b"], "src": t["src"], "hit": hit})
    if hit: print(t["src"], t["a"], t["b"], hit, flush=True)
json.dump(res, open("bf_runs/track_a/gamma2_hits.json", "w"), indent=0)
print("explained", sum(1 for r in res if r["hit"]), "/", len(res), flush=True)
