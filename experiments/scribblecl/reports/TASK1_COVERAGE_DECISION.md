DECISION: NO-GO-ZS

Commit: `dcf4aa68993e4915381a96bbac173dea4c9e0409`.

No coverage budget is frozen and no Task-1 seed-43 confirmation is authorized.

The decision uses validation results only.  PCE has a modest B1-to-B2 mean-Dice increase (0.12099 to 0.13640) followed by a B3 decline (0.12461); it is not a monotonic recovery curve.  ZS does not recover as coverage grows (0.07438, 0.07228, 0.07246 for B1/B2/B3) and is substantially below the paired PCE at every budget.  All three predicted classes are non-empty, so this is not an all-background or NaN collapse; predicted-pixel statistics nevertheless show severe overprediction in several classes and require module-level diagnosis.

The dense control is finite and non-empty, the label mapping is independently confirmed, future logits are masked in the audited validation calculation, and the zero-supervision audit has no positive-slice scribble omission.  Therefore increasing the same centreline to B3 does not resolve the ZS deficit, and choosing B2 merely because it has the largest PCE mean would be a result-driven protocol choice.

Static source audit identifies the immediate incompatibility: the current `zs_current_task_loss` is PCE plus a simple active-class mixture-ratio MSE and horizontal-flip consistency.  It does **not** implement the ZScribbleSeg EM estimator, spatial prior, PuzzleMix, Cutout, pseudo correction, or integrity/shape components.  Those absent components consequently have no enable epoch or logged contribution in the coverage queue.  A fresh, explicitly logged Task-1 ZS diagnostic is required before reopening the coverage gate; it must preserve the same split, seed, budget, training budget, and validation-only selection rule, and must not be tuned on test data.

Consequences: do not run PCE/ZS Task-1 seed 43, do not implement or run ScribbleMiB-v2 pilot/core training, and do not start core seeds 43/44 until this blocker is resolved and a new coverage gate passes.
