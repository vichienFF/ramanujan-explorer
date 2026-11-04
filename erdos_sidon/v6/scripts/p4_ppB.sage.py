# H-PP-B (registered): B(q) = 2q + phi(-1)q + chi(3) b_q at q = 289, 361, 529, 841, 1331.  # LOCAL-OK: est. < 25 min (q=1331: 1.8M terms)
# CONTROL: same evaluator gives the referee-checked values at q=49 (53) and q=121 (605).
exec(open('p4_char35.sage.py').read().split('ctl = ')[0])
ctl = B(49)[0] == 53 and B(121)[0] == 605; print('CONTROL:', 'PASS' if ctl else 'FAIL', flush=True); ok = ctl
for p, n in ((17, 2), (19, 2), (23, 2), (29, 2), (11, 3)):
    q = p**n; b, f1, c3 = B(q); pred = 2*q + f1*q + c3*bq(p, n); ok &= b == pred
    print('q=%d B=%d pred %d -> %s' % (q, b, pred, 'HOLDS' if b == pred else 'FAILS'), flush=True)
print('H-PP-B:', 'PASS' if ok else 'FAIL')
