# Data audit 2026-08-09

All 14 immutable H5 files matched the expected SHA-256. Every image and mask tensor is 256x256 by slice. Split-specific patient boundaries were read from `patient_info_train`, `patient_info_val`, and `patient_info_test`; no validation array was substituted for a training array. All image values were finite.

## Class

| Task | Train/val/test slices | Patients | Converted labels | SHA-256 |
|---|---:|---:|---|---|
| T1 MYO/LV/LA | 1500/200/900 | 15/2/9 | 0-3 | `1f3d2c...f4c1` |
| T2 RA/RV | 1500/200/900 | 15/2/9 | 0-2, shifted to 0/4/5 | `dc2740...ec3d` |
| T3 AO/PA | 1500/200/900 | 15/2/9 | 0-2, shifted to 0/6/7 | `785b82...5834` |
| Whole-heart final test | -/-/1350 | -/-/9 | 0-7 | `4d22c5...011f` |

Class images have mean approximately 0 and standard deviation approximately 1 in every split.

## Domain

| Center | Train/val/test slices | Patients | SHA-256 |
|---|---:|---:|---|
| A BIDMC | 301/94/126 | 7/2/3 | `66e24b...c52` |
| B HK | 168/48/72 | 7/2/3 | `9729bd...f06` |
| C ISBI | 345/75/158 | 18/4/8 | `9a1a95...2d3` |
| D UCL | 166/52/100 | 7/2/4 | `76ef63...8a9` |
| E ISBI 1.5 | 582/130/254 | 18/4/8 | `2370e1...126` |
| F I2CVB | 704/192/320 | 11/3/5 | `1c1f49...79e` |

## Organ

| Task | Train/val/test slices | Patients | SHA-256 |
|---|---:|---:|---|
| T1 left atrium MRI | 762/153/298 | 25/5/10 | `4b9cc2...26d` |
| T2 prostate MRI | 166/52/100 | 7/2/4 | `76ef63...8a9` |
| T3 liver CT | 1421/343/496 | 17/4/7 | `b0a2a0...b9c` |
| T4 brain-tumor MRI | 1963/894/1223 | 50/20/30 | `84edef...90e` |

The prostate masks have raw fractional boundary values. Executable-code parity requires same-size resize followed by `long` conversion, so the training/evaluation labels are binary 0/1 with fractional values truncated. Other organ masks are raw binary 0/1. Test data is not used for hyperparameter, epoch, or gate selection.
