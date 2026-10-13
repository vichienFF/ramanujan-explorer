"""Verify the 15-1a match for C1 at 160 digits and try the Batch-16 coboundary proof.
Partner a(n) = 2n - 1, b(n) = 15n^2 - 88n + 105 = (3n - 5)(5n - 21); bf convention y = (p + q x)/(r + s x), (p,q,r,s) = (-5,-4,5,0)."""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [H, os.path.join(H, "..", "cmf")]
from deep_id import cf
import mpmath as mp, sympy as sp
import b16_coboundary as B
C = json.load(open(os.path.join(H, "bf_runs", "track_a", "irreducible15.json")))
x, _ = cf(C[1]["a"], C[1]["b"], 160); y, _ = cf([-1, 2], [105, -88, 15], 160)
mp.mp.dps = 170; pred = (-5 - 4 * x) / 5; d = float(-mp.log10(abs(pred - y) / abs(y)))
print("C1 agree", d, "digits", flush=True)
r = B.solve(B.poly(C[1]["a"]), B.poly(C[1]["b"]), 2 * B.n - 1, sp.expand((3 * B.n - 5) * (5 * B.n - 21)))
print("C1 proof:", "PROVEN" if r else "not found", r)
json.dump({"digits": d, "proof": r}, open(os.path.join(H, "b15_c1_verify.json"), "w"), indent=1)
