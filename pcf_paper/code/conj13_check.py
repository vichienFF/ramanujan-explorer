"""Check whether a PCF belongs to the family of Ben David et al. Conjecture 1.3 (d=2):
b_n = B·∏_{i=1..4}(n − x_i),  a_n = (B/m)·(n+1−x_i1)(n+1−x_i2) − m·(n−x_i3)(n−x_i4),  m ∈ Q\{0, ±√|B|}"""
import itertools, json, math, sys
import sympy as S
n = S.Symbol("n")


def in_conj13(a, b):
    A_ = sum(int(c) * n ** i for i, c in enumerate(a)); B_ = sum(int(c) * n ** i for i, c in enumerate(b))
    Bc = S.Poly(B_, n).LC(); roots = []
    for r, mult in S.roots(S.Poly(B_, n)).items():
        roots += [r] * mult
    if len(roots) != 4 or any(not r.is_rational for r in roots):
        return None
    A = S.Poly(A_, n).LC()
    disc = A * A + 4 * Bc
    sq = S.sqrt(disc)
    if not sq.is_rational:
        return None
    for m in {(-A + sq) / 2, (-A - sq) / 2}:
        if m == 0:
            continue
        for pair in itertools.combinations(range(4), 2):
            rest = [i for i in range(4) if i not in pair]
            cand = (Bc / m) * (n + 1 - roots[pair[0]]) * (n + 1 - roots[pair[1]]) - m * (n - roots[rest[0]]) * (n - roots[rest[1]])
            if S.expand(cand - A_) == 0:
                return {"m": str(m), "shifted_roots": [str(roots[i]) for i in pair], "other_roots": [str(roots[i]) for i in rest]}
    return False


if __name__ == "__main__":
    T = json.load(open(sys.argv[1]))
    res = [(t, in_conj13(t["a"], t["b"])) for t in T]
    print("in Conjecture-1.3 family:", sum(bool(r) for _, r in res), "/", len(res))
    for t, r in res[:6]:
        print(t["a"], t["b"], "->", r)
    json.dump([dict(t, conj13=r) for t, r in res], open(sys.argv[1].replace(".json", "_conj13.json"), "w"), indent=0)
