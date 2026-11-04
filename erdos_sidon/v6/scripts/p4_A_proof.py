# HAND proof check for A = sum chi(m H(s,m)) = (1+phi(-1))q + chi(3) (char not 2,3,5); char 5: minus q.  # LOCAL-OK: seconds
# Symbolic: on m=-4+k(s-1), m*H = (s-1)^2 * g_k(s), g_k = (k(s-1)-4)*L_k(s); disc_s(g_k) = c*(e1-e2)^2 -> double root iff k=-1; g_k(1) = 16(k^2-5).
# CONTROL (independent): brute-force A at q=7,11,13 and char-5 values A(5)=4 (p4_ch5A.sage.py output) vs the closed form.
import sympy as sp
s, k, m = sp.symbols('s k m')
H = m**3+8*m*m-3*m*s*s+6*m*s+13*m+2*s**3+2*s*s-10*s+6
L = (k-1)**2*(k+2)*s - (k-2)*(k+3)**2; g = (k*(s-1)-4)*L
e1 = (k-1)**2*(k+2)*(k+4); e2 = k*(k-2)*(k+3)**2
c1 = sp.expand((m*H).subs(m, -4+k*(s-1)) - (s-1)**2*g) == 0
d = sp.factor(sp.discriminant(sp.expand(g), s)); c2 = sp.simplify(d / (e1-e2)**2).free_symbols == set()
c3 = sp.expand(g.subs(s, 1) - 16*(k*k-5)) == 0
def chi(a, q): a %= q; return 0 if a == 0 else (1 if pow(a, (q-1)//2, q) == 1 else -1)
def A(q): return sum(chi(mm*(mm**3+8*mm*mm-3*mm*ss*ss+6*mm*ss+13*mm+2*ss**3+2*ss*ss-10*ss+6), q) for ss in range(q) for mm in range(q))
c4 = all(A(q) == (1+chi(-1, q))*q + chi(3, q) for q in (7, 11, 13, 17, 19))
print('m*H=(s-1)^2 g_k:', c1, '| disc = const*(e1-e2)^2:', c2, d, '| g_k(1)=16(k^2-5):', c3, '| closed form on 7..19:', c4)
