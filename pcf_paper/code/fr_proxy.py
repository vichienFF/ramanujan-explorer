"""Cheap vectorised proxy for factorial reduction: count the primes l in PR dividing both p_N and q_N.
Generic PCF: probability ~1/l^2 per prime -> almost none. Meaningful PCF: the gcd grows factorially -> almost all divide."""
import numpy as np

PR = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]   # skip 2, 3 (often inherited from a constant scaling of b)


def fr_count(a_coef, B, N=60):
    """a_coef: tuple of a coefficients, B: array (m, deg+1) of b coefficients -> array: number of primes dividing both"""
    B = np.asarray(B, dtype=np.int64)
    m = B.shape[0]
    cnt = np.zeros(m, dtype=np.int32)
    for l in PR:
        Bl = B % l
        p1 = np.ones(m, np.int64); p0 = np.full(m, a_coef[0] % l, np.int64)
        q1 = np.zeros(m, np.int64); q0 = np.ones(m, np.int64)
        for n in range(1, N + 1):
            an = sum(c * n ** i for i, c in enumerate(a_coef)) % l
            bn = sum(Bl[:, i] * pow(n, i, l) for i in range(Bl.shape[1])) % l
            p1, p0 = p0, (an * p0 + bn * p1) % l
            q1, q0 = q0, (an * q0 + bn * q1) % l
        cnt += ((p0 == 0) & (q0 == 0)).astype(np.int32)
    return cnt


if __name__ == "__main__":
    import json
    ref = [([3, 11, 11], [0, 0, 0, 0, 1]), ([1, 3, 3], [0, 0, 0, 0, -2]), ([1, 5, 4], [0, 0, 1, -1, -2]),
           ([3, 10, 10], [0, 0, 0, 0, -9]), ([5, 27, 51, 34], [0, 0, 0, 0, 0, 0, -1])]
    for a, b in ref:
        print("ref", a, b, fr_count(tuple(a), [b])[0])
    for d in json.load(open("R2_discovery.json"))["discovery"]:
        print(d["id"], fr_count(tuple(d["pcf_a"]), [d["pcf_b"]])[0])
