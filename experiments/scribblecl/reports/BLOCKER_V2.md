# ScribbleCL-v2 blocker

DECISION: NO-GO-ZS

The coverage gate is blocked, not failed-over.  The completed seed-42 validation-only coverage experiment shows no recovery of ZS from B1 through B3 and a consistent material deficit relative to paired PCE.  The zero-supervision audit found no positive-slice omission, the dense control is finite and non-empty, and label mapping / future-logit masking are verified.

The current portable ZS implementation is deliberately reduced relative to the read-only ZScribbleSeg source: it has active-class ratio MSE plus flip consistency only.  The original source contains PuzzleMix, Cutout, EM ratio estimation, spatial Gated-CRF prior, pseudo correction, and integrity/shape operations; these are absent and cannot be blamed from current logs or silently claimed as enabled.

Required minimum unblock sequence:

1. add per-epoch validation, component-loss, gradient-norm, finite-value, and prediction-distribution logging without changing the completed coverage artifacts;
2. add fixed Task-1 seed-42 validation-only diagnostics for PCE, PCE+augmentation/consistency, PCE+prior/shape, and full compatible ZS, each with current-task-only masks and leakage tests;
3. rerun a complete coverage gate under one frozen diagnostic commit if a model-output-changing ZS repair is made;
4. require the resulting coverage decision to be `COVERAGE-B1`, `COVERAGE-B2`, or `COVERAGE-B3` before seed 43 or MiB-v2 work.

LegacyConditionalKD remains diagnostic-only.  Its old results are invalid for the formal table because they predate future-logit evaluation masking and do not use unbiased MiB.
