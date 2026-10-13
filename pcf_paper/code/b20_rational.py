"""Batch 20A (PLAN_BATCH20_2026-10-12): rational-lambda coboundary prover.
Find a polynomial 2x2 matrix V(n) (deg <= DMAX) with
   row form:  q(n) M1(n) V(n)   = kappa p(n) V(n-1) M2(n - s)
   col form:  q(n) M1(n) V(n-1) = kappa p(n) V(n)   M2(n - s)
M(n) = [[0, b(n)], [1, a(n)]], i.e. lambda = kappa p/q. p, q = products of linear factors of b1(n), b2(n - s) and their
shifts by -1, 0, +1 (p: 0..3 factors, q: 0..2 factors; q = 1 kept so that Batch-16 type proofs are also inside the box).
Necessary condition used to prune (exact, no loss): taking determinants, det V(n)/det V(n-1) must equal a fixed rational
function R(n) built from kappa, p, q, b1, b2; R must therefore be of the form D(n)/D(n-1) with D a polynomial of
degree <= 2*DMAX (checked by matching linear factors along integer shifts), and kappa is fixed by the leading coefficients.
Survivors: linear nullspace over Q (sympy), then the matrix identity is expanded symbolically (= proof).
Checkpoint: one jsonl line per (job, partner, s, form) sub-unit; time check inside the (p, q) loop (TLIM_H, default 8).
Usage: python b20_rational.py control | C1 | C5 | C7 | C14   [env DMAX=6, TLIM_H=8, OUT=b20_<job>.jsonl]"""
import itertools, json, os, sys, time
from fractions import Fraction
import sympy as sp
T0 = time.time(); TLIM = float(os.environ.get("TLIM_H", "8")) * 3600
n = sp.Symbol("n"); H = os.path.dirname(os.path.abspath(__file__)); DMAX = int(os.environ.get("DMAX", "6"))
KAPS = {Fraction(k) for k in (1, 2, 3, 4, 6, 8, 9, 12, 16, 18, 24, 27, 36)}
if os.environ.get("KAPS_RATIO"):        # Amendment 20-1: kappa = ratio of two list values (partner normalisation)
    KAPS = {Fraction(a, b) for a in KAPS for b in KAPS}
SHIFTS = range(-int(os.environ.get("SHIFT_MAX", "3")), int(os.environ.get("SHIFT_MAX", "3")) + 1)   # Batch 21: SHIFT_MAX=6

def M(a, b, m): return sp.Matrix([[0, b.subs(n, m)], [1, a.subs(n, m)]])
def poly(c): return sp.expand(sum(sp.Integer(v) * n ** k for k, v in enumerate(c)))

def lin_factors(p):
    """linear factors as (k, t) for k n + t, primitive with k > 0, with multiplicity; plus leading constant"""
    c, fl = sp.factor_list(sp.expand(p), n); out = []
    for f, e in fl:
        P = sp.Poly(f, n)
        if P.degree() != 1: return None
        k, t = (int(v) for v in P.all_coeffs())
        if k < 0: k, t, c = -k, -t, -c
        out += [(k, t)] * e
    return Fraction(int(sp.numer(c)), int(sp.denom(c))), out

def root(f): return Fraction(-f[1], f[0])            # k n + t = 0  at n = -t/k

def telescopes(num, den, maxdeg):
    """num, den: lists of linear factors (k, t). True if prod(num)/prod(den) = D(n)/D(n-1) * const for a polynomial D of
    degree <= maxdeg. Each factor of D with root r contributes root r upstairs and root r + 1 downstairs, so every
    upstairs root must pair with a downstairs root larger by a positive integer (greedy pairing per class r mod 1 and per k)."""
    num = sorted(num, key=root); den = sorted(den, key=root); deg = 0
    if len(num) != len(den): return False
    used = [False] * len(den)
    for f in sorted(num, key=lambda f: -root(f)):        # pair from the largest upstairs root
        best = None
        for j, g in enumerate(den):
            if used[j] or g[0] != f[0]: continue
            d = root(g) - root(f)
            if d.denominator == 1 and d > 0 and (best is None or d < root(den[best]) - root(f)): best = j
        if best is None: return False
        used[best] = True; deg += int(root(den[best]) - root(f))
    return deg <= maxdeg

def cancel(num, den):
    num, den = list(num), list(den)
    for f in list(num):
        if f in den: num.remove(f); den.remove(f)
    return num, den

