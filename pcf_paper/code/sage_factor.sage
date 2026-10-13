# Factor the differential operator (after dividing by (n!)^2) of F1 and of the Gamma-type members G1, G2 with ore_algebra
from ore_algebra import OreAlgebra
import time
R.<z> = QQ['z']; A.<Dz> = OreAlgebra(R)
Rn.<n> = QQ['n']
a = 4*n^2 + 10*n - 3
CASES = {"F1": -n^2*(n+4)*(3*n-4),
         "G1": (n+3)*(2*n-5)*(2*n-1)*(3*n-1),
         "G2": (n+1)*(2*n-3)*(2*n+1)*(3*n-5)}
th = z*Dz
def poly_th(p, shift):
    return sum(c * (th + shift)^k for k, c in enumerate(p.list()))
for name, b in CASES.items():
    L = th^2*(th-1)^2 - z*poly_th(a, 1)*th^2 - z^2*poly_th(b, 2)
    L = L.primitive_part() if hasattr(L, "primitive_part") else L
    print("=" * 60, flush=True); print(name, "order", L.order(), "lead", L.leading_coefficient().factor(), flush=True)
    t = time.time()
    try:
        F = L.factor(verbose=False)
        print(name, "factors orders:", [f.order() for f in F], "time %.0fs" % (time.time() - t), flush=True)
        for f in F:
            print("   factor:", f, flush=True)
    except Exception as e:
        print(name, "factor() failed:", repr(e)[:300], flush=True)
