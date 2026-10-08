# Physics P2 plan (2026-10-08, register before running) - adding weak lensing: SPARC rotation curves + KiDS-1000 lensing RAR

Motivation: P1 showed rotation curves alone cannot discriminate NFW / cored / RAR (mock recovery < 80%); the literature map
(rule 5) requires lensing + rotation curves together. Novelty level: REPRODUCTION, then a joint stress test.
Data: Brouwer et al. 2021 (A&A 650, A113) KiDS-1000 lensing RAR, kids.strw.leidenuniv.nl/sci_data/brouwer2021_rar.tar
(SHA-256 73adc2d4...), converted with the README formulas (g_obs = 4 G ESD_t/bias, errors and full covariance /bias); SPARC as P1.

P2-a reproduction: rebuild the B21 lensing RAR for isolated KiDS galaxies (Fig. 4/5 file) and the early/late split (Fig. 8
colour and Sersic bins). Check: the early- vs late-type difference is significant at >= 5 sigma using the published covariance
(B21 report >= 6 sigma) - this is the positive control for our pipeline.
P2-b one-law test: the RAR law g_obs = g_bar / (1 - exp(-sqrt(g_bar/a0))) with a0 FROZEN from SPARC (P1: 1.01e-10 m/s^2) is
compared with the lensing points (chi^2 with full covariance, g_bar from the B21 files' stellar + hot-gas estimates as given).
Reported: chi^2/dof and p-value for (i) all isolated, (ii) early, (iii) late types.
P2-c CDM baseline: NFW halos with the stellar-to-halo mass relation of Behroozi et al. (2013) median, concentration-mass relation
of Duffy et al. (2008), projected to the same g_bar bins; chi^2 as in P2-b. (Exploratory; approximate halo-model, no 2-halo term.)
Decision rules stated in advance: a model "fails the joint test" if chi^2 p < 0.001 in (i). No new-physics claim is made from P2;
it is the bench on which any future mechanism from the user's project must perform at least as well as the better baseline.
