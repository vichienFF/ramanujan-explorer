"""Genus g(rho) of the universal curves C_{a,b,c} (via plane model G and genus_mono). Orbit reps by height."""
import sys, time, sympy as sp
from math import gcd
from irred_cert import eqs, s, t, r
from genus_mono import genus
HMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 5
seen = set()
for H in range(2, HMAX + 1):
    for u in range(-H, H + 1):
        for v in range(1, H + 1):
            if max(abs(u), v) != H or u == 0 or u == v or gcd(abs(u), v) != 1: continue
            trip = (u - v, v, -u); key = min(tuple(sorted(x)) for x in (trip, tuple(-z for z in trip)))
            if key in seen: continue
            seen.add(key)
            a_, c_, b_ = sorted(trip, key=abs, reverse=True)
            t0 = time.time(); e1, e2 = eqs(a_, b_, c_); R = sp.resultant(e1, e2, r)
            Gs = [g for g, m in sp.factor_list(R)[1] if sp.Poly(g, s, t).total_degree() > 1]
            if not Gs: print(f"H={H} rho={u}/{v} exps={key}: no curve (forbidden)", flush=True); continue
            for G in Gs:
                d = sp.Poly(G, s, t).total_degree()
                try: g, D, nb = genus(G)
                except Exception as ex: g, D, nb = None, None, str(ex)[:40]
                print(f"H={H} rho={u}/{v} exps={key} deg={d} genus={g} (plane bound {(d-1)*(d-2)//2}) sum|exp|={sum(map(abs,key))} {time.time()-t0:.0f}s", flush=True)
