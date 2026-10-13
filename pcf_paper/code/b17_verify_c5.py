"""Verify the 17A match for C5 at 160 digits: partner a(n) = 6n - 3, b(n) = 9(3n-2)(5n-2) = 135n^2 - 144n + 36,
Mobius (p,q,r,s) = (-3, 1, -4, -1) in the bf convention y = (p + q x)/(r + s x)."""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, "..", "cmf"))
from deep_id import cf
import mpmath as mp
C = json.load(open(os.path.join(H, "bf_runs", "track_a", "irreducible15.json")))
x, _ = cf(C[5]["a"], C[5]["b"], 160)
for a2, b2, mob in (([-3, 6], [36, -144, 135], (-3, 1, -4, -1)), ([-6, 12], [144, -576, 540], (-6, 2, -4, -1))):
    y, _ = cf(a2, b2, 160); mp.mp.dps = 170; p, q, r, s = mob; pred = (p + q * x) / (r + s * x)
    print("C5 partner", a2, b2, "agree", float(-mp.log10(abs(pred - y) / abs(y))), "digits")
