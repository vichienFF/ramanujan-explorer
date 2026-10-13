"""Linearly independent log-Gamma basis (relations from the Gamma multiplication/reflection formulas removed by adding one element at a time and checking with PSLQ)"""
import mpmath as mp
from math import gcd
def gamma_basis(d, dps=160):
    mp.mp.dps = dps
    B = [("log pi", mp.log(mp.pi))] + [("log %d" % p, mp.log(p)) for p in (2, 3, 5, 7, 13)]
    for dd in [x for x in range(3, d + 1) if d % x == 0]:
        for k in range(1, (dd + 1) // 2):
            if gcd(k, dd) != 1: continue
            v = mp.log(mp.gamma(mp.mpf(k) / dd))
            r = mp.pslq([v] + [b for _, b in B], maxcoeff=10**4, maxsteps=10**6)
            if not (r and r[0]): B.append(("logG(%d/%d)" % (k, dd), v))
    return B
def identify(logc, d, dps=160, maxcoeff=500):
    B = gamma_basis(d, dps)
    r = mp.pslq([logc] + [b for _, b in B], maxcoeff=maxcoeff, maxsteps=10**6)
    if r and r[0]:
        return {"coef_logC": int(r[0]), "terms": {B[i][0]: int(c) for i, c in enumerate(r[1:]) if c}}, len(B)
    return None, len(B)
if __name__ == "__main__":
    mp.mp.dps = 160
    for d, planted in [(60, mp.gamma(mp.mpf(7)/60)**2*mp.gamma(mp.mpf(1)/20)/mp.gamma(mp.mpf(11)/60)**3*mp.pi**(-mp.mpf(1)/2)*mp.mpf(3)**(mp.mpf(2)/5)),
                       (84, mp.gamma(mp.mpf(5)/84)*mp.gamma(mp.mpf(1)/12)/(mp.gamma(mp.mpf(25)/84)*mp.pi)*mp.mpf(7)**(mp.mpf(1)/3))]:
        res, n = identify(mp.log(planted), d)
        print("control d", d, "independent basis", n, "->", res)
