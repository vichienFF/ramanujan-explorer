# Step 3: Riemann schemes of the 15 irreducible cases (singular points + exponents), to look for structure / pullbacks
import json
from ore_algebra import OreAlgebra
R.<z> = QQ['z']; A.<Dz> = OreAlgebra(R); th = z*Dz
T = json.load(open("bf_runs/track_a/irreducible15.json"))
out = []
for i, t in enumerate(T):
    ap = sum(QQ(c)*(th+1)^j for j, c in enumerate(t["a"])); bp = sum(QQ(c)*(th+2)^j for j, c in enumerate(t["b"]))
    L = th^2*(th-1)^2 - z*ap*th^2 - z^2*bp
    lc = L.leading_coefficient()
    sch = {}
    for p, m in lc.factor():
        ind = L.indicial_polynomial(p)
        sch[str(p)] = str(ind.factor())
    ind_inf = L.indicial_polynomial(1/z)
    sch["inf"] = str(ind_inf.factor())
    out.append({"i": i, "a": t["a"], "b": t["b"], "scheme": sch})
    print(i, t["a"], "| sing:", list(sch.keys()), flush=True)
    for k, v in sch.items(): print("     ", k, ":", v, flush=True)
json.dump(out, open("bf_runs/track_a/scheme15.json", "w"), indent=0)
