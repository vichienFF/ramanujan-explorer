# Step 3: the 306 cases that are not hidden Euler type (over Q) -> (a) factor the differential operator (after dividing by (n!)^2), (b) hypergeometric solutions over Q(sqrt(-3))
# checkpoint: one jsonl line per target (rerun = skip finished ones)
import json, os, time
from ore_algebra import OreAlgebra
R.<z> = QQ['z']; A.<Dz> = OreAlgebra(R); th = z*Dz
K.<s3> = QuadraticField(-3)
Rn.<n> = K['n']; S.<Sn> = OreAlgebra(Rn, 'Sn')
T = [t for t in json.load(open("bf_runs/track_a/hyper_check.json")) if not t["hyper_factor"]]
OUT = "bf_runs/track_a/classify.jsonl"
done = set()
if os.path.exists(OUT):
    for l in open(OUT):
        r = json.loads(l); done.add((tuple(r["a"]), tuple(r["b"])))
print("targets", len(T), "done", len(done), flush=True)
for i, t in enumerate(T):
    key = (tuple(t["a"]), tuple(t["b"]))
    if key in done: continue
    t0 = time.time()
    ap = sum(QQ(c)*(th+1)^j for j, c in enumerate(t["a"]))
    bp = sum(QQ(c)*(th+2)^j for j, c in enumerate(t["b"]))
    L = th^2*(th-1)^2 - z*ap*th^2 - z^2*bp
    rec = {"a": t["a"], "b": t["b"], "src": t["src"]}
    try:
        t1 = time.time(); F = L.factor(); rec["t_ode"] = float(round(time.time() - t1, 1))
        rec["ode_orders"] = [int(f.order()) for f in F]
    except Exception as e:
        rec["ode_orders"] = None; rec["ode_err"] = repr(e)[:150]
    rec["sec"] = float(round(time.time() - t0, 1))
    with open(OUT, "a") as fh:
        fh.write(json.dumps(rec) + "\n")
    print(i, t["src"], rec["ode_orders"], rec.get("t_ode"), flush=True)
print("DONE", flush=True)
