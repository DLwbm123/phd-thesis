# C1 two-batch smoke

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
| pce_unmixed | 1.33495051 | 1.33495051 | 7.24103975 | 3387.5 |
| pce_mixed | 1.34139889 | 1.34139889 | 7.92290592 | 4600.5 |
| global | 0.00000000 | 0.00000000 | 0.00000000 | 0.0 |
| shape | 0.00000000 | 0.00000000 | 0.00000000 | 0.0 |
| spatial | 0.00000000 | 0.00000000 | 0.00000000 | 0.0 |

Prediction fractions: `{"0": 0.000222625732421875, "1": 0.8648741149902344, "2": 0.001794281005859375, "3": 0.13310897827148438}`.
Non-empty rates: `{"1": 1.0, "2": 1.0, "3": 1.0}`.
Foreground patient mean after two optimization steps: `0.01000028`; this is a smoke diagnostic, not an experimental result.

No test labels or dense training labels were read. Future channels were excluded by the active-logit mask and the corresponding regression test.