def solve_one(a1, b1, a2, b2, s, form, qfix=None):
    """yield (p, q, kappa) passing the determinant test, then try the linear solve; returns the first proof or stats"""
    b2s = sp.expand(b2.subs(n, n - s)); L1, L2 = lin_factors(b1), lin_factors(b2s)
    if L1 is None or L2 is None: return {"err": "non-linear factor"}, 0
    (c1, F1), (c2, F2) = L1, L2
    LC1 = c1 * sp.prod([k for k, _ in F1]); LC2 = c2 * sp.prod([k for k, _ in F2])   # leading coefficients of b1, b2s
    LC1, LC2 = Fraction(LC1), Fraction(LC2)
    pool = sorted({(k, t + k * d) for (k, t) in F1 + F2 for d in (-1, 0, 1)})
    qs = [()] + [c for r in (1, 2) for c in itertools.combinations_with_replacement(pool, r)]
    if qfix is not None: qs = [qfix]
    ps = [c for r in range(0, 4) for c in itertools.combinations_with_replacement(pool, r)]
    cs = sp.symbols(f"v0:{4 * (DMAX + 1)}")
    V = sp.Matrix(2, 2, [sum(cs[e * (DMAX + 1) + j] * n ** j for j in range(DMAX + 1)) for e in range(4)])
    M1 = M(a1, b1, n); M2 = M(a2, b2, n - s); tried = 0
    for q in qs:
        for p in ps:
            if len(p) != len(q) + 1 or set(p) & set(q): continue          # degree balance (from det), coprime
            if time.time() - T0 > TLIM: return {"timeout": True}, tried
            lcp = 1; lcq = 1
            for f in p: lcp *= f[0]
            for f in q: lcq *= f[0]
            # row: detV(n)/detV(n-1) = kappa^2 p^2 b2s / (q^2 b1);  col: inverse
            k2 = Fraction(lcq * lcq) * LC1 / (Fraction(lcp * lcp) * LC2)      # kappa^2 forced by leading coefficients (both forms)
            num, den = (list(p) * 2 + F2, list(q) * 2 + F1)
            if form == "col": num, den = den, num
            if k2 <= 0: continue
            kr = Fraction(int(round(k2.numerator ** 0.5)), int(round(k2.denominator ** 0.5)))
            if kr * kr != k2 or kr not in KAPS: continue
            nu, de = cancel(num, den)
            if not telescopes(nu, de, 2 * DMAX): continue
            pe = sp.prod([f[0] * n + f[1] for f in p]) if p else sp.Integer(1)
            qe = sp.prod([f[0] * n + f[1] for f in q]) if q else sp.Integer(1)
            for kap in (kr, -kr):
                tried += 1; K = sp.Rational(kap.numerator, kap.denominator)
                if form == "row": E = (qe * M1 * V - K * pe * V.subs(n, n - 1) * M2)
                else: E = (qe * M1 * V.subs(n, n - 1) - K * pe * V * M2)
                eqs = [c for e in E.applyfunc(sp.expand) for c in sp.Poly(e, n).all_coeffs()]
                A, _ = sp.linear_eq_to_matrix(eqs, cs); ns = A.nullspace()
                for sol in ns:
                    Vs = V.subs(dict(zip(cs, sol))).applyfunc(sp.expand)
                    if sp.expand(Vs.det()) == 0: continue
                    chk = ((qe * M1 * Vs - K * pe * Vs.subs(n, n - 1) * M2) if form == "row" else
                           (qe * M1 * Vs.subs(n, n - 1) - K * pe * Vs * M2)).applyfunc(sp.expand)
                    if all(e == 0 for e in chk):
                        return {"proof": True, "s": s, "form": form, "lambda": str(sp.factor(K * pe / qe)),
                                "V": [[str(Vs[i, j]) for j in range(2)] for i in range(2)], "detV": str(sp.factor(Vs.det())),
                                "identity_verified": True}, tried
    return {"proof": False}, tried

def run(job, a1, b1, partners, out, qfix=None):
    done = set()
    if os.path.exists(out):
        for l in open(out): r = json.loads(l); done.add((r["job"], str(r["partner"]), r["s"], r["form"]))
    for (a2, b2) in partners:
        for s, form in itertools.product(SHIFTS, ("row", "col")):
            key = (job, str([a2, b2]), s, form)
            if key in done: continue
            if time.time() - T0 > TLIM: print("time limit", flush=True); return
            t = time.time(); r, tried = solve_one(a1, b1, poly(a2), poly(b2), s, form, qfix)
            rec = {"job": job, "partner": [a2, b2], "s": s, "form": form, "tried": tried, "sec": round(time.time() - t, 1), **r}
            open(out, "a").write(json.dumps(rec) + "\n")
            print(job, a2, b2, s, form, "tried", tried, "->", "PROOF " + r["lambda"] if r.get("proof") else r, f"{rec['sec']}s", flush=True)
            if r.get("timeout"): return
            if r.get("proof"): return                         # one proof per job is enough

C15 = None
def cand(i):
    global C15
    if C15 is None: C15 = json.load(open(os.path.join(H, "bf_runs", "track_a", "irreducible15.json")))
    return poly(C15[i]["a"]), poly(C15[i]["b"])

PARTNERS = {"C1": [([-1, 2], [105, -88, 15])],
            "C5": [([-3, 6], [36, -144, 135]), ([-6, 12], [144, -576, 540])],
            "C7": [([0, 2], [12, 44, 24]), ([0, 4], [48, 176, 96])],
            "C14": [([8, 2], [-28, -92, 80])],
            "C2": [([-8, 2], [-16, -8, 48]), ([-9, 1], [-22, -38, 12]), ([-16, 4], [-64, -32, 192])]}   # Batch 21B partners

if __name__ == "__main__":
    job = sys.argv[1]; out = os.environ.get("OUT", os.path.join(H, f"b20{os.environ.get('TAG', '')}_{job}.jsonl"))
    if job == "control":
        a1, b1 = cand(0)
        run("pos2_planted", a1, b1, [([3, 2], [5, 28, 15])], out, qfix=((3, 2),))      # q = 3n + 2 forced
        run("pos1_C0", a1, b1, [([3, 2], [5, 28, 15])], out)
        a1, b1 = cand(2); run("neg_C2_random", a1, b1, [([2, 1], [4, 11, 6])], out)    # b = (2n+1)(3n+4)
    else:
        a1, b1 = cand(int(job[1:])); run(job, a1, b1, PARTNERS[job], out)
