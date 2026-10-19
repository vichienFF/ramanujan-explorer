# Erdos Sidon problem (Guy C9; related to Erdos #30) - Version 2 release (19 October 2026)

Companion files for the preprint "Dilated Singer sets and the excess in Erdos's Sidon problem: a curve-counting theorem,
forbidden-structure laws, and a reduction" (Version 2 of Zenodo DOI 10.5281/zenodo.23407357). Version 1 files are in the parent
folder `erdos_sidon/`.

## Contents
- `paper/c9_note_v2.tex` - LaTeX source.
- `code/` - curve certificates (`irred_cert.py`, `gen_cert.py`), point counts (`curve_count.py`), genus by Riemann-Hurwitz and
  numerical monodromy (`genus_mono.py`, `genus_family.py`), variance law and identities (`variance_*.py`, `identity_I3.py`),
  prime-power Singer sets (`ppsinger.py`, `pp_template.py`), Kaggle templates (`v3_template.py`, `v4_template.py`,
  `b28_run_template.py`, `b29_run_template.py`) and analysis scripts (`b28_analyze.py`, `b29_analyze.py`).
- `certificates/` - absolute-irreducibility certificates: height <= 4 (`cert_H4.txt`), height 5-6 (`cert_H6.txt`), height 5-8 Kaggle
  run (`cert_H5to8_run1.jsonl`), the four orbits that exceeded 10 h (`cert_hard4_run2.jsonl`, status "slow", none failed), genus values.
- `data/` - Kaggle outputs: blind moment tests (`b28/`, `b29/`), variance law (`v3_*`, `lerr_*`), per-dilate errors (`lall_*`,
  `lbulk_*`), k = 4 identity (`v4_*`), prime powers (`ppa_*`, `ppb_*`, `ppc_*`).
- `plans/` - registered plans (frozen before computing) and the SHA-256 ledger with dates.
- `reviews/` - independent AI reviews of the proofs and of the paper, the full-text literature review, and the working notes.

## Labels
Statements marked "proved" in the paper were checked by an independent AI review and by exact computation, not yet by a human expert.
Higher-moment and variance laws are numerical (pre-registered blind tests). Computations and drafting used AI assistance
(Anthropic Claude).

## Reproduce
Python 3 with numpy, scipy, sympy. Kaggle templates expect the modules they embed; see comments at the top of each file.
