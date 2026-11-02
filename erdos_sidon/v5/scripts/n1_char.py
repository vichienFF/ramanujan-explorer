r"""N1 (NEW_MATH_PROGRAM): exact character expansion of N(rho) and of its variance.  # LOCAL-OK: small q, seconds
Claims to test (INFERENCE, derived by hand 2026-10-28):
 (A) N(rho) = (q^3-q)/m - (q-2)(m-1)/m + (1/m) sum_{j != 0} J(chi_j, chi_{-j rho}),   J(a,b) = sum_{y in K} a(1-y) b(y),
     chi_j(g^k) = e(jk/m) characters of K^*/F^* (order | m), with chi(0) = 0.  N(rho) = #{y in K \ F : log(1-y) == rho log y (mod m)} (Zech form).
 (B) sum_rho |N(rho) - Nbar|^2 = (1/m^2) sum_{lambda} C(lambda) over the m-1 'directions', where for prime m
     C(lambda) = sum_{j != 0} sum_k J(chi_j, chi_k) conj(J(chi_{lambda j}, chi_{lambda k}))  (substitution k = -j rho),
     and C(q) = C(q^2) = C(1) (Frobenius invariance of Jacobi sums) -> the |G| = 3 main term of the variance law.
Checks: (A) for every rho exactly (float tolerance on complex sums, compared with integer counts), (B) numerically, C(q)/C(1), C(q^2)/C(1)."""
import sys, cmath, itertools
def field(q):  # F_{q^3} for prime q via a primitive cubic; elements as tuples (c0,c1,c2), x^3 = a x^2 + b x + c
    for a, b, c in itertools.product(range(q), range(q), range(1, q)):
        def mul(u, v):
            r = [0] * 5
            for i in range(3):
                for j in range(3): r[i + j] += u[i] * v[j]
            for d in (4, 3):
                t = r[d]; r[d] = 0; r[d - 1] += a * t; r[d - 2] += b * t; r[d - 3] += c * t
            return tuple(x % q for x in r[:3])
        g = (0, 1, 0); cur = (1, 0, 0); log = {}
        for k in range(q ** 3 - 1):
            if cur in log: break
            log[cur] = k; cur = mul(cur, g)
        if len(log) == q ** 3 - 1: return log
    raise ValueError
def run(q):
    log = field(q); Q3 = q ** 3; m = q * q + q + 1; el = list(log.keys()) + [(0, 0, 0)]
    one = (1, 0, 0)
    sub = lambda u, v: tuple((x - y) % q for x, y in zip(u, v))
    inF = lambda u: u[1] == 0 and u[2] == 0
    L = {u: log[u] % m for u in log}  # log in K^*/F^*
    def chi(j, u): return 0 if u == (0, 0, 0) else cmath.exp(2j * cmath.pi * j * L[u] / m)
    pairs = [(L[sub(one, y)], L[y]) for y in log if not inF(y) and sub(one, y) in log]  # y in K\F (then 1-y != 0)
    Nz = [sum(1 for a, b in pairs if (a - r * b) % m == 0) for r in range(m)]
    # Jacobi sums over all y in K (y = 0, 1 give 0 for nontrivial chars; trivial char: chi_0(0) = 0 convention)
    allpairs = [(sub(one, y), y) for y in log if sub(one, y) in log]
    J = {}
    def Jac(j, k):
        key = (j % m, k % m)
        if key not in J: J[key] = sum(chi(j, a) * chi(k, b) for a, b in allpairs)
        return J[key]
    errA = 0.0
    for r in range(m):
        val = (Q3 - q) / m - (q - 2) * (m - 1) / m + sum(Jac(j, -j * r) for j in range(1, m)) / m
        errA = max(errA, abs(val - Nz[r]))
    Nbar = sum(Nz) / m; var = sum((x - Nbar) ** 2 for x in Nz)
    C = {lam: sum(Jac(j, k) * Jac(lam * j, lam * k).conjugate() for j in range(1, m) for k in range(m)) for lam in (1, q % m, q * q % m)}
    print('q=%d m=%d  (A) max |formula - count| = %.2e   var = %.3f   C(q)/C(1) = %s  C(q^2)/C(1) = %s' % (
        q, m, errA, var, complex(round((C[q % m] / C[1]).real, 9), round((C[q % m] / C[1]).imag, 9)),
        complex(round((C[q * q % m] / C[1]).real, 9), round((C[q * q % m] / C[1]).imag, 9))))
if __name__ == '__main__':
    for q in map(int, sys.argv[1:]): run(q)
