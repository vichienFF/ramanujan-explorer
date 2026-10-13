"""Try to prove lhs == rhs with sympy (separate process, timeout controlled by the main process) -> if proven = algebraic / well-known formula"""
import json, sys
import sympy as S
from sympy.parsing.sympy_parser import parse_expr

n = S.Symbol("n", integer=True, positive=True)
LOC = dict(pi=S.pi, e=S.E, E=S.E, euler=S.EulerGamma, catalan=S.Catalan, phi=S.GoldenRatio, apery=S.zeta(3),
           ln2=S.log(2), ln10=S.log(10), sqrt=S.sqrt, cbrt=S.cbrt, root=S.root, exp=S.exp, log=S.log, ln=S.log,
           sin=S.sin, cos=S.cos, tan=S.tan, cot=S.cot, sec=S.sec, csc=S.csc, asin=S.asin, acos=S.acos,
           atan=S.atan, acot=S.acot, sinh=S.sinh, cosh=S.cosh, tanh=S.tanh, atanh=S.atanh, asinh=S.asinh,
           zeta=S.zeta, gamma=S.gamma, factorial=S.factorial, fac=S.factorial, binomial=S.binomial,
           fib=S.fibonacci, fibonacci=S.fibonacci, bernoulli=S.bernoulli, harmonic=S.harmonic, polylog=S.polylog,
           mpf=S.nsimplify, mpq=S.Rational, fraction=S.Rational, power=S.Pow, fabs=S.Abs, abs=S.Abs,
           floor=S.floor, ceil=S.ceiling, rf=S.rf, ff=S.ff, beta=S.beta, erf=S.erf, loggamma=S.loggamma,
           psi=S.polygamma, digamma=S.digamma, n=n, inf=S.oo)

import re
_GEN = re.compile(r"\bsum\((.+?) for (\w) in range\(([^,()]+(?:\([^()]*\))?[^,()]*),\s*([^()]+(?:\([^()]*\))?[^()]*)\)\)")
_NS = re.compile(r"\bn(sum|prod)\(lambda (\w):\s*(.+?),\s*\[([^,\]]+),\s*([^\]]+)\]\)")


def to_sympy(x):
    """Rewrite forms sympy cannot read: sum(.. for k in range(a,b)) -> Sum(..,(k,a,b-1)); nsum/nprod(lambda k: .., [a,b])"""
    x = _GEN.sub(lambda m: f"Sum({m.group(1)},({m.group(2)},{m.group(3)},({m.group(4)})-1))", x)
    x = _NS.sub(lambda m: f"{'Sum' if m.group(1) == 'sum' else 'Product'}({m.group(3)},({m.group(2)},{m.group(4)},{m.group(5)}))", x)
    return x


LOC.update(Sum=S.Sum, Product=S.Product, k=S.Symbol("k", integer=True, positive=True))

if __name__ == "__main__":
    job = json.loads(sys.stdin.read())
    try:
        l = parse_expr(to_sympy(job["lhs"]).replace("**", "^").replace("^", "**"), local_dict=LOC)
        r = parse_expr(to_sympy(job["rhs"]).replace("**", "^").replace("^", "**"), local_dict=LOC)
        d = S.simplify((l - r).doit())
        proven = d == 0 or S.simplify(S.expand_func(S.expand(d))) == 0
        out = {"parsed": True, "proven": bool(proven)}
    except Exception as ex:
        out = {"parsed": False, "proven": False, "error": type(ex).__name__}
    sys.stdout.write(json.dumps(out))
