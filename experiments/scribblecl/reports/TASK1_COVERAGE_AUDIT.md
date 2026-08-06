# Task-1 coverage audit

Audited commit: `dcf4aa68993e4915381a96bbac173dea4c9e0409`.

All seven queued Task-1 seed-42 runs completed with return code 0.  Audit values were recomputed from each saved final checkpoint on the validation split with future logits masked to classes 0--3.  The test split was not opened.

| Run | MYO Dice | LV Dice | LA Dice | Mean Dice | final loss (last-20 mean ± sd) |
|---|---:|---:|---:|---:|---:|
| Dense | 0.45563 | 0.48317 | 0.68984 | 0.54288 | 0.001965 ± 0.000029 |
| PCE-B1 | 0.03134 | 0.17150 | 0.16014 | 0.12099 | 0.000327 ± 0.000047 |
| ZS-B1 | 0.04866 | 0.05005 | 0.12444 | 0.07438 | 0.000888 ± 0.000074 |
| PCE-B2 | 0.02940 | 0.18082 | 0.19898 | 0.13640 | 0.000314 ± 0.000077 |
| ZS-B2 | 0.04921 | 0.10801 | 0.05963 | 0.07228 | 0.000868 ± 0.000066 |
| PCE-B3 | 0.03083 | 0.16878 | 0.17423 | 0.12461 | 0.000339 ± 0.000030 |
| ZS-B3 | 0.05007 | 0.11045 | 0.05686 | 0.07246 | 0.000927 ± 0.000072 |

Dense passed the common-pipeline gate: all checkpoint tensors and logged losses are finite, and MYO/LV/LA predictions are non-empty on 100.0%, 98.4%, and 100.0% of their positive validation slices, respectively.  Thus the observed weak-supervision failure is not evidence of a common output/metric collapse.

## Actual coverage and zero-supervision audit

| Budget (width) | MYO | LV | LA | zero-supervision slices | zero-supervision batches |
|---|---:|---:|---:|---:|---:|
| B1 (1 px) | 7.37% | 2.54% | 3.53% | 282/1500 (18.8%) | 0/188 |
| B2 (3 px) | 21.89% | 7.69% | 10.59% | 282/1500 (18.8%) | 0/188 |
| B3 (5 px) | 35.94% | 12.98% | 17.70% | 282/1500 (18.8%) | 0/188 |

`zero_supervision_slice_audit.csv` separates all 282 zero-label slices by dense Task-1 GT solely for generator verification: all are category A true-negative slices; category B (`GT active class exists but no scribble`) is exactly 0.  The training loss safely receives zero direct weak supervision for all-ignore samples and no batch is entirely zero-supervision after the seeded shuffle.

## Required evidence limitations

The queue's immutable trainer retained only final checkpoints and epoch-level training loss.  It did not log per-epoch validation Dice/loss, ZS component losses, gradient norms, or a validation-selected best checkpoint.  Accordingly, the CSV records these fields as `NA_not_logged`; this audit does not invent them or relabel the final checkpoint as validation-best.  This logging gap must be corrected before any fresh protocol run, but it does not alter or overwrite the completed coverage evidence.

Detailed machine-readable evidence is in `results/task1_coverage_runs.csv`, `results/task1_coverage_classwise.csv`, `results/task1_coverage_curves.csv`, and `results/task1_coverage_summary.csv`.
