r"""Step 5, class rep (members with a repeated root) written out in full (2026-11-04): closed form of SPEC_rep(q).  # LOCAL-OK: < 2 min
Hand derivation (P4_SPECIAL_LEMMA.md, 'Class rep in full'): for Y = y0 not in {0, 1} the member (c, d) = (Y^-3, (1-Y)^-3) has the double root Y;
f = c y^4 + d (1-y)^4 - 1 = c' (y - Y)^2 Q(y), Q(y) = numerator quotient by (y-Y)^2 (leading coefficient 3Y^2-3Y+1; computed symbolically below),
disc_y Q = -8 Y^2 (Y-1)^2 (Y^2-Y+1), Q(Y) = 6 Y^2 (Y-1)^2 != 0 (no triple root), Q(1) != 0 (c != 1).
Excluded Y: c = 1 <-> Y^3 = 1; c + d = 0 <-> 3Y^2-3Y+1 = 0 (those members belong to the other classes).
Weights (ordered pairs of distinct roots): pairs (Y, r) have residual roots {Y, r'} with Y != r', so chi(-D4) = 1; the pair (r1, r2) has residual
roots {Y, Y}, so D4 = 0. Singular pairs (t^4 equal) of type (Y, r): r = Y/(2Y-1) [t -> -t], root of Q iff 2Y^2-2Y+1 = 0; r = eps Y/(eps Y - Y + 1),
eps^2 = -1 [t -> eps t], root of Q iff (2Y-1) + eps (Y^2-Y-1) = 0, i.e. Y in {eps, 1+eps}, norm (Y^2+1)(Y^2-2Y+2).
 k = 2 residual roots in F_q (chi(-2(Y^2-Y+1)) = 1): C(Y) = 6 - (4*2 + 2*1) + s(Y) = -4 + s(Y), s = 2 * #{r : (Y, r) singular};
 k = 1 (Y^2-Y+1 = 0, member c = d = -1 with two double roots, reached from both Y and 1-Y): C = -4 [pair nonsingular], counted once.
=> SPEC_rep = sum over valid Y with Y^2-Y+1 != 0 of [-2(1 + chi(-2(Y^2-Y+1))) + s(Y)]  +  (1/2) sum_{Y^2-Y+1=0} (-4 [nonsingular])
CONTROL: referee brute force referee4/perclass.py pieces(q)['rep'] at every prime 7 <= q < 400.
"""
import sys, sympy as sp
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
exec(open('referee4/perclass.py', encoding='utf-8').read().split("if __name__=='__main__':")[0])   # pieces(q), D4
y, Y = sp.symbols('y Y')
c = Y**-3; d = (1 - Y)**-3
num = sp.expand(sp.numer(sp.together(c*y**4 + d*(1 - y)**4 - 1)))
Qp, rem = sp.div(sp.Poly(num, y), sp.Poly((y - Y)**2, y)); Q = Qp.as_expr()
a2, a1, a0 = sp.Poly(Q, y).all_coeffs()
t = lambda z: z/(1 - z)
eI = sp.numer(sp.together(Q.subs(y, sp.I*Y/(sp.I*Y - Y + 1))))
sym = {
 'double root': rem.is_zero,
 'disc': sp.factor(a1**2 - 4*a2*a0) == sp.factor(-8*Y**2*(Y-1)**2*(Y**2-Y+1)),
 'Q(Y)': sp.factor(Q.subs(y, Y)) == 6*Y**2*(Y-1)**2,
 'Q(1) ~ c-1': sp.factor(Q.subs(y, 1)) == sp.factor(sp.numer(sp.together((c - 1)*Y**3*(1-Y)**3))) or sp.simplify(Q.subs(y, 1)) != 0,
 'c+d=0': sp.factor(sp.numer(sp.together(c + d))) in (sp.factor(3*Y**2-3*Y+1), sp.factor(-(3*Y**2-3*Y+1))),
 't->-t': sp.factor(sp.numer(sp.together(Q.subs(y, Y/(2*Y - 1))))) == sp.factor(2*Y**2*(Y-1)**2*(2*Y**2-2*Y+1)),
 't->it': sp.factor(sp.expand(eI)) == sp.factor(sp.expand(-2*Y**2*(Y-1)**2*((2*Y-1) + sp.I*(Y**2-Y-1)))),
 'norm': sp.factor(sp.expand(((2*Y-1)**2 + (Y**2-Y-1)**2))) == sp.factor((Y**2+1)*(Y**2-2*Y+2)),
}
print('SYM identities:', sym, '->', 'PASS' if all(sym.values()) else 'FAIL')
def chi(x, q):
    x %= q
    return 0 if x == 0 else (1 if pow(x, (q-1)//2, q) == 1 else -1)
def inv(x, q): return pow(x % q, q - 2, q)
def Qroots(Yv, q):
    A2, A1, A0 = [int(sp.Poly(Q, y).all_coeffs()[i].subs(Y, Yv)) % q for i in range(3)]
    return [r for r in range(q) if (A2*r*r + A1*r + A0) % q == 0]
def tq(z, q): return z * inv(1 - z, q) % q
def s_of(Yv, q):           # 2 * number of residual roots r with t(r)^4 = t(Y)^4 (explicit candidates only)
    i_s = [x for x in range(q) if (x*x + 1) % q == 0]
    cands = {Yv * inv(2*Yv - 1, q) % q} | {e*Yv * inv(e*Yv - Yv + 1, q) % q for e in i_s if (e*Yv - Yv + 1) % q}
    R = set(Qroots(Yv, q)) - {Yv}
    return 2 * len(cands & R)
def spec_closed(q):
    total = 0
    for Yv in range(2, q):
        if pow(Yv, 3, q) == 1 or (3*Yv*Yv - 3*Yv + 1) % q == 0: continue
        if (Yv*Yv - Yv + 1) % q == 0:
            r1 = (1 - Yv) % q                  # the double root of Q (other root of Y^2-Y+1)
            nonsing = pow(tq(Yv, q), 4, q) != pow(tq(r1, q), 4, q)
            total += -2 * nonsing              # (1/2) * (-4 [nonsingular])
            continue
        Zs = (2*Yv*Yv - 2*Yv + 1) * (Yv*Yv + 1) * (Yv*Yv - 2*Yv + 2) % q == 0
        total += -2*(1 + chi(-2*(Yv*Yv - Yv + 1), q)) + (s_of(Yv, q) if Zs else 0)
    return total
Pr = [p for p in range(7, 400) if sp.isprime(p)]
rows = [(q, pieces(q)['rep'], spec_closed(q)) for q in Pr]
bad = [r for r in rows if r[1] != r[2]]
print('CONTROL vs referee brute force (perclass.pieces) at %d primes 7..%d: %s' % (len(Pr), Pr[-1], 'PASS' if not bad else 'FAIL %s' % bad[:6]))
print('examples (q, brute, closed):', rows[:5])
# Fully explicit form (no per-Y root search): s(Y) = 2 on Z_s = roots of (2Y^2-2Y+1)(Y^2+1)(Y^2-2Y+2) (valid Y), the k=1 members are always
# nonsingular (t(1-Y) = 1/t(Y), t^8 = Y^-8 = Y^-2 != 1), so
# SPEC_rep = -2(q - chi(-2)) + 2 sum_{Y in X} (1 + chi(-2(Y^2-Y+1))) + 2 #Z_s(valid) - 2 #Z(Y^2-Y+1),  X = {0,1} u Z(Y^2+Y+1) u Z(3Y^2-3Y+1) u Z(Y^2-Y+1).
def roots(coeffs, q): return {x for x in range(q) if sum(cf*pow(x, i, q) for i, cf in enumerate(coeffs)) % q == 0}
def spec_explicit(q):
    X = {0, 1} | roots([1, 1, 1], q) | roots([1, -3, 3], q) | roots([1, -1, 1], q)
    Zs = (roots([1, -2, 2], q) | roots([1, 0, 1], q) | roots([2, -2, 1], q)) - X
    return -2*(q - chi(-2, q)) + 2*sum(1 + chi(-2*(x*x - x + 1), q) for x in X) + 2*len(Zs) - 2*len(roots([1, -1, 1], q))
L = [sp.Poly(p, Y) for p in (Y**3 - 1, 3*Y**2 - 3*Y + 1, Y**2 - Y + 1, 2*Y**2 - 2*Y + 1, Y**2 + 1, Y**2 - 2*Y + 2, 2*Y - 1, Y**2 - Y - 1)]
coll = set()
for i in range(len(L)):
    for j in range(i+1, len(L)):
        r = sp.resultant(L[i].as_expr(), L[j].as_expr(), Y)
        if r != 0: coll |= set(sp.factorint(abs(r)))
print('collision primes of the rep loci (pairwise resultants):', sorted(coll))
bad2 = [(q, pieces(q)['rep'], spec_explicit(q)) for q in Pr if pieces(q)['rep'] != spec_explicit(q)]
print('explicit formula vs brute force at %d primes: %s' % (len(Pr), 'PASS' if not bad2 else 'FAIL %s' % bad2[:6]))
