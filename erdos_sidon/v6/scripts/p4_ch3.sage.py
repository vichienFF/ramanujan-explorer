# H-CH3 (registered): F3(4)-(q-2)(q+1) at q=3 predicted -4.  # LOCAL-OK: seconds
# CONTROL: same functions reproduce q=9 residual 2 and q=7 proved value (from p4_scope.out).
exec(open('p4_scope.sage.py').read().split("S, m = singer(11)")[0])
S, m = singer(7); ctl = F3(ms(S, m, 4)) == 5*8 + bp(7)
S, m = singer(9); ctl &= F3(ms(S, m, 4)) - 7*10 == 2
S, m = singer(3); r = F3(ms(S, m, 4)) - 1*4
print('CONTROL:', 'PASS' if ctl else 'FAIL', '| q=3 residual', r, '-> H-CH3', ('PASS' if r == -4 else 'FAIL') if ctl else 'VOID')
