"""Lane B completeness check (LANE_B_PLAN rule 2): prints ONLY row counts, error rows, time-limit lines and run times.
Never prints statistic values. Usage: python check_complete.py <sealed kernel dir>"""
import glob, json, os, sys
d = sys.argv[1]; rows = errs = 0; secs = []; keys = set()
for f in sorted(glob.glob(os.path.join(d, "out", "*.jsonl"))):
    for l in open(f):
        if not l.strip(): continue
        r = json.loads(l); rows += 1; errs += "err" in r; secs.append(r.get("sec", 0) or 0)
        keys.add((r.get("kind"), r.get("q"), r.get("rep", 0)))
logs = glob.glob(os.path.join(d, "*.log")); tl = sum(open(x, encoding="utf-8", errors="ignore").read().count("time limit") for x in logs)
tb = sum(open(x, encoding="utf-8", errors="ignore").read().count("Traceback") for x in logs)
print(f"{d}: rows {rows}, distinct jobs {len(keys)}, error rows {errs}, time-limit lines {tl}, tracebacks {tb}, total job hours {sum(secs)/3600:.2f}")
