"""สร้างชุดตัวเลขสำหรับ E1 (R2_PLAN.md) แบบกำหนดตายตัว — seed 20260928 · รันครั้งเดียวก่อน commit แผน"""
import json, random, sys
import mpmath as mp
sys.argv = ["x"]
import bf_search as B

mp.mp.dps = 60
CAL = [  # (ชื่อ, นิพจน์ที่ใช้คำนวณ) — ผู้เล่นเห็นแค่ตัวเลข 30 หลัก
    ("pi", "(3+pi)/(4-pi)"), ("log2", "2/(5-3*log(2))"), ("zeta3", "8/(7*zeta(3))"),
    ("catalan", "(1+2*catalan)/(2*catalan)"), ("lemniscate", "4*sqrt(2*pi)/gamma(mpf(1)/4)**2"),
    ("L2_chi3", "18/(zeta(2, mpf(1)/3) - zeta(2, mpf(2)/3))"), ("gamma13", "gamma(mpf(1)/3)/2 + 1"),
    ("gauss", "(1+1/agm(1,sqrt(2)))/(1-1/agm(1,sqrt(2)))"), ("pi_sqrt3", "6/(pi*sqrt(3)) + 1"),
    ("log5", "log(5)/(1+log(5))"),
]
ns = {k: getattr(mp, k) for k in dir(mp) if not k.startswith("_")}
cal = [{"id": f"C{i+1}", "value": mp.nstr(eval(e, {"__builtins__": {}}, ns), 30), "answer_hidden": e, "family": f}
       for i, (f, e) in enumerate(CAL)]

# ชุดค้นพบ: PCF ลู่เข้าเร็วที่ไม่ตรงค่าคงที่อ้างอิง 36 ตัว และไม่ใช่จำนวนพีชคณิตดีกรี ≤ 4
B.use_const_set("ext")
cv = B.const_values(60)
rnd = random.Random(20260928)
lin = [(k, t) for k in (1, 2, 3, 4) for t in range(-4, 5) if not (k > 1 and t % k == 0 and t != 0)]
disc, tries = [], 0
while len(disc) < 10 and tries < 20000:
    tries += 1
    a = [rnd.randint(-14, 14) for _ in range(3)]
    if a[2] <= 0:
        continue
    b = [0.0]
    import numpy as np
    b = np.array([1.0])
    for k, t in rnd.sample(lin, 4):
        b = np.polynomial.polynomial.polymul(b, [t, k])
    sc = rnd.choice([1, -1, 2, -2])          # สเกลเดียวทั้งพหุนาม (b ยังเป็นผลคูณตัวประกอบเชิงเส้น)
    b = [int(round(x)) * sc for x in b]
    if any(x == 0 for x in [sum(c * n ** i for i, c in enumerate(b)) for n in range(1, 60)]):
        continue
    try:
        v1, v2 = B.cf_mp(a, b, 300, 50), B.cf_mp(a, b, 600, 50)
    except ZeroDivisionError:
        continue
    if not mp.isfinite(v2) or abs(v2) > 1e4 or abs(v2) < 1e-4 or abs(v1 - v2) > mp.mpf(10) ** -35:
        continue
    x = v2
    if mp.findpoly(x, 4, maxcoeff=200):      # จำนวนพีชคณิตง่าย → ตัดทิ้ง
        continue
    hit = False
    for c in cv.values():  # Möbius: p + q·c − r·x − s·c·x = 0 → ความสัมพันธ์จำนวนเต็มของ [1, c, x, c·x] (PSLQ)
        rel = mp.pslq([1, c, x, c * x], maxcoeff=200, maxsteps=5000)
        if rel and (rel[2] or rel[3]):
            hit = True; break
    if hit:
        continue
    disc.append({"id": f"D{len(disc)+1}", "value": mp.nstr(x, 30), "pcf_a": a, "pcf_b": b})
json.dump({"seed": 20260928, "calibration": cal}, open("R2_calibration.json", "w"), indent=1)
json.dump({"seed": 20260928, "tries": tries, "discovery": disc}, open("R2_discovery.json", "w"), indent=1)
print(len(cal), len(disc), tries)
