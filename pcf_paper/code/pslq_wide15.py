"""Step 3: wide PSLQ on the 15 cases - Mobius of one constant (<= 1e6) and two constants [1,c1,c2,x,xc1,xc2] (<= 1e4), 90 digits.
Pairs of constants that are rationally related are skipped (avoids spurious pi*sqrt3 vs pi/sqrt3 hits) and x must enter the relation."""
import itertools, json
import mpmath as mp
import bf_search as BF
mp.mp.dps = 90
g3, g4, pi, s2, s3 = mp.gamma(mp.mpf(1)/3), mp.gamma(mp.mpf(1)/4), mp.pi, mp.sqrt(2), mp.sqrt(3)
C = {"pi": pi, "pi^2": pi**2, "pi s2": pi*s2, "pi s3": pi*s3, "log2": mp.log(2), "log3": mp.log(3), "log5": mp.log(5),
     "zeta3": mp.zeta(3), "G": mp.catalan, "s3 L2chi3": s3*(mp.zeta(2, mp.mpf(1)/3) - mp.zeta(2, mp.mpf(2)/3))/9,
     "K3": g3**3*s3/pi, "K3b": pi**2/g3**3, "K4": g4**2/mp.sqrt(pi), "K4b": pi**(1.5)/g4**2, "log(1+s2)": mp.log(1+s2),
     "log phi": mp.log((1+mp.sqrt(5))/2), "pi s5": pi*mp.sqrt(5), "e": mp.e, "euler": mp.euler, "pi log2": pi*mp.log(2)}
pairs = []
for (n1, c1), (n2, c2) in itertools.combinations(C.items(), 2):
    r = mp.pslq([1, c1, c2, c1*c2], maxcoeff=10**4, maxsteps=10**4)
    if not r: pairs.append((n1, c1, n2, c2))
print("constants", len(C), "independent pairs", len(pairs), flush=True)
T = json.load(open("bf_runs/track_a/irreducible15.json")); res = []
for i, t in enumerate(T):
    x = BF.cf_mp(t["a"], t["b"], 4000, 110); mp.mp.dps = 90; hit = None
    for n1, c1 in C.items():
        r = mp.pslq([1, x, c1, x*c1], maxcoeff=10**6, maxsteps=10**5)
        if r and (r[1] or r[3]) and (r[2] or r[3]): hit = [n1, [int(v) for v in r]]; break
    if not hit:
        for n1, c1, n2, c2 in pairs:
            r = mp.pslq([1, c1, c2, x, x*c1, x*c2], maxcoeff=10**4, maxsteps=10**5)
            if r and any(r[3:]) and any(r[1:3] + r[4:]): hit = [n1 + " & " + n2, [int(v) for v in r]]; break
    res.append({"i": i, "hit": hit}); print(i, hit, flush=True)
json.dump(res, open("bf_runs/track_a/pslq_wide15.json", "w"), indent=0)
print("explained", sum(1 for r in res if r["hit"]), "/", len(res))
