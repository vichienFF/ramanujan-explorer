"""Bose / random ratio of 3-term relation counts (note, Section 2): per-q ratio = Bose count / mean of the null counts;
reported: mean of per-q ratios and a percentile bootstrap 95% interval (resampling primes q with replacement, 20000 draws, seed 1).
Usage: python relations_ratio_ci.py <folder with res_*.jsonl from release/erdos_sidon/data/relations_k3>"""
import glob, json, sys
import numpy as np
rows = [json.loads(l) for f in sorted(glob.glob(sys.argv[1] + "/res_*.jsonl")) for l in open(f) if l.strip()]
qs = sorted({r["q"] for r in rows})
ratio = []
for q in qs:
    b = [r["relations_k3"] for r in rows if r["q"] == q and r["kind"] == "bose"]
    n = [r["relations_k3"] for r in rows if r["q"] == q and r["kind"] == "null"]
    ratio.append(b[0] / np.mean(n))
ratio = np.array(ratio); rng = np.random.default_rng(1)
boot = np.array([rng.choice(ratio, len(ratio)).mean() for _ in range(20000)])
print(f"primes {qs[0]}..{qs[-1]} ({len(qs)}); mean per-q ratio {ratio.mean():.4f}; "
      f"bootstrap 95% [{np.percentile(boot, 2.5):.3f}, {np.percentile(boot, 97.5):.3f}]")
