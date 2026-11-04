"""Version 6: saved outputs for the prime-power checks of (N3) (math referee v6: the p = 7, 13 parity checks must ship with data).  # LOCAL-OK: ~10 min
Writes v6_pp.json in the gf_ncount format {"p^n": [[N1, N2, N3], seconds]}; evaluate with: python eval_gf.py v6_pp.json
CONTROL: the same Sage/brute-force values as gf_ncount.py (q = 9, 7, 49, 125).
"""
import sys, os, json, time
D = os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
exec(open('gf_ncount.py', encoding='utf-8').read().split("if __name__")[0])
ctl = Ns(3, 2) == (65, 60, 36) and Ns(7, 1) == (37, 26, 6) and Ns(7, 2)[2] == 2022 and Ns(5, 3)[2] == 14778
print('CONTROL (Sage/brute-force values q=9,7,49,125):', 'PASS' if ctl else 'FAIL', flush=True)
QS = ['7^2', '7^3', '7^4', '11^2', '13^2', '13^3', '13^4', '5^3', '5^5', '5^6']
res = {}
for a in QS:
    t = time.time(); res[a] = [list(Ns(*map(int, a.split('^')))), round(time.time() - t)]; print(a, res[a], flush=True)
json.dump(res, open('v6_pp.json', 'w'))
