# H-N3CAT (registered PLAN_UNIFORM_A 11-03): check the 5 category closed forms on unseen primes.  # LOCAL-OK: q<=89, O(q^3) numpy, est. < 20 min total
# CONTROL: p4_n3_assembly.run reproduces N3 (independent (c,d) count) and sum(cat) == E, as in p4_n3_assembly.py.
import sys
sys.argv = ['x', '0']; exec(open('p4_n3_assembly.py', encoding='utf-8').read().split('for q in [int(a)')[0])
ok = True
for q in [int(a) for a in sys.argv_cat] if hasattr(sys, 'argv_cat') else (67, 71, 73, 79, 83, 89):
    cat, tot = run(q); f1, f2, f3 = chi(-1, q), chi(-2, q), chi(-3, q); ctl = tot == Ns(q)[3]
    rest = sum(v for k, v in cat.items() if k not in ('c=0 or d=0', 'diagonal u^2=4v', 'singular t1^4=t2^4', 'generic'))
    got = (cat.get('c=0 or d=0', 0), cat.get('diagonal u^2=4v', 0), cat.get('singular t1^4=t2^4', 0), cat.get('generic', 0), rest)
    pred = (-6*(1+f1)*q + 24*(1+f1), -q + 3*f2, -11*(1+f1), 0, -3*q + 12 + 5*f1 + 6*f2 + 4*f3)
    ok &= ctl and got == pred; print('q=%d CONTROL %s got %s pred %s -> %s' % (q, ctl, got, pred, 'OK' if got == pred else 'MISMATCH'), flush=True)
print('H-N3CAT:', 'PASS' if ok else 'FAIL')
