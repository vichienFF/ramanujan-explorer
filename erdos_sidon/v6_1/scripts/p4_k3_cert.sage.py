# R1 certificate for the FFA draft (Sec. 5.4): two explicit sections of E_k: Y^2 = X(X-e1)(X-e2) over Q(i)(k), their Y-coordinates,  # LOCAL-OK: seconds
# the fibre components they meet (j at each reducible fibre), heights h(P) = 4 + 2(P.O) - sum contr_v, and the pairing <P1,P2>.
# Reuses the height code of p4_shioda.sage.py (same file, controls there: torsion h=0, h(2P)=4h(P), h(P+T)=h(P)).
# CONTROL: the two Gram entries must reproduce p4_shioda.out ('basis rows (0, 1) Gram [3/2, 0, 0, 2/3]'); each point must lie on E.
exec(open('p4_shioda.sage.py').read().split("print('heights:'")[0])
def comps(Pt):
    x = F(Pt[0]); out = []
    for v, r, node in FIN:
        o = ordv(x - (e1 if node == 'e1' else 0), v); out.append((v, 2*r, min(o, r) if (ordv(x, v) >= 0 and o > 0) else 0))
    oi = 4 - deg(x - e1); out.append(('inf', 6, min(oi, 3) if (4 - deg(x) >= 0 and oi > 0) else 0))
    return out
P1, P2 = P[0], P[1]
ok = all(F(Q[1])**2 == F(Q[0])*(F(Q[0]) - e1)*(F(Q[0]) - e2) for Q in (P1, P2))
g12 = (h(P1 + P2) - h(P1) - h(P2)) / 2
print('on curve:', ok, '| h(P1) =', h(P1), '| h(P2) =', h(P2), '| <P1,P2> =', g12)
print('CONTROL (p4_shioda.out Gram [3/2,0,0,2/3]):', 'PASS' if ok and (h(P1), h(P2), g12) == (QQ(3)/2, QQ(2)/3, 0) else 'FAIL')
for name, Q in (('P1', P1), ('P2', P2)):
    print(name, ': X =', F(Q[0]).factor(), '| Y =', F(Q[1]).factor())
    print('   components (place, I_n, j):', comps(Q))
