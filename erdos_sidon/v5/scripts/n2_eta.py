r"""PREDICTION (2026-10-30, before computing): the base change w^2=(p-1)(p-9) of the Gamma1(6) surface (fibres I6,I3,I2,I1; n2_surface.sage)  # LOCAL-OK: seconds
is the extremal K3 with fibres 3 I6 + 3 I2, whose weight-3 form should be eta(2t)^3 eta(6t)^3 (CM by Q(sqrt-3), level 12).
Test: its q-expansion coefficient a_p equals b_p of n2_cm.py (0 if p==2 mod 3, t^2-2p with even t, 4p=t^2+3m^2) for every prime 5<=p<=200.
CONTROL: a_1 = 1 and every even-index coefficient is 0 (series = q * g(q^2)); b_p formula re-derived independently here."""
def b(p):
    if p % 3 == 2: return 0
    for t in range(0, 2 * int(p**0.5) + 2, 2):
        r = 4 * p - t * t
        if r >= 0 and r % 3 == 0 and round((r // 3) ** 0.5) ** 2 == r // 3: return t * t - 2 * p


if __name__ == "__main__":  # import-safe (E43/E44: importers only need b())
    L = 202
    c = [0] * L; c[1] = 1
    for n in range(1, L):
        for step in (2 * n, 6 * n):
            for _ in range(3):  # multiply by (1 - q^step)
                for i in range(L - 1, step - 1, -1): c[i] -= c[i - step]
    assert c[1] == 1 and all(c[i] == 0 for i in range(0, L, 2)), 'CONTROL FAIL'
    print('CONTROL a_1=1, even coefficients 0: PASS ; first terms', [(i, c[i]) for i in range(1, 30) if c[i]])
    primes = [p for p in range(5, L) if all(p % d for d in range(2, int(p**0.5) + 1))]
    miss = [(p, c[p], b(p)) for p in primes if c[p] != b(p)]
    print('primes tested %d (5..%d): misses %s' % (len(primes), primes[-1], miss or 'none'))
