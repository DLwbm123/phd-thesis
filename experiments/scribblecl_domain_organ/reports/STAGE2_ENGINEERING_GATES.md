# Seed-42 PCE-EWC stage-2 engineering gates

Status: `DIAGNOSTIC_PASS_REVALIDATION_RUNNING`

Date: 2026-08-09

Both EWC runs load the exact paired PCE-FT `stage_1.pt`. Fisher is then
re-estimated from the first task's current training images and sparse PCE only.
The 50% comparison is an engineering-collapse check, not a scientific
threshold.

| Scenario | Paired FT current | EWC current | EWC / FT | Prediction FG fraction | Finite | Fisher/penalty finite | Decision |
|---|---:|---:|---:|---:|---|---|---|
| Domain, Center B | 0.539035 | 0.539043 | 1.000016 | 0.155753 | yes | yes | DIAGNOSTIC PASS |
| Organ, T2 | 0.485448 | 0.441509 | 0.909487 | 0.303548 | yes | yes | DIAGNOSTIC PASS |

Evidence runs:

- Domain FT: `domain_pce_ft_seed42_20260809T082951Z`
- Domain EWC: `domain_pce_ewc_seed42_20260809T085816Z`
- Organ FT: `organ_pce_ft_seed42_20260809T083415Z`
- Organ EWC: `organ_pce_ewc_seed42_20260809T091347Z`

These two runs were subsequently marked `invalid_engineering` and stopped after
profiling showed that the parameter-wise penalty created avoidable kernel-launch
overhead on large tasks. A value- and gradient-equivalent vectorized penalty
passed the full test suite and reduced the isolated GPU penalty call from 4.35
ms to 0.70 ms. Replacement runs
`domain_pce_ewc_seed42_20260809T095455Z` and
`organ_pce_ewc_seed42_20260809T095457Z` restart from the same parent
checkpoints and must independently pass this gate before the status becomes
formal PASS. This diagnostic gate does not authorize seeds 43/44.
