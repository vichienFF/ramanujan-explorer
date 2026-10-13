"""OEIS novelty check for the 15 candidates (2026-10-06): (1) decimal digits of |x|, (2) reduced convergent denominators."""
import json, math, time, urllib.request, urllib.parse
T = json.load(open("bf_runs/track_a/irreducible15.json")); out = []
def q(s):
    url = "https://oeis.org/search?" + urllib.parse.urlencode({"q": s, "fmt": "json"})
    try:
        d = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "research-check"}), timeout=60).read())
        res = d if isinstance(d, list) else ((d or {}).get("results") or [])
        return [f"A{r['number']:06d} {r['name'][:60]}" for r in (res or [])][:3]
    except Exception as e:
        return [f"ERR {e!r}"[:80]]
for i, t in enumerate(T):
    x = t["x50"].lstrip("-"); dig = ",".join(c for c in x.replace(".", "")[:18])
    A = lambda n: sum(c * n ** k for k, c in enumerate(t["a"])); B = lambda n: sum(c * n ** k for k, c in enumerate(t["b"]))
    P0, P1, Q0, Q1 = 1, A(0), 0, 1; den = []
    for n in range(1, 10):
        P0, P1, Q0, Q1 = P1, A(n) * P1 + B(n) * P0, Q1, A(n) * Q1 + B(n) * Q0; den.append(abs(Q1 // math.gcd(P1, Q1)))
    r1 = q(dig); time.sleep(3); r2 = q(",".join(map(str, den[:8]))); time.sleep(3)
    out.append({"C": i, "digits": dig, "digits_hits": r1, "den": den[:8], "den_hits": r2}); print(i, r1, r2, flush=True)
json.dump(out, open("bf_runs/track_a/oeis_check.json", "w"), indent=1)
