# Physics P1 plan (2026-10-08, register before running) - a test bench for galaxy dark-sector models on SPARC

Purpose: before testing any new mechanism from the user's dark-matter project, reproduce the standard model comparison on
SPARC with controls, so that a future mechanism can be judged against it. Novelty level of P1 itself: REPRODUCTION.
Data: SPARC (Lelli, McGaugh & Schombert 2016), files and SHA-256 as in PLAN_BATCH14 (14B). Galaxies with quality Q < 3,
inclination >= 30 deg and >= 8 rotation-curve points. Baryons: V_bar^2 = V_gas|V_gas| + Y_d V_disk^2 + 1.4 Y_d V_bul^2,
Y_d free per galaxy with a log-normal prior (median 0.5, 0.1 dex).

## P1-A model comparison
Models: (1) NFW halo (V200, c), (2) cored pseudo-isothermal halo rho0 / (1 + (r/rc)^2) (SIDM proxy), (3) RAR/MOND:
V^2 = V_bar^2 / (1 - exp(-sqrt(g_bar/a0))) with ONE global a0 fitted on a random half of the galaxies (seed 20261025) and
frozen for the other half. Fits: weighted least squares (errors e_Vobs, floor 3 km/s) with the Y_d prior.
Tests: (i) per-galaxy BIC, fraction of galaxies preferring each model; (ii) EXTRAPOLATION: fit the inner 2/3 of each rotation
curve, predict the outer 1/3; median normalised RMS per model.
Expectation stated in advance (from the literature, not a discovery): cored >= NFW on both tests; RAR competitive with one
global parameter.
Positive control (model recovery): for every galaxy, mock rotation curves generated from each model's best fit (real baryons,
real error bars, Gaussian noise) must be assigned to the generating model by the BIC rule in >= 80% of cases (per model).
## P1-B what SIDM cross-section the cores require
For galaxies preferring the cored model: sigma/m from rho(r_c) <v_rel> (sigma/m) t = 1 at r = r_c, <v_rel> = (4/sqrt(pi)) V_flat/sqrt(2),
t = 10 Gyr. Fit log(sigma/m) = A - alpha log V_flat and compare its extrapolation to cluster velocities (~1000 km/s) with the
cluster limits in PHYSICS_LITERATURE_MAP.md (< 0.2-1 cm^2/g). Exploratory; reported with the caveat that the simple
rate argument is an approximation (known: Kaplinghat, Tulin & Yu 2016).
## P1-C (only after the full 3D-Time paper is available): V34A-0 consistency check + sign of the predicted GW speed deviation.
All outcomes reported; nothing here is labelled new unless it goes beyond the cited literature.
