# HAND proof check for S_a = sum chi(D4) = A' + B', A' = sum chi(H(s,m)) = 2q, B' = sum chi(s H(s,m)) = (1+phi(-1))q + chi(3) (char not 2,3,5).  # LOCAL-OK: seconds
# Hand steps: s=1 line gives -phi(-1) in both; node projection H=(s-1)^2 L_k, L_k linear (A') / s*L_k quadratic with roots 0, b/a (B'); special k: a=0 at k=1,-2; b=0 at k=2,-3; Jacobsthal sums of k^2-5 with removed points.
# CONTROL (independent): S_a brute force via D4 (p4_charsum definition) equals A'+B' (change of variables of Step 4v) and the read-off form (3+f1)q+f1f3.
import sympy as sp
def chi(a, q): a %= q; return 0 if a == 0 else (1 if pow(a, (q-1)//2, q) == 1 else -1)
def H(s, m): return m**3+8*m*m-3*m*s*s+6*m*s+13*m+2*s**3+2*s*s-10*s+6
def D4(u, v): return 7*u**4 + 12*u**3*v + 12*u**3 + 12*u**2*v**2 - 4*u**2*v + 12*u**2 - 16*v**3 + 32*v**2 - 16*v
s, k = sp.symbols('s k'); L = (k-1)**2*(k+2)*s - (k-2)*(k+3)**2
c0 = sp.expand(H(s, -4+k*(s-1)) - (s-1)**2*L) == 0
ok = c0
for q in (7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43):
    A1 = sum(chi(H(x, y), q) for x in range(q) for y in range(q)); B1 = sum(chi(x*H(x, y), q) for x in range(q) for y in range(q))
    Sa = sum(chi(D4(u, v), q) for u in range(q) for v in range(q)); f1 = chi(-1, q); c3 = chi(3, q)
    ok &= A1 == 2*q and B1 == (1+f1)*q + c3 and Sa == A1 + B1 == (3+f1)*q + f1*chi(-3, q)
print("H=(s-1)^2 L_k:", c0, "| A'=2q, B'=(1+f1)q+chi(3), S_a=A'+B'=(3+f1)q+f1f3 on 11 primes 7..43:", ok)
