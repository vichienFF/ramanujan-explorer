r"""Regression test for run_orb.py (Table 2 rows q >= 12167, including the q = 12167 blind test, were computed with run_orb.py on Kaggle;
rows 4096, 4913, 6859 with run_nb_top12.py, see README).  # LOCAL-OK: about a minute
Runs run_orb.py locally (numba optional) for q = 125, 343 and compares Var(M)/E(M) with an INDEPENDENT brute-force count
(probe3.Nvec from the Version 3 release, all triples, no orbit reduction) and with Table 1 of the paper (ratio/3k = 1.101, 1.180).
Usage: python regress_run_orb.py [path to the v3 local_probes folder]  (default: ../../v3/local_probes as on GitHub, else ../../release_v3/local_probes)"""
import os, sys, json, subprocess, tempfile, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
_cands = [os.path.join(HERE, '..', '..', d, 'local_probes') for d in ('v3', 'release_v3')]
PROBES = sys.argv[1] if len(sys.argv) > 1 else next((c for c in _cands if os.path.isdir(c)), _cands[0])
TABLE = {125: 1.101, 343: 1.180}
work = tempfile.mkdtemp()
env = dict(os.environ, QS=','.join(map(str, TABLE)))
subprocess.run([sys.executable, os.path.join(HERE, 'run_orb.py')], cwd=work, env=env, check=True)
orb = {r['q']: r for r in map(json.loads, open(os.path.join(work, 'pp_nb.jsonl')))}
sys.path.insert(0, PROBES); os.chdir(PROBES)
from probe3 import Nvec
bad = 0
for q, tab in TABLE.items():
    p, k = {125: (5, 3), 343: (7, 3)}[q]
    N, good, m, _ = Nvec(p, k); M = N[good] // (3 * k); ind = M.var() / M.mean()
    o = orb[q]['VoverE']; ok = abs(o - ind) < 1e-9 and round(o, 3) == tab and orb[q]['all_div_3k']
    bad += not ok
    print('q=%d run_orb V/E=%.6f  independent=%.6f  table=%.3f  3k|N: %s -> %s' % (q, o, ind, tab, orb[q]['all_div_3k'], 'PASS' if ok else 'FAIL'))
sys.exit(1 if bad else 0)
