# Seed-42 PCE-EWC stage-2 engineering gates

Date: 2026-08-09

Both EWC runs load the exact paired PCE-FT `stage_1.pt`. Fisher is then
re-estimated from the first task's current training images and sparse PCE only.
The 50% comparison is an engineering-collapse check, not a scientific
threshold.

| Scenario | Paired FT current | EWC current | EWC / FT | Prediction FG fraction | Finite | Fisher/penalty finite | Decision |
|---|---:|---:|---:|---:|---|---|---|
| Domain, Center B | 0.539035 | 0.539043 | 1.000016 | 0.155753 | yes | yes | PASS |
| Organ, T2 | 0.485448 | 0.441509 | 0.909487 | 0.303548 | yes | yes | PASS |

Evidence runs:

- Domain FT: `domain_pce_ft_seed42_20260809T082951Z`
- Domain EWC: `domain_pce_ewc_seed42_20260809T085816Z`
- Organ FT: `organ_pce_ft_seed42_20260809T083415Z`
- Organ EWC: `organ_pce_ewc_seed42_20260809T091347Z`

The second-stage EWC state files contain the consolidated Fisher diagonal and
`theta_star`. No blocker file was produced, and both processes continued to the
third stage. This gate does not authorize seeds 43/44; the complete seed-42
matrix gate is still required.
