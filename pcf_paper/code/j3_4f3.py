"""Batch 3 J3 (registered 417dee5): Riemann-scheme-guided 4F3 test for the 15 irreducible candidates (+ control G1).
a_i = exponents at infinity (Sage indicial roots alpha) + integer shifts in {-2..2}; b_j = 1 + shifts in {0,1,2};
w from finite nonzero singular points z1, z2: z1/z2, 1 - z1/z2 and their inverses / other order, keep |w| < 1.
x vs Mobius (|c| <= 12) of y in {F, F(a1+1)/F, F(b1+1)/F}: float-hash screen at 25 digits, verify at 120 digits."""
import itertools, json, math, re
from fractions import Fraction
import mpmath as mp
import bf_search as BF

def roots_of(fac):
    return [Fraction(-Fraction(m.group(1).replace(" ", ""))) if m.group(1) else Fraction(0)
            for m in re.finditer(r"\(alpha(?: ([+-] [\d/]+))?\)(?:\^(\d+))?", fac) for _ in range(int(m.group(2) or 1))]

def parse_root(t):
    s = t.replace(" ", ""); return -Fraction(s) if s else Fraction(0)

def inf_exponents(fac):
    out = []
    for m in re.finditer(r"\(alpha( [+-] [\d/]+)?\)(\^\d+)?", fac):
        r = parse_root(m.group(1) or ""); out += [r] * (int(m.group(2)[1:]) if m.group(2) else 1)
    return out

def wlist(z1, z2):
    r = Fraction(z1) / Fraction(z2); c = {r, 1 / r, 1 - r, 1 / (1 - r) if r != 1 else None, 1 - 1 / r, r / (r - 1) if r != 1 else None}
    return sorted({w for w in c if w is not None and 0 < abs(w) < 1}, key=float)

def mob_hash(x, R=12):
    H = {}; xf = float(x)
    for p, q, r, s in itertools.product(range(-R, R + 1), repeat=4):
        if p * s - q * r == 0 or abs(r + s * xf) < 1e-9: continue
        v = (p + q * xf) / (r + s * xf)
        if 1e-8 < abs(v) < 1e8: H.setdefault(round(v, 8), []).append((p, q, r, s))
    return H

def run(name, a, b, ainf, zs):
    mp.mp.dps = 130; x = BF.cf_mp(a, b, 4000, 130); mp.mp.dps = 25; H = mob_hash(x); hits, tested = [], 0
    for w in wlist(*zs):
        W = mp.mpf(w.numerator) / w.denominator
        for sh in itertools.product(range(-2, 3), repeat=4):
            A = [mp.mpf(Fraction(ai + k).numerator) / Fraction(ai + k).denominator for ai, k in zip(ainf, sh)]
            if any(ai == int(ai) and ai <= 0 for ai in A): continue
            for bs in {tuple(sorted(t)) for t in itertools.product((1, 2, 3), repeat=3)}:
                mp.mp.dps = 25
                try:
                    F = mp.hyper(A, list(bs), W); ys = {"F": F, "Fa": mp.hyper([A[0] + 1] + A[1:], list(bs), W) / F,
                                                       "Fb": mp.hyper(A, [bs[0] + 1] + list(bs[1:]), W) / F}
                except Exception:
                    continue
                tested += 1
                for kind, y in ys.items():
                    if not mp.isfinite(y) or abs(y) < 1e-8 or abs(y) > 1e8: continue
                    for m in H.get(round(float(y), 8), []):
                        mp.mp.dps = 120; Ah = [mp.mpf(Fraction(ai + k).numerator) / Fraction(ai + k).denominator for ai, k in zip(ainf, sh)]
                        Wh = mp.mpf(w.numerator) / w.denominator; Fh = mp.hyper(Ah, list(bs), Wh)
                        yh = {"F": Fh, "Fa": mp.hyper([Ah[0] + 1] + Ah[1:], list(bs), Wh) / Fh, "Fb": mp.hyper(Ah, [bs[0] + 1] + list(bs[1:]), Wh) / Fh}[kind]
                        p, q, r, s = m
                        if abs((p + q * x) / (r + s * x) - yh) < mp.mpf(10) ** -100:
                            hits.append(dict(w=str(w), a=[str(Fraction(ai + k)) for ai, k in zip(ainf, sh)], b=bs, kind=kind, mobius=m))
                        mp.mp.dps = 25
    print(name, "tested", tested, "hits", len(hits), hits[:2], flush=True)
    return dict(name=name, tested=tested, hits=hits)

if __name__ == "__main__":
    S = json.load(open("bf_runs/track_a/scheme15.json")); out = []
    # control G1 (Gamma-type limit): b roots -3, 5/2, 1/2, 1/3 -> alpha = root - 2 ; singular points -1/2, 1/6
    out.append(run("G1-control", [-3, 10, 4], [-15, 76, -93, -4, 12], [Fraction(-5), Fraction(1, 2), Fraction(-3, 2), Fraction(-5, 3)],
                   (Fraction(1, 6), Fraction(-1, 2))))
    for t in S:
        zs = [-Fraction(k.split(" ")[-1].replace("+", "-").replace("--", "")) if False else None for k in t["scheme"]]
        fin = []
        for k in t["scheme"]:
            if k in ("z", "inf"): continue
            m = re.match(r"z ([+-]) ([\d/]+)", k); fin.append(Fraction(m.group(2)) * (1 if m.group(1) == "-" else -1))
        out.append(run(f"C{t['i']}", t["a"], t["b"], inf_exponents(t["scheme"]["inf"]), tuple(fin)))
    json.dump(out, open("bf_runs/track_a/j3_4f3.json", "w"), indent=0, default=str)
    print("TOTAL hits", sum(len(o["hits"]) for o in out[1:]), "| control hits", len(out[0]["hits"]))
