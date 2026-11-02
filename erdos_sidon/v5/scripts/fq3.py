r"""Shared F_{q^3} helper (2026-10-30; replaces the copies in n2_kloost/n2_pencil/n2_dev). Import-safe: no top-level work.
F_{q^3} = F_q[t]/(t^3 - t - k); Tr(a0 + a1 t + a2 t^2) = 3 a0 + 2 a2.
CONTROL (selftest): Tr is F_q-linear with Tr(1)=3; a * a^-1 = 1 for random a; Tr(a)^q-structure: #{[a] in P^2: Tr a = 0} = q+1."""
def field(q):
    k = next(k for k in range(1, q) if all((x**3 - x - k) % q for x in range(q)))
    def mul(u, v):
        p = [0] * 5
        for i in range(3):
            for j in range(3): p[i + j] += u[i] * v[j]
        for i in (4, 3): p[i - 2] += p[i]; p[i - 3] += k * p[i]; p[i] = 0
        return tuple(x % q for x in p[:3])
    def inv(u):
        r, b, n = (1, 0, 0), u, q**3 - 2
        while n:
            if n & 1: r = mul(r, b)
            b = mul(b, b); n >>= 1
        return r
    tr = lambda u: (3 * u[0] + 2 * u[2]) % q
    return mul, inv, tr
def p2_reps(q):
    return [(1, b, c) for b in range(q) for c in range(q)] + [(0, 1, c) for c in range(q)] + [(0, 0, 1)]
def tu_table(q):
    mul, inv, tr = field(q)
    return [(tr(u), tr(inv(u))) for u in p2_reps(q)]
def chi(a, q):
    a %= q
    return 0 if a == 0 else (1 if pow(a, (q - 1) // 2, q) == 1 else -1)
def selftest(q=11):
    import random
    mul, inv, tr = field(q); rnd = random.Random(1)
    for _ in range(50):
        u = tuple(rnd.randrange(q) for _ in range(3))
        if u != (0, 0, 0): assert mul(u, inv(u)) == (1, 0, 0)
    assert tr((1, 0, 0)) == 3 % q and sum(1 for T, U in tu_table(q) if T == 0) == q + 1
    return True
if __name__ == "__main__":
    print('fq3 CONTROL selftest', 'PASS' if selftest(5) and selftest(11) else 'FAIL')
