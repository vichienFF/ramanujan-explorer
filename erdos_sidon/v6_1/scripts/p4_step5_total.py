r"""Step 5 closed: SPEC = SPEC_c1 + SPEC_cd0 + SPEC_rep evaluated SYMBOLICALLY from the three explicit class formulas  # LOCAL-OK: seconds
(p4_step5_c1.py, p4_step5_cd0.py, p4_step5_rep.py), for every q = p^n with p not in {2,3,5,7,13} (where all the exceptional loci are disjoint).
Each correction is a sum over the roots in F_q of an explicit polynomial P of 1 + chi(h(x)); when h mod P is a constant kappa the sum equals
#roots(P) * (1 + chi(kappa)), #roots = 1 (linear) or 1 + chi(disc P) (quadratic). All kappa and discriminants have prime factors in {2,3,7}, so the total
is a function of the signs chi(-1), chi(2), chi(3), chi(7) (16 combinations = every Frobenius class of Q(i, sqrt2, sqrt-3, sqrt-7), incl. all +1 for n even).
Target (*): SPEC = -q + 10 + 5 chi(-1) + 6 chi(-2) + 2 chi(-3) - 2 chi(-7).
CONTROL: the same evaluator reproduces the brute-force SPEC_c1 + SPEC_cd0 + SPEC_rep at the primes 11, 17, 19, 23, 29, 31, 37, 41, 43 (from referee4/perclass.py).
"""
import sys, itertools, sympy as sp
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
x = sp.symbols('x')
# (sign, weight, polynomial, h or None): contribution = sign * weight * sum_{roots of P} (1 + chi(h)) ; h None -> count of roots only
W1 = -(3*x**2 + 6*x + 4); W2 = -(3*x**2 + 4); W3 = -2*(x**2 - x + 1)
TERMS = ([(-1, 2, P, W1) for P in (x+1, 4*x**2+8*x+5, 2*x**2+5*x+4, 3*x**2+6*x+4)] + [(-1, 1, P, W1) for P in (12*x**2+24*x+13, 2*x+1)] +
         [(+1, 1, P, W2) for P in (x, x**2+1, x+1, x**2-x+2, 3*x**2+4, x-2, x+2)] + [(-1, 1, 3*x**2+1, W2)] +
         [(+1, 2, P, W3) for P in (x, x-1, x**2+x+1, 3*x**2-3*x+1, x**2-x+1)] +
         [(+1, 2, P, None) for P in (2*x**2-2*x+1, x**2+1, x**2-2*x+2)] + [(-1, 2, x**2-x+1, None)])
MAIN = {'q': 2 - 1 - 2, 'chi(-3)': -2 + 1, 'chi(-2)': +2}          # 2(q-chi(-3)) - (q-chi(-3)) - 2(q-chi(-2))
def chi_num(n, s):            # s = (chi(-1), chi(2), chi(3), chi(7)); n a nonzero rational
    n = sp.Rational(n); v = n.p * n.q
    out = s[0] if v < 0 else 1
    for p, e in sp.factorint(abs(v)).items():
        if e % 2 == 0: continue
        if p not in (2, 3, 7): raise ValueError('prime %d outside {2,3,7}' % p)
        out *= s[{2: 1, 3: 2, 7: 3}[p]]
    return out
SQ_HINT = {sp.expand(2*x**2+5*x+4): (1, x+2)}   # on roots of 2u^2+5u+4 one root of the pair is -1, so Delta = (a-b)^2 = (u+2)^2 (checked below)
def const_mod(h, P):
    r = sp.rem(sp.expand(h), P, x)
    if sp.degree(r, x) <= 0: return sp.nsimplify(r)
    if sp.expand(P) in SQ_HINT: k, g = SQ_HINT[sp.expand(P)]
    else:                                   # solve h = k (x + beta)^2 mod P for rational k, beta (a pair containing a fixed root)
        k_, b_ = sp.symbols('k_ b_'); eqs = sp.Poly(sp.rem(sp.expand(h - k_*(x + b_)**2), P, x), x).all_coeffs()
        sol = [z for z in sp.solve(eqs, [k_, b_], dict=True) if z[k_].is_rational and z[b_].is_rational]
        assert sol, 'no rational square form for h mod %s' % P
        k, g = sol[0][k_], x + sol[0][b_]; pass
    assert sp.rem(sp.expand(h - k*g**2), P, x) == 0 and sp.resultant(P, g, x) != 0, 'square hint fails'
    return sp.Rational(k)   # was sp.Integer(k): truncated -4/3 to -1 (bug found 11-04)
def total(s):             # constant part (coefficient of q is MAIN['q'])
    tot = MAIN['chi(-3)'] * chi_num(-3, s) + MAIN['chi(-2)'] * chi_num(-2, s)
    for sign, wgt, P, h in TERMS:
        P = sp.Poly(P, x); nroots = 1 if P.degree() == 1 else 1 + chi_num(sp.discriminant(P.as_expr(), x), s)
        val = 1 if h is None else 1 + (0 if const_mod(h, P.as_expr()) == 0 else chi_num(const_mod(h, P.as_expr()), s))
        tot += sign * wgt * nroots * val
    return tot
def target(s): return 10 + 5*chi_num(-1, s) + 6*chi_num(-2, s) + 2*chi_num(-3, s) - 2*chi_num(-7, s)
# CONTROL: compare with brute force at generic primes
exec(open('referee4/perclass.py', encoding='utf-8').read().split("if __name__=='__main__':")[0])
def leg(a, q): return 1 if pow(a % q, (q-1)//2, q) == 1 else -1
ctl = True
for q in (11, 17, 19, 23, 29, 31, 37, 41, 43):
    s = (leg(-1, q), leg(2, q), leg(3, q), leg(7, q)); b = pieces(q)
    ctl &= MAIN['q']*q + total(s) == b['c=1'] + b['c+d=0'] + b['rep']
print('CONTROL (symbolic evaluator = brute force at 9 generic primes):', 'PASS' if ctl else 'FAIL')
print('coefficient of q:', MAIN['q'])
res = [(s, total(s), target(s)) for s in itertools.product((1, -1), repeat=4)]
for s, a, b in res: print('signs chi(-1),chi(2),chi(3),chi(7) =', s, '| constant part', a, '| target', b, '|', 'EQUAL' if a == b else 'DIFF')
print('ALL 16 classes:', 'PASS' if all(a == b for _, a, b in res) and MAIN['q'] == -1 else 'FAIL')
