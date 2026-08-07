# Static Task-1 reference results

Decision remains `DECISION: NO-GO-ZS`.

These values were exported without training or test-set access from the completed MMWHS Task-1 validation runs under `/remote-home/wangbomin/ScribbleCL/static_task1_commit470b0d0`. The immutable evidence copy is `/remote-home/wangbomin/ScribbleCL/static_reference_exports_20260807`; its filtered tree SHA-256 is `1849487e14840a580f676fdcd7ec446af9547354e52bf275fa7ddc8a656b745e`.

The historical run called `A0` below is the old foreground-only diagnostic. It must not be confused with the new formal ladder's `A0 = PCE-FG+BG without shared geometry`.

## Best checkpoint metrics

| Historical run | Status | Epoch | BG-inclusive mean | BG patient Dice | Foreground patient mean | MYO | LV | LA |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| A0 / FG-only | diagnostic | 4 | 0.146502 | 0.000000 | 0.195336 | 0.027720 | 0.305278 | 0.253009 |
| A-ratio | diagnostic-only | 10 | 0.509141 | 0.937021 | 0.366515 | 0.206247 | 0.370916 | 0.522382 |
| Dense-v2 | valid dense reference | 136 | 0.818302 | 0.992411 | 0.760266 | 0.680808 | 0.780680 | 0.819310 |

## Positive-slice and aggregate-volume Dice

| Historical run | Positive MYO | Positive LV | Positive LA | Positive mean | Aggregate MYO | Aggregate LV | Aggregate LA | Aggregate mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A0 / FG-only | 0.039965 | 0.352668 | 0.336142 | 0.242925 | 0.027638 | 0.306158 | 0.296954 | 0.210250 |
| A-ratio | 0.259774 | 0.344709 | 0.579657 | 0.394713 | 0.197090 | 0.399764 | 0.605248 | 0.400701 |
| Dense-v2 | 0.648445 | 0.694048 | 0.803606 | 0.715366 | 0.650425 | 0.780774 | 0.873625 | 0.768275 |

## Last epoch and last-20 stability

| Historical run | Last epoch | Last BG-inclusive | Last foreground | Last-20 BG mean ± std | Last-20 foreground mean ± std |
|---|---:|---:|---:|---:|---:|
| A0 / FG-only | 149 | 0.105977 | 0.141302 | 0.114676 ± 0.004299 | 0.152901 ± 0.005731 |
| A-ratio | 149 | 0.373760 | 0.242183 | 0.387601 ± 0.005139 | 0.257218 ± 0.005964 |
| Dense-v2 | 149 | 0.811501 | 0.751257 | 0.804636 ± 0.008963 | 0.742151 ± 0.011860 |

## Checkpoint-selection audit

- A-ratio's legacy BG-inclusive best is epoch 10, while its foreground-patient best is epoch 13 (`0.367150`). This is direct evidence that BG-inclusive checkpoint selection is invalid for the formal ladder.
- Dense-v2 has the same BG and foreground best epoch, 136.
- Previously completed A and B were independently rechecked from their full validation JSONL: A is epoch 56 under both metrics; B is epoch 124 under both metrics. They do not require rerunning solely for checkpoint-selection correction.
- The previously completed `B` used right-angle geometry and is retained only as `basic_geometry_diagnostic`; it is not a paper component or a formal rung. The rebuilt formal `A` uses the paper's shared flip/random-rotation augmentation.
- New formal runs select and gate only on `foreground_patient_mean`. BG-inclusive mean remains logged as a diagnostic.

The complete machine-readable values and checkpoint SHA-256 digests are in `results/static_reference_results.csv`. Checkpoint bodies were not copied; the external evidence directory contains metadata and the original small JSON/JSONL records only.
