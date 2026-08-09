# Current global gates

| Gate | Status | Evidence |
|---|---|---|
| DENSE_SANITY_GATE | PASS | ZS U-Net 16-slice eval-mode aggregate 0.966683 at step 450; minimum class 0.949119 |
| ZS_STATIC_TASK1_GATE | NO-GO | A-to-C1 drop 0.036433 exceeds registered 0.03 threshold |
| DOMAIN_PCE_GATE | RUNNING_TINY | Pilot not authorized until all six dense/PCE tiny gates pass |
| ORGAN_PCE_GATE | RUNNING_TINY | Pilot not authorized until all four dense/PCE tiny gates pass |
| DOMAIN_ZS_GATE | BLOCKED | blocked_by_static_gate |
| ORGAN_ZS_GATE | BLOCKED | blocked_by_static_gate |

Global decision remains `DECISION: NO-GO-ZS`.
