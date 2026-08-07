# E two-batch smoke

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
| pce_unmixed | 1.32635987 | 1.32635987 | 7.24103975 | 3387.5 |
| pce_mixed | 1.32685071 | 1.32685071 | 7.97003508 | 12752.5 |
| global | -0.97673324 | -0.04883666 | 0.01007828 | 516096.0 |
| shape | 1.11078697 | 1.11078697 | 6.87383938 | 232534.0 |
| spatial | 0.61047035 | 0.61047035 | 2.51573229 | 1041803.0 |

Prediction fractions: `{"0": 0.000997161865234375, "1": 0.896538314819336, "2": 0.0017049407958984375, "3": 0.10075958251953125}`.
Non-empty rates: `{"1": 1.0, "2": 1.0, "3": 1.0}`.
Foreground patient mean after two optimization steps: `0.00966033`; this is a smoke diagnostic, not an experimental result.

No test labels or dense training labels were read. Future channels were excluded by the active-logit mask and the corresponding regression test.
