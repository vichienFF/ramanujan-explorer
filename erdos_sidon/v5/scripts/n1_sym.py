r"""AN-C9-N1 think-then-test: which maps on units lambda mod m preserve C(lambda)?  # LOCAL-OK: small q, seconds
Hand derivation (INFERENCE): C(q lambda) = C(lambda) (Frobenius) and C(1/lambda) = conj C(lambda) = C(lambda) (substitute j' = lambda j; C real)
=> C constant on orbits of H = <q, inversion> (size 6 generically) -> explains multiplicities divisible by 6.
Test: (1) verify both symmetries exactly-to-float; (2) count H-orbits vs distinct C values; (3) try extra candidate maps
(-lambda, 1-lambda, lambda/(lambda-1), lambda^2, lambda+1) for further hidden collapse.  Control: a random permutation must FAIL."""
import sys, random, numpy as np
sys.path.insert(0, 'D:/Research_FlyBrain/math_explorer/erdos/stepb')
from n1_char import field
def Cvals(q):
    log = field(q); m = q * q + q + 1; one = (1, 0, 0)
    sub = lambda u, v: tuple((x - y) % q for x, y in zip(u, v))
    H = np.zeros((m, m))
    for y in log:
        w = sub(one, y)
        if w in log: H[log[w] % m, log[y] % m] += 1
    J = np.fft.ifft2(H) * m * m; J[0, :] = 0
    idx = np.arange(m)
    return m, {l: np.sum(J * np.conj(J[np.ix_((l * idx) % m, (l * idx) % m)])).real for l in range(1, m)}
if __name__ == "__main__":
  pass
for q in map(int, sys.argv[1:] if __name__ == "__main__" else []):
    m, C = Cvals(q); C1 = C[1]; inv = lambda l: pow(l, -1, m)
    tol = 1e-7 * C1
    def holds(f):
        return all(abs(C[l] - C[f(l)]) < tol for l in C if f(l) % m != 0)
    seen, orbits = set(), []
    for l in C:
        if l in seen: continue
        orb, stack = set(), [l]
        while stack:
            x = stack.pop()
            if x in orb: continue
            orb.add(x); stack += [q * x % m, inv(x)]
        seen |= orb; orbits.append(orb)
    const = all(max(C[x] for x in o) - min(C[x] for x in o) < tol for o in orbits)
    vals = sorted({round(C[l] / C1, 6) for l in C})
    perm = list(C); random.seed(1); random.shuffle(perm); P = dict(zip(C, perm))
    cands = {'-l': lambda l: -l % m, '1-l': lambda l: (1 - l) % m, 'l/(l-1)': lambda l: l * inv((l - 1) % m) % m if (l - 1) % m else 0,
             'l^2': lambda l: l * l % m, 'l+1': lambda l: (l + 1) % m, 'CONTROL random': lambda l: P[l]}
    print('q=%d m=%d  C(ql)=C(l): %s  C(1/l)=C(l): %s  H-orbits=%d (const on all: %s)  distinct C values=%d  orbit sizes=%s' % (
        q, m, holds(lambda l: q * l % m), holds(inv), len(orbits), const, len(vals), sorted({len(o) for o in orbits})))
    print('   extra maps preserving C: %s' % {k: holds(f) for k, f in cands.items()}); sys.stdout.flush()
