"""Batch 21A (PLAN_BATCH21_2026-10-13): oscillation band of a degree-(1,2) PCF, used to decide the last C12 partner.
Values P_n/Q_n at 200 log-spaced depths in [1e3, 1e6] and the 4 following depths (mpmath, 60 digits).
band = [min, max] over depths >= 1e4; early window [1e4, 2e4], late window [5e5, 1e6].
Decision for the C12 partner: REJECTED if the Mobius prediction lies outside the band widened by 10x its width;
CONFIRMED if late width < 1e-3 x early width and the prediction is inside; else UNRESOLVED.
Controls: (i) a = 2n+1, b = n^2 (4/pi): band < 1e-50; (ii) a = 2n+1, b = -2n^2 (elliptic): late width >= 1e-3 x early width."""
import json, os, sys
import mpmath as mp
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
DPS = 60; NMAX = 10 ** 6

def values(a, b):
    mp.mp.dps = DPS
    base = sorted({int(round(10 ** (3 + 3 * i / 199))) for i in range(200)})
    marks = sorted({m + j for m in base for j in range(5) if m + j <= NMAX})
    want = set(marks); out = {}
    p0, p1, q0, q1 = mp.mpf(1), mp.mpf(a(0)), mp.mpf(0), mp.mpf(1)
    for n in range(1, NMAX + 1):
        an, bn = a(n), b(n); p0, p1, q0, q1 = p1, an * p1 + bn * p0, q1, an * q1 + bn * q0
        if n % 32 == 0:
            s = max(abs(p1), abs(q1)); p0, p1, q0, q1 = p0 / s, p1 / s, q0 / s, q1 / s
        if n in want: out[n] = p1 / q1
    return out

def band(v, lo, hi):
    w = [x for n, x in v.items() if lo <= n <= hi]; return min(w), max(w)

def analyse(name, a, b):
    v = values(a, b); lo, hi = band(v, 10 ** 4, NMAX); e = band(v, 10 ** 4, 2 * 10 ** 4); l = band(v, 5 * 10 ** 5, NMAX)
    r = {"name": name, "band": [mp.nstr(lo, 25), mp.nstr(hi, 25)], "width": float(hi - lo), "early_width": float(e[1] - e[0]),
         "late_width": float(l[1] - l[0]), "n_values": len(v)}
    print(json.dumps(r), flush=True); return r, lo, hi

if __name__ == "__main__":
    out = {}
    r, lo, hi = analyse("control_i_4_over_pi", lambda n: 2 * n + 1, lambda n: n * n)
    r["pass"] = r["width"] < 1e-50 and abs(float(hi) - float(4 / mp.pi)) < 1e-40; out["control_i"] = r
    r, lo, hi = analyse("control_ii_elliptic", lambda n: 2 * n + 1, lambda n: -2 * n * n)
    r["pass"] = r["late_width"] >= 1e-3 * r["early_width"] and r["early_width"] > 0; out["control_ii"] = r
    r, lo, hi = analyse("C12_partner", lambda n: 14 * n - 7, lambda n: -54 * n * n + 261 * n - 81)
    import b18_mechanism as M                                   # C12 limit via the Amendment 18-2 evaluator (90 digits)
    x, d = M.limit_mp(lambda n: 4 * n * n + 10 * n - 3, lambda n: 675 + 210 * n - 397 * n ** 2 - 68 * n ** 3 + 60 * n ** 4, 60, 64000)
    mp.mp.dps = DPS; y = (-6 - 8 * x) / (8 - 7 * x); w = hi - lo
    inside_wide = (lo - 10 * w) <= y <= (hi + 10 * w); shrinks = r["late_width"] < 1e-3 * r["early_width"]
    r.update({"C12_x": mp.nstr(x, 30), "prediction": mp.nstr(y, 25), "distance_to_band": float(min(abs(y - lo), abs(y - hi))) if not (lo <= y <= hi) else 0.0,
              "shrinks": shrinks, "verdict": "REJECTED" if not inside_wide else ("CONFIRMED" if shrinks and lo <= y <= hi else "UNRESOLVED")})
    out["C12_partner"] = r; out["controls_ok"] = out["control_i"]["pass"] and out["control_ii"]["pass"]
    print("controls_ok", out["controls_ok"], "| verdict", r["verdict"], "| distance", r["distance_to_band"], "| band width", r["width"], flush=True)
    json.dump(out, open(os.path.join(H, "b21a_result.json"), "w"), indent=1)
