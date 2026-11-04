r"""Prop spec for p = 7, 13 (FFA round-2 referee item 4): the class formulas of Lemmas c1, cd0, repc (valid in every characteristic >= 5) are  # LOCAL-OK: < 15 min
evaluated over F_{p^n} for one representative of each class n odd / n = 2 mod 4 / n = 0 mod 4 and compared with -q+10+5f1+6f2+2f3-2chi(-7).
Uses GF and closed() from p4_step5_pp.py. CONTROL: closed() equals the brute-force SPEC at q = 49, 169, 2401 (p4_step5_pp.out) and at q = 7, 13
(referee4/perclass.pieces) - recomputed here for 7, 13, 49."""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
exec(open('p4_step5_pp.py', encoding='utf-8').read().split("if __name__ == '__main__':")[0])
ctl = all(closed(GF(p, n))[0] == pieces(GF(p, n)) for p, n in [(7, 1), (13, 1), (7, 2)])
print('CONTROL (closed forms = brute-force per-class SPEC at q = 7, 13, 49):', 'PASS' if ctl else 'FAIL', flush=True)
for p, n in [(7, 1), (7, 2), (7, 4), (13, 1), (13, 2), (13, 4)]:
    F = GF(p, n); cf, tgt = closed(F)
    print('q=%d^%d=%d (n %s): closed-form SPEC %d, target %d -> %s' % (p, n, F.q, 'odd' if n % 2 else ('= 2 mod 4' if n % 4 == 2 else '= 0 mod 4'),
          sum(cf.values()), tgt, 'EQUAL' if sum(cf.values()) == tgt else 'DIFF'), flush=True)
