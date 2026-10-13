"""Check whether the PCF recurrence  u_n = a(n) u_{n-1} + b(n) u_{n-2}  has a hypergeometric solution (Petkovsek, sympy rsolve_hyper).
If so -> the PCF is equivalent to a series (generalised Euler type) -> its value is a hypergeometric series, not a new constant."""
import sympy as S
from sympy.solvers.recurr import rsolve_hyper

n = S.Symbol("n", integer=True)


def has_hyper(a, b):
    A = sum(int(c) * n ** i for i, c in enumerate(a))
    Bp = sum(int(c) * n ** i for i, c in enumerate(b))
    # u(n+2) - A(n+2) u(n+1) - B(n+2) u(n) = 0
    coeffs = [-Bp.subs(n, n + 2), -A.subs(n, n + 2), S.Integer(1)]
    try:
        sol = rsolve_hyper(coeffs, 0, n)
    except Exception as e:
        return "err:" + type(e).__name__
    return sol is not None and sol != 0


if __name__ == "__main__":
    import json, sys
    tests = {"Apery zeta2": ([3, 11, 11], [0, 0, 0, 0, 1]), "Catalan RM": ([1, 3, 3], [0, 0, 0, 0, -2]),
             "Brouncker 4/pi": ([1, 2], [0, 0, 1]), "lemniscate cand": ([1, 5, 4], [0, 0, 1, -1, -2])}
    for k, (a, b) in tests.items():
        print(k, has_hyper(a, b), flush=True)
    d = json.load(open("bf_runs/test_fr/mystery_stage3.json"))["mystery"]
    for m in d[:8]:
        print(m["a"], m["b"], has_hyper(m["a"], m["b"]), flush=True)
