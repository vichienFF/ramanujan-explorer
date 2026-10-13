"""
mpmath computation sandbox (runs as a separate process: python sandbox.py < job.json > out.json)
- AST check: only mpmath function/constant names + safe builtins are allowed; no attributes, imports or dunders
- the main process enforces a timeout (killed if exceeded) -> guards against endless loops / huge numbers
Jobs: {"op":"eval","expr":..,"dps":..} | {"op":"claim","lhs":..,"rhs":..,"vars":"n"|"", ...}
"""
import ast, json, os, re, sys
import mpmath

_SKIP = {"mp", "fp", "iv", "libmp", "ctx_base", "ctx_mp", "ctx_fp", "ctx_iv", "ctx_mp_python", "calculus",
         "functions", "matrices", "identification", "visualization", "plot", "cplot", "splot", "runtests",
         "doctests", "workdps", "workprec", "extradps", "extraprec", "autoprec", "memoize", "rational", "math2",
         "usertools", "timing", "monitor", "function_docs", "config", "BACKEND", "mpmath", "print_function",
         "absolute_import", "version", "pslq", "identify", "findpoly"}  # do not let the explorer use our own novelty checkers
ALLOWED = {k: getattr(mpmath, k) for k in dir(mpmath)
           if not k.startswith("_") and k not in _SKIP and type(getattr(mpmath, k)).__name__ != "module"}
ALLOWED.update(_div=None, _pow=None, range=range, sum=sum, abs=abs, min=min, max=max, int=int, len=len, round=round, all=all, any=any,
               pow=pow, divmod=divmod, bin=bin, list=list, tuple=tuple, sorted=sorted, reversed=reversed,
               zip=zip, enumerate=enumerate, str=str, True_=True)
if os.environ.get("RAMA_X"):  # R2 E1: let the name X pass the AST check (its value is put into ev at the working precision)
    ALLOWED["X"] = None
OK_NODES = (ast.Expression, ast.Call, ast.Name, ast.Load, ast.Constant, ast.BinOp, ast.UnaryOp, ast.BoolOp,
            ast.Compare, ast.IfExp, ast.Lambda, ast.arguments, ast.arg, ast.Tuple, ast.List, ast.keyword,
            ast.GeneratorExp, ast.ListComp, ast.comprehension, ast.Subscript, ast.Slice, ast.Store,
            ast.operator, ast.unaryop, ast.boolop, ast.cmpop, ast.expr_context)


def compile_safe(expr, extra=()):
    if not isinstance(expr, str) or not expr.strip() or len(expr) > 500:
        raise ValueError("empty_or_too_long")
    expr = re.sub(r"\b(mpmath|mp)\.", "", expr)  # AI writes mpmath.zeta -> strip prefix (round 1 counted as ERROR)
    tree = ast.parse(expr.strip(), mode="eval")
    local = set(extra)
    for node in ast.walk(tree):
        if not isinstance(node, OK_NODES):
            raise ValueError(f"forbidden:{type(node).__name__}")
        if isinstance(node, ast.arg):
            local.add(node.arg)
        if isinstance(node, ast.comprehension):
            for t in ast.walk(node.target):
                if isinstance(t, ast.Name):
                    local.add(t.id)
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id not in ALLOWED and node.id not in local:
            raise ValueError(f"unknown_name:{node.id}")
        if isinstance(node, ast.Name) and "__" in node.id:
            raise ValueError("dunder")
    tree = ast.fix_missing_locations(_Exact().visit(tree))
    return compile(tree, "<x>", "eval")


def _div(a, b):
    return mpmath.mpf(a) / b if isinstance(a, int) and isinstance(b, int) else a / b


def _pow(a, b):
    return mpmath.mpf(a) ** b if isinstance(a, int) and isinstance(b, int) and b < 0 else a ** b


class _Exact(ast.NodeTransformer):
    """int/int and int**(-k) give 16-digit floats in Python -> converted to high-precision mpf"""
    def visit_BinOp(self, node):
        self.generic_visit(node)
        f = {ast.Div: "_div", ast.Pow: "_pow"}.get(type(node.op))
        return ast.Call(ast.Name(f, ast.Load()), [node.left, node.right], []) if f else node

    def visit_Constant(self, node):  # a float such as 0.1 is inexact -> mpf("0.1") (in round 1 this wrongly turned 2 true formulas into NEAR_MISS)
        if isinstance(node.value, float):
            return ast.Call(ast.Name("mpf", ast.Load()), [ast.Constant(repr(node.value))], [])
        return node


def ev(code, dps, **vars_):
    ALLOWED.update(_div=_div, _pow=_pow)
    mpmath.mp.dps = dps
    if os.environ.get("RAMA_X"):  # R2 E1: mystery number X (high precision) - no effect on other jobs unless this variable is set
        ALLOWED["X"] = mpmath.mpf(os.environ["RAMA_X"])
    v = eval(code, dict(ALLOWED, __builtins__={}, **vars_))  # globals: visible inside generators
    if isinstance(v, (int, float, bool)):
        v = mpmath.mpf(v)
    return v


def num(v, digits):
    try:
        return mpmath.nstr(v, digits)
    except Exception:
        return str(v)[:300]


def rel_err(a, b):
    return abs(a - b) / max(1, abs(a), abs(b))


def run(job):
    op = job["op"]
    if op == "eval":
        code = compile_safe(job["expr"])
        v = ev(code, job.get("dps", 40))
        return {"ok": True, "value": num(v, job.get("show", 30))}
    if op == "claim":
        vars_ = job.get("vars") or ""
        cl, cr = compile_safe(job["lhs"], vars_.split()), compile_safe(job["rhs"], vars_.split())
        if not vars_:
            out = {}
            for d in (60, 110):
                l, r = ev(cl, d), ev(cr, d)
                out[d] = (l, r)
            (l60, r60), (l110, r110) = out[60], out[110]
            mpmath.mp.dps = 110
            e110, e60 = rel_err(l110, r110), rel_err(l60, r60)
            stab = max(rel_err(l60, l110), rel_err(r60, r110))
            return {"ok": True, "err110": num(e110, 3), "err60": num(e60, 3), "stab": num(stab, 3),
                    "lhs": num(l110, 40), "rhs": num(r110, 40),
                    "digits": int(-mpmath.log10(e110)) if e110 > 0 else 110,
                    "pass": bool(e110 < mpmath.mpf(10) ** -100 and e60 < mpmath.mpf(10) ** -50),
                    "unstable": bool(stab > mpmath.mpf(10) ** -50)}
        # check every n = 1..N (60 digits; equal if the difference is < 1e-45)
        N = job.get("N", 100)
        mpmath.mp.dps = 60
        for n in range(1, N + 1):
            l, r = ev(cl, 60, n=n), ev(cr, 60, n=n)
            if rel_err(l, r) > mpmath.mpf(10) ** -45:
                return {"ok": True, "pass": False, "fail_n": n, "lhs": num(l, 20), "rhs": num(r, 20)}
        return {"ok": True, "pass": True, "checked_n": N}
    if op == "identify":  # used by the verifier only (the explorer cannot call identify) - separate process because some values take very long
        mpmath.mp.dps = 30
        v = mpmath.identify(mpmath.mpf(job["value"]), job["consts"], tol=mpmath.mpf(10) ** -25)
        return {"ok": True, "value": v}
    raise ValueError("bad_op")


if __name__ == "__main__":
    job = json.loads(sys.stdin.read())
    try:
        res = run(job)
    except Exception as ex:
        res = {"ok": False, "error": f"{type(ex).__name__}: {str(ex)[:200]}"}
    sys.stdout.write(json.dumps(res))
