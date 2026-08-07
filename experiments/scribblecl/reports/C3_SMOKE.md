# C3 two-batch smoke

Decision: `PASS`.

Full unit-test prerequisite: `60 passed`.
Both runs used initialization `1a4ff6895aa40b51149882142047dd5349da1b44296bb91cafdd70546e09458f` and parameter max absolute difference was `0.0`.

| Check | Result |
|---|:---:|
| both_completed | True |
| same_initialization | True |
| exact_parameter_repeat | True |
| exact_loss_repeat | True |
| finite | True |
| three_classes_nonempty | True |
| background_and_foreground_not_collapsed | True |
| component_has_valid_pixels | True |
| component_gradient_finite | True |
| sparse_only | True |
| test_set_unused | True |
| future_logits_excluded | True |

| Component | Raw loss | Weighted loss | Gradient norm | Valid pixels |
|---|---:|---:|---:|---:|
| pce_unmixed | 1.33551311 | 1.33551311 | 7.24103975 | 3387.5 |
| pce_mixed | 1.32402331 | 1.32402331 | 7.97003508 | 12756.5 |
| global | -0.97809237 | -0.04890462 | 0.01007828 | 516096.0 |
| shape | 0.00000000 | 0.00000000 | 0.00000000 | 0.0 |
| spatial | 0.00000000 | 0.00000000 | 0.00000000 | 0.0 |

Prediction fractions: `{"0": 0.0011962890625, "1": 0.8677003479003906, "2": 0.001733856201171875, "3": 0.1293695068359375}`.
Non-empty rates: `{"1": 1.0, "2": 1.0, "3": 1.0}`.
Foreground patient mean after two optimization steps: `0.00996609`; this is a smoke diagnostic, not an experimental result.

No test labels or dense training labels were read. Future channels were excluded by the active-logit mask and the corresponding regression test.
