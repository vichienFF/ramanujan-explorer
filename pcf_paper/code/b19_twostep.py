"""Batch 19A (PLAN_BATCH19_2026-10-08): two-step coboundary  M1(n) U(n) = lambda(n) U(n-1) M2(2n-s) M2(2n-s-1)
(row convention; column variant M1(n) U(n-1) = lambda U(n) N(n) also tried), M(n) = [[0, b(n)], [1, a(n)]].
Usage: python b19_twostep.py control | C1 | C7 | C14      (partner forms from the verification files; timer TLIM_S)."""
import itertools, json, os, sys, time
import sympy as sp
n = sp.Symbol("n"); H = os.path.dirname(os.path.abspath(__file__)); DMAX = int(os.environ.get("DMAX", "4"))
T0 = time.time(); TLIM_S = float(os.environ.get("TLIM_S", "1e12")); OUTDIR = os.environ.get("OUTDIR", H)
KAPS = (1, -1, 2, -2, 3, -3, 4, -4, 6, -6, 8, -8, 9, -9, 12, -12, 16, -16); SHIFTS = (-2, -1, 0, 1, 2, 3)

def M(a, b, m): return sp.Matrix([[0, b.subs(n, m)], [1, a.subs(n, m)]])

def lin_factors(p):
    c, fl = sp.factor_list(sp.expand(p), n); out = []
    for f, e in fl:
        if sp.degree(f, n) == 1: out += [f] * e
    return out

def lambdas(polys):
    facs = [f for p in polys for f in lin_factors(p)]; seen = set()
    for k in range(0, 4):
        for sub in itertools.combinations(range(len(facs)), k):
            base = sp.expand(sp.prod([facs[i] for i in sub]) if sub else sp.Integer(1))
            for kap in KAPS:
                lam = sp.expand(kap * base)
                if lam not in seen: seen.add(lam); yield lam

def solve(a1, b1, a2, b2):
    cs = sp.symbols(f"u0:{4 * (DMAX + 1)}")
    U = sp.Matrix(2, 2, [sum(cs[e * (DMAX + 1) + j] * n ** j for j in range(DMAX + 1)) for e in range(4)])
    M1 = M(a1, b1, n)
    for s, form in itertools.product(SHIFTS, ("row", "col")):
        N = (M(a2, b2, 2 * n - s) * M(a2, b2, 2 * n - s - 1)) if form == "row" else (M(a2, b2, 2 * n - s - 1) * M(a2, b2, 2 * n - s))
        N = N.applyfunc(sp.expand)
        lhs = M1 * U if form == "row" else M1 * U.subs(n, n - 1)
        for lam in lambdas([b1, b2.subs(n, 2 * n - s), b2.subs(n, 2 * n - s - 1)]):
            if time.time() - T0 > TLIM_S: return {"timeout": True}
            rhs = lam * U.subs(n, n - 1) * N if form == "row" else lam * U * N
            E = (lhs - rhs).applyfunc(sp.expand)
            eqs = [c for e in E for c in sp.Poly(e, n).all_coeffs()]
            A, _ = sp.linear_eq_to_matrix(eqs, cs); ns = A.nullspace()
            if not ns: continue
            Us = U.subs(dict(zip(cs, ns[0]))).applyfunc(sp.expand)
            if sp.expand(Us.det()) == 0: continue
            chk = ((M1 * Us - lam * Us.subs(n, n - 1) * N) if form == "row" else (M1 * Us.subs(n, n - 1) - lam * Us * N)).applyfunc(sp.expand)
            if all(e == 0 for e in chk):
                return {"s": s, "form": form, "lambda": str(lam), "U": [[str(Us[i, j]) for j in range(2)] for i in range(2)],
                        "detU": str(sp.factor(Us.det())), "identity_verified": True}
    return None

def poly(c): return sum(sp.Integer(v) * n ** k for k, v in enumerate(c))

def contraction(a, b):
    """even part of a PCF as a PCF: from the two-step matrix product, a'(n) = trace-type expression (standard contraction)."""
    # u_{2n} in terms of u_{2n-2}, u_{2n-4}: A(n) u_{2n-2} + B(n) u_{2n-4}
    a2n, a2n1, a2n2 = a.subs(n, 2 * n), a.subs(n, 2 * n - 1), a.subs(n, 2 * n - 2)
    b2n, b2n1 = b.subs(n, 2 * n), b.subs(n, 2 * n - 1)
    A = sp.cancel(a2n * a2n1 + b2n + b2n1 * a2n / a2n2); B = sp.cancel(-b2n1 * b.subs(n, 2 * n - 2) * a2n / a2n2)
    return sp.expand(A * a2n2), sp.expand(B * a2n2 * a.subs(n, 2 * n - 4))   # cleared denominators (equivalence scaling)

if __name__ == "__main__":
    job = sys.argv[1]; out = {"job": job}
    if job == "control":
        a2, b2 = 2 * n + 1, (2 * n + 1) * (3 * n + 1)
        ac, bc = contraction(a2, b2); out["control_pcf"] = [str(ac), str(bc)]
        out["positive"] = solve(ac, bc, a2, b2)
        C = json.load(open(os.path.join(H, "bf_runs", "track_a", "irreducible15.json")))
        out["negative"] = solve(poly(C[2]["a"]), poly(C[2]["b"]), 2 * n + 3, sp.expand((2 * n + 1) * (5 * n + 2)))
        print("positive", out["positive"], "\nnegative", out["negative"], flush=True)
    else:
        i = int(job[1:]); C = json.load(open(os.path.join(H, "bf_runs", "track_a", "irreducible15.json")))
        if i == 1: forms = [{"a": [-1, 2], "b": [105, -88, 15], "mobius": [-5, -4, 5, 0]}]
        else: forms = [v for v in json.load(open(os.path.join(H, "b13_verify.json"))) if v["C"] == i and v["digits_agree"] > 150]
        out["attempts"] = []
        for f in forms:
            r = solve(poly(C[i]["a"]), poly(C[i]["b"]), poly(f["a"]), poly(f["b"]))
            out["attempts"].append({"partner_a": f["a"], "partner_b": f["b"], "result": r})
            print(job, f["a"], f["b"], "->", ("TIMEOUT" if r and r.get("timeout") else "PROVEN") if r else "not found", r, flush=True)
            json.dump(out, open(os.path.join(OUTDIR, f"b19_{job}.json"), "w"), indent=1)
            if r: break
    json.dump(out, open(os.path.join(OUTDIR, f"b19_{job}.json"), "w"), indent=1)
