# HYPOTHESIS (hand, Riemann-Hurwitz): the c+d=0 locus {h(t1)=h(t2), t1!=t2}, h(t)=(t-1)(t^2+1)/(1+t)^3 (P(t1),P(t2),P(-1) collinear) is genus 1,
# so its point count carries an elliptic trace a_q that must CANCEL against the repeated-root locus. Kill-test: a_q must vary non-elementarily
# (not a fixed character combination) and a_q(ii) - a_q(iii) (or sum) must be elementary.  # LOCAL-OK: seconds
# CONTROL: independent recount of locus (ii) via the definition c+d=0 from the pair's (c,d) (no use of h) must equal the h-count.
def chi(a, q): a %= q; return 0 if a == 0 else (1 if pow(a, (q-1)//2, q) == 1 else -1)
for q in (7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47):
    inv = lambda a: pow(a % q, q-2, q)
    h = {t: (t-1)*(t*t+1)*inv(pow(1+t, 3, q)) % q for t in range(q) if (1+t) % q}
    n_h = sum(1 for a in h for b in h if a != b and h[a] == h[b])
    n_cd, n_rep = 0, 0
    for a in range(q):
        for b in range(q):
            if a == b or (1+a) % q == 0 or (1+b) % q == 0: continue
            A1, A2 = pow(a, 4, q), pow(b, 4, q)
            if A1 == A2: continue
            B1, B2 = pow(1+a, 4, q), pow(1+b, 4, q); c = (B1-B2)*inv(A1-A2) % q; d = (B1 - c*A1) % q
            if (c + d) % q == 0: n_cd += 1
            # repeated root at a: F'(a) = 4(1+a)^3 - 4c a^3 = 0
            if ((1+a)**3 - c*a**3) % q == 0: n_rep += 1
    print('q=%d CONTROL n_h==n_cd %s | locus(ii) pairs %d (q - n = %d) | rep-at-t1 pairs %d (q - n = %d)' % (q, n_h == n_cd, n_cd, q - n_cd, n_rep, q - n_rep))
