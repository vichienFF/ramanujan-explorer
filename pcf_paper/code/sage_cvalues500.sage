# Identify C_P, C_Q separately: log|C| = integer combination of log Gamma(k/d'), log pi, log p (small p) - values to 500 digits
# Control: C_P of F1 must be a Gamma product (f_P is genuinely hypergeometric) - jsonl checkpoint
import json, os, time, mpmath
exec(preparse(open("sage_connect.sage").read().split('if __name__ == "__main__":')[0]))
mpmath.mp.dps = 160
T = [{"name": "F1", "a": [-3, 10, 4], "b": [0, 0, 16, -8, -3]},
     {"name": "G1", "a": [-3, 10, 4], "b": [-15, 76, -93, -4, 12]},
     {"name": "G2", "a": [-3, 10, 4], "b": [15, 26, -21, -20, 12]}]
T += [dict(name="C%d" % i, a=t["a"], b=t["b"]) for i, t in enumerate(json.load(open("bf_runs/track_a/irreducible15.json")))]
OUT = "bf_runs/track_a/cvalues500.jsonl"
done = {json.loads(l)["name"] for l in open(OUT)} if os.path.exists(OUT) else set()
def basis_for(d):
    B = [("log pi", mpmath.log(mpmath.pi))] + [("log %d" % p, mpmath.log(p)) for p in (2, 3, 5, 7, 13)]
    for dd in divisors(d):
        if dd < 3: continue
        for k in range(1, (dd + 1)//2):
            if gcd(k, dd) == 1: B.append(("logG(%d/%d)" % (k, dd), mpmath.log(mpmath.gamma(mpmath.mpf(k)/dd))))
    return B
for t in T:
    if t["name"] in done: continue
    t0 = time.time()
    M, b1, vP, vQ = x_from_connection(t["a"], t["b"], eps=RealField(1800)(10)^(-505))
    k = [j for j, m in enumerate(b1) if "^(" in str(m) and "log" not in str(m)]; k = k[0] if k else 0
    rho = QQ(str(b1[k]).split("^(")[1].rstrip(")"))
    rec = {"name": t["name"], "mono": str(b1[k]), "rho": str(rho)}
    for lab, v in (("CP", vP[k]), ("CQ", vQ[k])):
        rec[lab + "abs"] = str(abs(v).center()) if abs(v).rad() < RealField(1800)(10)^(-490) else None
    rec["sec"] = float(round(time.time() - t0, 1))
    open(OUT, "a").write(json.dumps(rec) + "\n")
    print(rec["name"], rec["mono"], bool(rec["CPabs"]), bool(rec["CQabs"]), rec["sec"], flush=True)
