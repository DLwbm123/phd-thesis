# Formal pilot running status

Snapshot: 2026-08-09T10:24:34Z (2026-08-09 18:24:34 Asia/Shanghai)

| Scenario/method | Seed | PID | Run status | Completed epoch records | Current stage/epoch |
|---|---:|---:|---|---:|---|
| Domain PCE-FT | 42 | 70590 (exited normally) | complete | 900/900 | complete |
| Domain PCE-EWC | 42 | 80127 | running | 179/900 | C, 28/150 |
| Organ PCE-FT | 42 | 71396 | running | 488/600 | T4, 37/150 |
| Organ PCE-EWC | 42 | 80128 | running | 158/600 | T3, 7/150 |

Formal run directories:

- `/remote-home/wangbomin/ScribbleCL/scribblecl_domain_organ_20260809/runs/domain/domain_pce_ft_seed42_20260809T082951Z`
- `/remote-home/wangbomin/ScribbleCL/scribblecl_domain_organ_20260809/runs/domain/domain_pce_ewc_seed42_20260809T095455Z`
- `/remote-home/wangbomin/ScribbleCL/scribblecl_domain_organ_20260809/runs/organ/organ_pce_ft_seed42_20260809T083415Z`
- `/remote-home/wangbomin/ScribbleCL/scribblecl_domain_organ_20260809/runs/organ/organ_pce_ewc_seed42_20260809T095457Z`

The low-priority Domain independent-PCE reference process (PID 81051) is
recoverably paused with `SIGSTOP` after one epoch so core EWC has priority. It
will be resumed for RMA after Domain EWC completes. No seeds 43/44, SI or ZS
process is running. The two pre-vectorization EWC diagnostics remain preserved
with `invalid_engineering` status and are excluded from aggregation.
