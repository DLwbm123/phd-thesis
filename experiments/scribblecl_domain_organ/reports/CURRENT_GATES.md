# Current global gates

| Gate | Status | Evidence |
|---|---|---|
| DENSE_SANITY_GATE | PASS | ZS U-Net 16-slice eval-mode aggregate 0.966683 at step 450; minimum class 0.949119 |
| ZS_STATIC_TASK1_GATE | NO-GO | A-to-C1 drop 0.036433 exceeds registered 0.03 threshold |
| DOMAIN_PCE_GATE | FT_COMPLETE_EWC_RUNNING | Tiny gates pass; PCE-FT complete; replacement PCE-EWC formally passed stage 2 and is running |
| ORGAN_PCE_GATE | FT_EWC_RUNNING | Tiny gates pass; PCE-FT and replacement PCE-EWC are running; both are past stage 2 |
| DOMAIN_ZS_GATE | BLOCKED | blocked_by_static_gate |
| ORGAN_ZS_GATE | BLOCKED | blocked_by_static_gate |

Global decision remains `DECISION: NO-GO-ZS`.

The seed-42 pilots are the only formal runs currently authorized. PCE-EWC is
started only from the paired PCE-FT Task-1 checkpoint. Seeds 43/44 and PCE-SI
remain blocked until the complete seed-42 gate is evaluated.
