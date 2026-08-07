# Task-1 class-wise shape oracle

This audit reads MMWHS Task-1 **training labels only**. Validation and test labels are not used.
The pre-registered eligibility rule is mean largest-component retention >= 0.99 and at least 95% of non-empty slices with retention >= 0.95.

| Class | Non-empty slices | Multi-component slices | Mean retention | P05 | Minimum | Fraction >=0.95 | Eligible |
|---|---:|---:|---:|---:|---:|---:|:---:|
| 1 MYO | 1011 | 184 | 0.995975 | 0.997045 | 0.333333 | 0.986152 | True |
| 2 LV | 884 | 27 | 0.998121 | 1.000000 | 0.581395 | 0.992081 | True |
| 3 LA | 806 | 70 | 0.987296 | 0.946573 | 0.500000 | 0.946650 | False |

Formal shape-loss classes: 1 MYO, 2 LV.

Machine-readable eligibility: `{"1": true, "2": true, "3": false}`.
