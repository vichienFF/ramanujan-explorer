# Step (i) of C-B: HAND claim B(q) = q - 1 + sum_{k in F_q} S_k, S_k = sum_x chi(x(x-e1(k))(x-e2(k))), for odd q with 5 not | q.  # LOCAL-OK: seconds
# Hand steps checked separately: (1) s=1 line gives q-2; (2) f_k(1) = 16(k^2-5); (3) x = A s maps f_k to the Legendre cubic, A=k(k-1)^2(k+2); (4) k in {0,1,-2}: both sums = -chi(-2), -1, -chi(-2).
# CONTROL (independent theory): sum_k chi(k^2-a) = -1 for a != 0 (Jacobsthal); KILL-TEST: q=5 must FAIL (5 = 0 there).
from sage.all import GF
def chi(q):
    F = GF(q, 'a'); sq = {x * x for x in F if x != 0}
    return F, (lambda v: 0 if v == 0 else (1 if v in sq else -1))
res = {}
for q in (5, 7, 9, 11, 13, 19, 27, 31, 49, 121, 125):
    F, c = chi(q); E = list(F)
    ctl = sum(c(k * k - 2) for k in E) == -1 and (q % 5 == 0 or sum(c(k * k - 5) for k in E) == -1)   # repro referee: no vacuous skip
    H = lambda s, m: m**3 + 8*m*m - 3*m*s*s + 6*m*s + 13*m + 2*s**3 + 2*s*s - 10*s + 6
    B = sum(c(s * m * H(s, m)) for s in E for m in E)
    Sk = {k: sum(c(x * (x - (k-1)**2*(k+2)*(k+4)) * (x - k*(k-2)*(k+3)**2)) for x in E) for k in E}
    rhs = q - 1 + sum(Sk.values())
    f = lambda k, s: s * (k * (s - 1) - 4) * ((k-1)**2*(k+2)*s - (k-2)*(k+3)**2)
    st2 = all(f(k, F(1)) == 16 * (k * k - 5) for k in E)
    st3 = all(sum(c(f(k, s)) for s in E) == Sk[k] for k in E if k * (k-1) * (k+2) != 0)
    c2 = c(F(-2)); st4 = [sum(c(f(F(k), s)) for s in E) for k in (0, 1, -2)] == [-c2, -1, -c2] == [Sk[F(0)], Sk[F(1)], Sk[F(-2)]]
    print('q=%d CONTROL Jacobsthal %s | step2 %s step3 %s step4 %s | B=%d rhs=%d -> %s' % (q, ctl, st2, st3, st4, B, rhs, 'EQUAL' if B == rhs else 'DIFFER'), flush=True)
