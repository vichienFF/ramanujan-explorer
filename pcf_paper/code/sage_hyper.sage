# Check every case: does the recurrence have a hypergeometric solution (order-1 right factor)? If so = hidden Euler-type CF (limit = Mobius of a series)
import json
from ore_algebra import OreAlgebra
Rn.<n> = QQ['n']; S.<Sn> = OreAlgebra(Rn, 'Sn')
T = json.load(open("bf_runs/track_a/all_for_sage.json"))
out = []
for i, t in enumerate(T):
    a = sum(c*n^j for j, c in enumerate(t["a"])); b = sum(c*n^j for j, c in enumerate(t["b"]))
    Rec = Sn^2 - a(n=n+2)*Sn - b(n=n+2)
    try:
        rf = Rec.right_factors()
        flat = [g for f in rf for g in (f if isinstance(f, list) else [f])]
        hyp = [str(g) for g in flat if g.order() == 1]
    except Exception as e:
        hyp = None; print(i, "ERR", repr(e)[:120], flush=True)
    t["hyper_factor"] = hyp
    out.append(t)
    if i % 25 == 0: print(i, t["src"], bool(hyp), flush=True)
json.dump(out, open("bf_runs/track_a/hyper_check.json", "w"), indent=0)
from collections import Counter
print("RESULT", Counter((t["src"], bool(t["hyper_factor"])) for t in out))
