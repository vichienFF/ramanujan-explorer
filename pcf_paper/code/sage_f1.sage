from ore_algebra import OreAlgebra
R.<z> = QQ['z']; A.<Dz> = OreAlgebra(R)
th = z*Dz
L = th^2*(th-1)^2 - z*(4*(th+1)^2+10*(th+1)-3)*th^2 + z^2*(th+2)^2*(th+6)*(3*th+2)
F = L.factor()
P = prod(F)
print("product/L:", (P.leading_coefficient()/L.leading_coefficient()), "check:", P == (P.leading_coefficient()/L.leading_coefficient())*L)
# recurrence side: Q_n = a(n) Q_{n-1} + b(n) Q_{n-2}  ->  shift operator in n
Rn.<n> = QQ['n']; S.<Sn> = OreAlgebra(Rn, 'Sn')
a = lambda m: 4*m^2+10*m-3
b = lambda m: -m^2*(m+4)*(3*m-4)
Rec = Sn^2 - a(n+2)*Sn - b(n+2)
print("rec methods:", [m for m in dir(Rec) if any(k in m for k in ("hyper", "factor", "dalemb", "right"))])
try:
    print("hypergeometric solutions:", Rec.right_factors())
except Exception as e:
    print("right_factors err", repr(e)[:200])
for m in ("generalized_series_solutions",):
    try:
        print(m, getattr(Rec, m)(3))
    except Exception as e:
        print(m, "err", repr(e)[:200])
