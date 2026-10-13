"""Build b21B_targets.json: candidates + controls with x to 180 digits (Amendment 18-2 evaluator, depth up to 4,096,000);
random controls: seeded random reals (seed 2026101321) with the a, b of C2 and C12."""
import json, random, time, mpmath as mp, b20b_mechanism as M20
C = json.load(open("bf_runs/track_a/irreducible15.json")); out = {}
f = lambda c: (lambda m: sum(v * m ** j for j, v in enumerate(c)))
for i in (0, 1, 5, 7, 14, 2, 3, 4, 6, 8, 9, 12, 13):
    t = time.time(); x, d = M20.limit_mp(f(C[i]["a"]), f(C[i]["b"]), 180, 4096000)
    print(f"C{i}", "digits", d, "ok" if x is not None else "SLOW", f"{time.time()-t:.0f}s", flush=True)
    if x is not None: mp.mp.dps = 200; out[f"C{i}"] = {"a": C[i]["a"], "b": C[i]["b"], "x": mp.nstr(x, 190)}
rnd = random.Random(2026101321)
for i in (2, 12):
    mp.mp.dps = 200; x = mp.mpf(rnd.choice("+-") + str(rnd.randint(1, 59)) + "." + "".join(rnd.choice("0123456789") for _ in range(185)))
    out[f"RAND_C{i}"] = {"a": C[i]["a"], "b": C[i]["b"], "x": mp.nstr(x, 190)}
json.dump(out, open("b21B_targets.json", "w"), indent=1); print("targets", list(out))
