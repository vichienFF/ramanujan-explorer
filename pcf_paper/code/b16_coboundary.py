"""Batch 16 (PLAN_BATCH16_2026-10-07): exact coboundary equivalence between a candidate PCF and its degree-(1,2) partner.
Find U(n) (2x2, polynomial entries deg <= DMAX) and lambda(n) with  M1(n) U(n-1) = lambda(n) U(n) M2(n - s),
M(n) = [[0, b(n)], [1, a(n)]]. For fixed (s, lambda) the system is linear in U's coefficients (exact over Q via sympy).
Usage: python b16_coboundary.py control | C0 | C7 | ... (partner forms from b12a/b13 verification files)."""
import itertools, json, os, sys, time
T0 = time.time(); TLIM_S = float(os.environ.get("TLIM_S", "1e12"))
import sympy as sp
n = sp.Symbol("n"); H = os.path.dirname(os.path.abspath(__file__)); DMAX = int(os.environ.get("DMAX", "3"))
KAPS = (1, -1, 2, -2, 3, -3, 4, -4, 6, -6, 8, -8, 9, -9, 12, -12) if os.environ.get("WIDE") else (1, -1, 2, -2, 3, -3, 4, -4, 6, -6)
NFAC = 4 if os.environ.get("WIDE") else 3
SHIFTS = (-2, -1, 0, 1, 2, 3) if os.environ.get("WIDE") else (-1, 0, 1, 2)

def M(a, b, m): return sp.Matrix([[0, b.subs(n, m)], [1, a.subs(n, m)]])

def lin_factors(p):
    c, fl = sp.factor_list(sp.expand(p), n); out = []
    for f, e in fl:
        if sp.degree(f, n) == 1: out += [f] * e
    return out

def lambdas(b1, b2s):
    facs = lin_factors(b1) + lin_factors(b2s); seen = set()
    for k in range(0, NFAC):
        for sub in itertools.combinations(range(len(facs)), k):
            base = sp.expand(sp.prod([facs[i] for i in sub]) if sub else sp.Integer(1))
            for kap in KAPS:
                lam = sp.expand(kap * base)
                if lam not in seen: seen.add(lam); yield lam

def solve(a1, b1, a2, b2):
    cs = sp.symbols(f"u0:{4 * (DMAX + 1)}")
    U = sp.Matrix(2, 2, [sum(cs[e * (DMAX + 1) + j] * n ** j for j in range(DMAX + 1)) for e in range(4)])
    for s, form in itertools.product(SHIFTS, ("row", "col")):
        M1 = M(a1, b1, n); M2 = M(a2, b2, n - s)
        # row-vector convention v_n = v_{n-1} M(n): M1(n) U(n) = lambda U(n-1) M2;  column form kept as alternative
        lhs, rhsU = (M1 * U, lambda lam: lam * U.subs(n, n - 1) * M2) if form == "row" else (M1 * U.subs(n, n - 1), lambda lam: lam * U * M2)
        for lam in lambdas(b1, b2.subs(n, n - s)):
            if time.time() - T0 > TLIM_S: return {"timeout": True, "reached_s": s, "form": form}
            E = (lhs - rhsU(lam)).applyfunc(sp.expand)
            eqs = [c for e in E for c in sp.Poly(e, n).all_coeffs()]
            A, _ = sp.linear_eq_to_matrix(eqs, cs); ns = A.nullspace()
            if not ns: continue
            sol = ns[0]; Us = U.subs(dict(zip(cs, sol))).applyfunc(sp.expand)
            if Us.det() == 0 or sp.expand(Us.det()) == 0: continue
            check = ((M1 * Us - lam * Us.subs(n, n - 1) * M2) if form == "row" else (M1 * Us.subs(n, n - 1) - lam * Us * M2)).applyfunc(sp.expand)
            if all(e == 0 for e in check):
                return {"s": s, "form": form, "lambda": str(lam), "U": [[str(Us[i, j]) for j in range(2)] for i in range(2)],
                        "detU": str(sp.factor(Us.det())), "identity_verified": True}
    return None

def poly(c): return sum(sp.Integer(v) * n ** k for k, v in enumerate(c))

if __name__ == "__main__":
    job = sys.argv[1]; out = {"job": job}
    if job == "control":
        a2, b2 = 2 * n + 3, (3 * n + 5) * (5 * n + 1); c = 2 * n + 1
        out["positive"] = solve(sp.expand(a2 * c), sp.expand(b2 * c * c.subs(n, n - 1)), a2, b2)
        C = json.load(open(os.path.join(H, "bf_runs", "track_a", "irreducible15.json")))
        out["negative"] = solve(poly(C[1]["a"]), poly(C[1]["b"]), n + 2, sp.expand((2 * n + 1) * (3 * n + 4)))
    else:
        i = int(job[1:]); C = json.load(open(os.path.join(H, "bf_runs", "track_a", "irreducible15.json")))
        V = json.load(open(os.path.join(H, "b13_verify.json" if i in (0, 7, 14) else "b12a_verify.json")))
        forms = [v for v in V if v["C"] == i and v["digits_agree"] > 150]
        out["attempts"] = []
        for f in forms:
            r = solve(poly(C[i]["a"]), poly(C[i]["b"]), poly(f["a"]), poly(f["b"]))
            out["attempts"].append({"partner_a": f["a"], "partner_b": f["b"], "mobius_numeric": f["mobius"], "result": r})
            print(job, f["a"], f["b"], "->", ("TIMEOUT" if r and r.get("timeout") else "PROVEN") if r else "not found", r, flush=True)
            json.dump(out, open(os.path.join(os.environ.get("OUTDIR", H), f"b16{os.environ.get('TAG', '')}_{job}.json"), "w"), indent=1)
            if r: break
    print(json.dumps(out, indent=1)); json.dump(out, open(os.path.join(H, f"b16{os.environ.get('TAG', '')}_{job}.json"), "w"), indent=1)
