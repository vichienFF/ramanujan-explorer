"""Batch 27 C3R-b verdicts exactly by PLAN_BATCH27_2026-10-15.md (commit 4dc8b6c)."""
import glob, json, numpy as np
R = [json.loads(l) for f in glob.glob("D:/Research_FlyBrain/math_explorer/kaggle_out_b27/rama-b27c3r/out/*.jsonl") for l in open(f) if l.strip()]
A = {(r["kind"], r["q"], r["C"]): r["R3_exact"] for r in map(json.loads, open("D:/Research_FlyBrain/math_explorer/erdos/c3r_a.jsonl"))}
BL = [293, 383, 677, 701, 743, 761, 773, 827, 839, 857, 911, 1091, 1097, 1163, 1181, 1193, 1217, 1373]
print("rows", len(R), "errors", sum("err" in r for r in R))
S = {r["q"]: r for r in R if r["kind"] == "singer"}; Nl = [r for r in R if r["kind"] == "null" and r["q"] in BL]
c1 = all(S[q]["forbidden_counts"] == [0, 0, 0] for q in BL); c2 = all(min(r["forbidden_counts"]) > 0 for r in Nl)
c3 = max(abs(S[41][f"R3_C{C}"] - A[("singer", 41, C)]) for C in (2, 3, 4, 5, 8))
print(f"controls: blind q present {sorted(S)==sorted(BL+[41])} ({len(S)} singer, {len(Nl)} null); forbidden=0 all Singer {c1}; null >0 {c2}; q41 max diff {c3:.1e} -> {'VALID' if c1 and c2 and c3<1e-9 else 'VOID'}")
npass = 0
for C in (2, 3, 4, 5, 8):
    M = np.mean([q * S[q][f"R3_C{C}"] for q in BL]); sd = np.std([r["q"] * r[f"R3_C{C}"] for r in Nl], ddof=1); sg = sd / np.sqrt(18)
    lo, hi = -1.5 / C - 3 * sg, -1.5 / C + 0.1 / C + 3 * sg; ok = lo <= M <= hi; npass += ok
    print(f"T1 C={C}: M={M:+.4f} (C*M={C*M:+.3f}) band [{lo:+.4f},{hi:+.4f}] {'PASS' if ok else 'FAIL'} | null sd {sd:.3f} | desc |CM+1.5|={abs(C*M+1.5):.3f} |CM+1.17|={abs(C*M+1.17):.3f} | singer sd {np.std([q*S[q][f'R3_C{C}'] for q in BL],ddof=1):.3f}")
print("T1:", "PASS" if npass >= 4 else "FAIL", f"({npass}/5)")
lq = np.log(BL)
for key in ("D_all", "D_mid"):
    e, b = np.polyfit(lq, np.log([S[q][key] for q in BL]), 1)
    en = np.polyfit(np.log([r["q"] for r in Nl]), np.log([r[key] for r in Nl]), 1)[0]
    print(f"T2 {key}: exponent {e:+.3f} -> {'PASS' if -0.65 <= e <= -0.35 else 'FAIL'} (null exponent {en:+.3f}, desc); sqrt(q)*D singer mean {np.mean([np.sqrt(q)*S[q][key] for q in BL]):.3f} null {np.mean([np.sqrt(r['q'])*r[key] for r in Nl]):.3f}")
