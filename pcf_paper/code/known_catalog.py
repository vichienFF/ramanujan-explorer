"""
Catalogue of classical formulas (written from general knowledge, not downloaded) - layer-2 filter for "already known formula".
Matching: the formula value equals the target constant + the "structural signature" (functions used + numbers in the expression) agrees.
No catalogue match does not mean new -> a manual literature search follows (layer 4).
"""
# (name, mpmath expression whose value = the constant, expression of the constant)
CATALOG = [
    ("Leibniz", "nsum(lambda k: (-1)**k/(2*k+1), [0, inf])", "pi/4"),
    ("Basel", "nsum(lambda k: 1/k**2, [1, inf])", "pi**2/6"),
    ("zeta4", "nsum(lambda k: 1/k**4, [1, inf])", "pi**4/90"),
    ("zeta6", "nsum(lambda k: 1/k**6, [1, inf])", "pi**6/945"),
    ("odd squares", "nsum(lambda k: 1/(2*k+1)**2, [0, inf])", "pi**2/8"),
    ("alt Basel", "nsum(lambda k: (-1)**(k+1)/k**2, [1, inf])", "pi**2/12"),
    ("Apery series", "nsum(lambda k: 1/k**3, [1, inf])", "zeta(3)"),
    ("Apery fast", "nsum(lambda k: (-1)**(k+1)/(k**3*binomial(2*k,k)), [1, inf])", "2*zeta(3)/5"),
    ("alt harmonic", "nsum(lambda k: (-1)**(k+1)/k, [1, inf])", "log(2)"),
    ("log2 fast", "nsum(lambda k: 1/(k*2**k), [1, inf])", "log(2)"),
    ("e series", "nsum(lambda k: 1/factorial(k), [0, inf])", "e"),
    ("e limit", "limit(lambda m: (1+1/m)**m, inf)", "e"),
    ("Wallis", "nprod(lambda k: 4*k**2/(4*k**2-1), [1, inf])", "pi/2"),
    ("Euler product zeta2", "nprod(lambda p: 1/(1-prime(p)**-2), [1, inf])", "pi**2/6"),
    ("Machin", "4*atan(1/5)-atan(1/239)", "pi/4"),
    ("Euler arctan", "atan(1/2)+atan(1/3)", "pi/4"),
    ("BBP", "nsum(lambda k: (4/(8*k+1)-2/(8*k+4)-1/(8*k+5)-1/(8*k+6))/16**k, [0, inf])", "pi"),
    ("Ramanujan 1/pi", "2*sqrt(2)/9801*nsum(lambda k: factorial(4*k)*(1103+26390*k)/(factorial(k)**4*396**(4*k)), [0, inf])", "1/pi"),
    ("Chudnovsky", "12*nsum(lambda k: (-1)**k*factorial(6*k)*(13591409+545140134*k)/(factorial(3*k)*factorial(k)**3*640320**(3*k+mpf(3)/2)), [0, inf])", "1/pi"),
    ("Catalan series", "nsum(lambda k: (-1)**k/(2*k+1)**2, [0, inf])", "catalan"),
    ("Euler gamma limit", "limit(lambda m: harmonic(m)-log(m), inf)", "euler"),
    ("Gaussian integral", "quad(lambda x: exp(-x**2), [-inf, inf])", "sqrt(pi)"),
    ("Dirichlet integral", "quad(lambda x: sin(x)/x, [0, inf])", "pi/2"),
    ("gamma half", "gamma(0.5)", "sqrt(pi)"),
    ("Euler identity", "exp(pi*1j)", "-1"),
    ("golden CF/radical", "sqrt(1+sqrt(1+sqrt(1+sqrt(1))))", "phi"),
    ("golden", "(1+sqrt(5))/2", "phi"),
    ("golden power", "phi**2", "phi+1"),
    ("Binet", "(phi**n-(1-phi)**n)/sqrt(5)", "fib(n)"),
    ("Ramanujan radical", "sqrt(1+2*sqrt(1+3*sqrt(1+4*sqrt(1+5*sqrt(1+6)))))", "3"),
    ("Ramanujan constant near-int", "exp(pi*sqrt(163))", "640320**3+744"),
    ("Stirling", "factorial(n)", "sqrt(2*pi*n)*(n/e)**n"),
    ("sum of cubes", "sum(k**3 for k in range(1, n+1))", "(n*(n+1)/2)**2"),
    ("sum of squares", "sum(k**2 for k in range(1, n+1))", "n*(n+1)*(2*n+1)/6"),
    ("sum of odds", "sum(2*k-1 for k in range(1, n+1))", "n**2"),
    ("Fibonacci sum", "sum(fib(k) for k in range(1, n+1))", "fib(n+2)-1"),
    ("Cassini", "fib(n+1)*fib(n-1)-fib(n)**2", "(-1)**n"),
    ("central binomial sum", "sum(binomial(n,k)**2 for k in range(0, n+1))", "binomial(2*n,n)"),
    ("binomial row", "sum(binomial(n,k) for k in range(0, n+1))", "2**n"),
    ("Wilson", "(factorial(n-1)+1) % n", "0"),
    ("zeta(2n) Bernoulli", "zeta(2*n)", "(-1)**(n+1)*bernoulli(2*n)*(2*pi)**(2*n)/(2*factorial(2*n))"),
    ("reflection", "gamma(z)*gamma(1-z)", "pi/sin(pi*z)"),
    ("Legendre duplication", "gamma(z)*gamma(z+0.5)", "2**(1-2*z)*sqrt(pi)*gamma(2*z)"),
    ("zeta(-1)", "zeta(-1)", "-1/12"),
    ("Glaisher", "glaisher", "exp(1/12 - diff(zeta, -1))"),
    ("Khinchin", "khinchin", "khinchin"),
    ("sin product", "nprod(lambda k: 1-(1/2)**2/k**2, [1, inf])", "2/pi"),
    ("Vieta", "2/pi", "sqrt(2)/2*sqrt(2+sqrt(2))/2"),
    ("pi CF (Brouncker)", "4/pi", "1+1/(2+9/(2+25/(2+49/(2+...))))"),
    ("e CF", "e", "[2;1,2,1,1,4,1,1,6,...]"),
    ("sqrt2 CF", "sqrt(2)", "[1;2,2,2,...]"),
    ("Gauss CF tanh", "tanh(1)", "1/(1+1/(3+1/(5+...)))"),
    ("Basel via integral", "quad(lambda x: log(x)*log(1-x)/x, [0,1])", "zeta(3)"),
    ("Frullani/log", "quad(lambda x: 1/(1+x), [0,1])", "log(2)"),
    ("pi integral", "quad(lambda x: 4/(1+x**2), [0,1])", "pi"),
    ("Euler-Mascheroni integral", "-quad(lambda x: exp(-x)*log(x), [0, inf])", "euler"),
    ("Catalan integral", "quad(lambda x: atan(x)/x, [0,1])", "catalan"),
    ("Lambert/Wallis", "22/7", "pi+quad(lambda x: x**4*(1-x)**4/(1+x**2), [0,1])"),
    ("Dottie", "cos(dottie)", "dottie"),
    ("omega constant", "lambertw(1)", "omega"),
    ("sophomore dream", "quad(lambda x: x**-x, [0,1])", "nsum(lambda k: k**-k, [1, inf])"),
    ("Euler pentagonal", "nprod(lambda k: 1-q**k, [1, inf])", "nsum(lambda k: (-1)**k*q**(k*(3*k-1)/2), [-inf, inf])"),
    ("Jacobi triple / theta", "jtheta(3, 0, q)", "nsum(lambda k: q**(k**2), [-inf, inf])"),
    ("Rogers-Ramanujan CF", "rr_cf(q)", "q**(1/5)*prod((1-q**(5k+1))(1-q**(5k+4)))/..."),
    ("zeta2 via central binomial", "3*nsum(lambda k: 1/(k**2*binomial(2*k,k)), [1, inf])", "pi**2/6"),
    ("Gregory log", "nsum(lambda k: 2/((2*k+1)*3**(2*k+1)), [0, inf])", "log(2)"),
]

import re

KNOWN_CONST_NAMES = ["pi", "e", "euler", "catalan", "phi", "zeta", "log", "glaisher", "khinchin", "apery",
                     "sqrt", "gamma", "exp", "fib", "binomial", "factorial", "bernoulli", "harmonic"]


def signature(expr):
    """Coarse structural signature: function names used + integers that appear (ignoring variable names / spaces)"""
    s = str(expr)
    names = set(re.findall(r"[A-Za-z_]\w*", s)) - {"lambda", "k", "n", "m", "x", "j", "i", "p", "q", "z", "inf", "for", "in", "range"}
    ints = set(re.findall(r"\b\d+\b", s))
    return frozenset(names), frozenset(ints)


def _full(a, b):
    (n1, i1), (n2, i2) = signature(a), signature(b)
    return n1 | n2, i1 | i2


SIGS = [(name, _full(a, b)) for name, a, b in CATALOG]


def catalog_match(lhs, rhs):
    """Return the catalogue name whose combined signature (function names + numbers) matches, or None - coarse, for filtering only"""
    sig = _full(lhs, rhs)
    for name, s in SIGS:
        if sig == s:
            return name
    return None
