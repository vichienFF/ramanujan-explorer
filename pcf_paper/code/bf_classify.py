"""
Classify brute-force hits: separate "Euler-type" PCFs (convertible to an ordinary series, hence easy to prove / usually known)
from the others (more interesting; novelty must be checked by hand / literature search).
Euler-type criterion: integer polynomials h1, h2 with b(n) = -h1(n)*h2(n) and a(n) = h1(n) + h2(n+1)
   (all factor splittings of b, divisor scalings, and h1/h2 swaps) - Bauer-Muir / Euler CF (arXiv 2308.02567)
Usage: python bf_classify.py <result dir> -> <dir>/classified.json
"""
import glob, itertools, json, os, sys
from collections import Counter, defaultdict
import sympy as S

n = S.Symbol("n")


def poly(c):
    return sum(int(v) * n ** i for i, v in enumerate(c))


def euler_type(a, b):
    A, B = S.expand(poly(a)), S.expand(poly(b))
    if B == 0:
        return False
    cont, fac = S.factor_list(B)
    items = []
    for f, e in fac:
        items += [f] * e
    divs = [d for d in S.divisors(abs(int(cont)))]
    for r in range(len(items) + 1):
        for idx in set(itertools.combinations(range(len(items)), r)):
            g1 = S.prod([items[i] for i in idx]) if idx else S.Integer(1)
            g2 = S.prod([items[i] for i in range(len(items)) if i not in idx]) if len(idx) < len(items) else S.Integer(1)
            for d in divs:
                for sg in (1, -1):
                    h1 = sg * d * g1
                    h2 = S.expand(-B / h1)
                    if not h2.is_polynomial(n):
                        continue
                    for x, y in ((h1, h2), (h2, h1)):
                        if S.expand(x + y.subs(n, n + 1) - A) == 0 or S.expand(x.subs(n, n + 1) + y - A) == 0:
                            return True
    return False


if __name__ == "__main__":
    d = sys.argv[1]
    H = []
    for f in glob.glob(os.path.join(d, "**", "units_*.jsonl"), recursive=True) + glob.glob(os.path.join(d, "unit_*.json")):
        for line in open(f):
            try:
                u = json.loads(line)
            except ValueError:
                continue
            H += [h for h in u["hits"] if h["status"] == "HIT" and not h.get("periodic_trivial")]
    seen, rows = set(), []
    for h in H:
        key = (tuple(h["a"]), tuple(h["b"]))
        if key in seen:
            continue
        seen.add(key)
        if [c for c in h["a"] if c][-1] < 0:   # a -> -a gives the negated value = same PCF
            continue
        h["euler"] = euler_type(h["a"], h["b"])
        rows.append(h)
    by = defaultdict(Counter)
    for h in rows:
        by[h["const"]]["euler" if h["euler"] else "non_euler"] += 1
    non = sorted([h for h in rows if not h["euler"]], key=lambda h: (h["const"], sum(map(abs, h["a"] + h["b"]))))
    json.dump({"counts": {k: dict(v) for k, v in by.items()}, "non_euler": non}, open(os.path.join(d, "classified.json"), "w"), indent=1)
    print({k: dict(v) for k, v in by.items()})
    for h in non[:60]:
        print(h["const"], "a=", h["a"], "b=", h["b"], "mob=", h["mobius"], S.factor(poly(h["b"])))
