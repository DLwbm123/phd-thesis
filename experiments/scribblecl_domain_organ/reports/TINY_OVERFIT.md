# Dense and sparse-PCE tiny-overfit gates

Date: 2026-08-09

All checks use a fixed set of 12 training slices from the named current
domain/task. Dense checks are diagnostic only and require foreground Dice
`>= 0.95`. Sparse checks train exclusively on known scribble pixels and require
a finite, material reduction in sparse PCE. Dense Dice printed by a PCE check
is diagnostic and is not a PCE pass criterion.

## Domain-CL

| Center | Dense final step | Dense foreground Dice | PCE final step | PCE loss (initial -> final) | Status |
|---|---:|---:|---:|---:|---|
| A | 125 | 0.963137 | 50 | 0.698547 -> 1.18e-9 | PASS |
| B | 1400 | 0.951053 | 50 | 0.652197 -> 5.30e-9 | PASS |
| C | 125 | 0.964355 | 75 | 0.635470 -> 0.081890 | PASS |
| D | 425 | 0.955551 | 150 | 0.613820 -> 0 | PASS |
| E | 100 | 0.972662 | 50 | 0.679070 -> 2.33e-6 | PASS |
| F | 225 | 0.950769 | 50 | 0.772642 -> 0.010707 | PASS |

Result: 12/12 checks pass.

The initial Center-B dense diagnostic used microbatches whose final
BatchNorm update did not represent the fixed 12-slice batch: its training loss
was small while eval-mode Dice was only 0.695. Repeating the diagnostic with
the full fixed batch removed this inconsistency and reached 0.951053. This did
not alter the registered pilot recipe.

## Organ-CL

| Task | Dense final step | Dense foreground Dice | PCE final step | PCE loss (initial -> final) | Status |
|---|---:|---:|---:|---:|---|
| T1 LA/LGE-MRI | 350 | 0.959372 | 50 | 0.645035 -> 8.94e-9 | PASS |
| T2 prostate/MRI | 400 | 0.959663 | 125 | 0.618021 -> 0 | PASS |
| T3 liver/CT | 175 | 0.954423 | 150 | 0.630238 -> 0.023669 | PASS |
| T4 brain/MRI | 125 | 0.954435 | 50 | 0.696516 -> 0 | PASS |

Result: 8/8 checks pass.

The initial T3 dense diagnostic diverged with Adam at `1e-3`. A bounded
diagnostic retry used the identical 12 slices and Adam at `1e-4`, reaching
0.954423. This change is restricted to the tiny-overfit diagnostic: the formal
pilot remains the frozen benchmark recipe (SGD, learning rate 0.008, 150
epochs/task).

## Artifact locations

- Domain: `/remote-home/wangbomin/ScribbleCL/scribblecl_domain_organ_20260809/tiny_v2/domain`
- Organ: `/remote-home/wangbomin/ScribbleCL/scribblecl_domain_organ_20260809/tiny_v3/organ`

The task-specific Organ heads were created dynamically for these checks; heads
for future tasks were not instantiated early. No replay buffer, past image, or
historical image cache was used.
