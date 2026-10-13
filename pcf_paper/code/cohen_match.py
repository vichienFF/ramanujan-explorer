"""Compare our candidates with Henri Cohen's database (arXiv 2409.06086 v4, CC-BY 4.0)
- reads only constant entries (starting with "[()->") whose a, b have period 1 - Cohen convention: a(0) + b(0)/(a(1) + b(1)/...)
- computes the limits itself (does not trust his closures), then Mobius comparison (coefficients <= R) with our values
- runs no GP code: polynomial expressions are parsed with sympy.sympify only"""
import itertools, json, re, sys
import mpmath as mp
import sympy as S

n = S.Symbol("n")
SRC = "external/cohen_pcf_db/CFfile2.tex"


def split_top(s):
    out, depth, cur = [], 0, ""
    for ch in s:
        if ch in "[(":
            depth += 1
        elif ch in "])":
            depth -= 1
        if ch == "," and depth == 0:
            out.append(cur); cur = ""
        else:
            cur += ch
    out.append(cur)
    return out


def parse_entries():
    lines = open(SRC, encoding="utf-8").read().split("\n")
    ents = []
    for i, L in enumerate(lines):
        if not L.startswith("[()->"):
            continue
        body = L.strip().rstrip(";")[1:-1]
        parts = split_top(body)
        if len(parts) < 2:
            continue
        ab = parts[1].strip()
        if not (ab.startswith("[[") and ab.endswith("]]")):
            continue
        A, B = split_top(ab[1:-1])
        A, B = A.strip()[1:-1], B.strip()[1:-1]
        if "[" in A or "[" in B:   # period 2 -> skip
            continue
        try:
            Ai = [S.sympify(x.replace("^", "**"), locals={"n": n}) for x in split_top(A)]
            Bi = [S.sympify(x.replace("^", "**"), locals={"n": n}) for x in split_top(B)]
        except Exception:
            continue
        if any(e.free_symbols - {n} for e in Ai + Bi):
            continue
        ents.append({"line": i + 1, "limit": parts[0].strip(), "A": Ai, "B": Bi,
                     "label": re.findall(r'"(\d+(?:\.\d+)+[A-Z]?)"', L)[:1]})
    return ents


def seq(lst, k):
    """Cohen-style sequence: [c0, c1, ..., poly(n)] -> value at k"""
    if k < len(lst) - 1:
        return lst[k]
    return lst[-1].subs(n, k) if hasattr(lst[-1], "subs") else lst[-1]


def value(e, depth):
    mp.mp.dps = 50
    fa = S.lambdify(n, e["A"][-1], "mpmath"); fb = S.lambdify(n, e["B"][-1], "mpmath")
    a = lambda k: mp.mpf(S.Rational(e["A"][k])) if k < len(e["A"]) - 1 else mp.mpf(fa(k))
    b = lambda k: mp.mpf(S.Rational(e["B"][k])) if k < len(e["B"]) - 1 else mp.mpf(fb(k))
    p1, p0, q1, q0 = mp.mpf(1), a(0), mp.mpf(0), mp.mpf(1)
    for k in range(1, depth + 1):
        ak, bk = a(k), b(k - 1)
        p1, p0, q1, q0 = p0, ak * p0 + bk * p1, q0, ak * q0 + bk * q1
        if k % 40 == 0:
            s = max(abs(p0), abs(q0)) or 1
            p1, p0, q1, q0 = p1 / s, p0 / s, q1 / s, q0 / s
    return p0 / q0 if q0 else None


if __name__ == "__main__":
    ents = parse_entries()
    print("parsed constant entries (period 1):", len(ents), flush=True)
    vals = []
    for e in ents:
        try:
            v1, v2 = value(e, 1500), value(e, 3000)
        except Exception:
            continue
        if v1 is None or v2 is None or not mp.isfinite(v2) or abs(v1 - v2) > mp.mpf(10) ** -25 * max(1, abs(v2)):
            continue
        vals.append((e, v2))
    print("converged:", len(vals), flush=True)
    targets = []
    for f in sys.argv[1:]:
        for t in json.load(open(f)):
            if "x80" in t:
                targets.append((f.split("/")[-1], t["a"], t["b"], mp.mpf(t["x80"][:45])))
    R = 6
    rng = range(-R, R + 1)
    H = {}
    for ti, (src, a, b, x) in enumerate(targets):
        xf = float(x)
        for p, q, r, s in itertools.product(rng, rng, rng, rng):
            if p * s - q * r == 0 or abs(r + s * xf) < 1e-9:
                continue
            H.setdefault(round((p + q * xf) / (r + s * xf), 10), []).append((ti, (p, q, r, s)))
    hits = []
    mp.mp.dps = 45
    for e, v in vals:
        for m in H.get(round(float(v), 10), []):
            ti, (p, q, r, s) = m
            x = targets[ti][3]
            if abs((p + q * x) / (r + s * x) - v) < mp.mpf(10) ** -25:
                hits.append({"target": targets[ti][:3], "cohen_line": e["line"], "cohen_label": e["label"],
                             "cohen_limit": e["limit"], "mobius": [p, q, r, s]})
    json.dump(hits, open("bf_runs/test_fr/cohen_hits.json", "w"), indent=0, default=str)
    print("targets", len(targets), "hits", len(hits), "distinct targets hit", len({str(h["target"]) for h in hits}))
    for h in hits[:15]:
        print(h["target"][1], h["target"][2], "->", h["cohen_label"], h["cohen_limit"][:60], h["mobius"])
