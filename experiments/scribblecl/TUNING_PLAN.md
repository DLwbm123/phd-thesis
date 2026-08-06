# Static Task-1 optimizer gate (pre-registered)

Legacy note: the prior PCE/ZS family-specific LR rule is revoked because it confounded method and optimizer. Its runs remain diagnostic-only.

Scope: MMWHS Task-1, seed 42, v2 S2 FG+BG scribbles, ResUNet32, commit `3299a1e`, validation only. Compare exactly two candidates:

- Adam, lr `1e-4`, weight decay `1e-4` (original ZS source setting);
- plain SGD, lr `0.004`, no momentum or weight decay (bounded Benchmark-derived stability candidate).

Both candidates run level A (PCE-FG+BG) for 20 full epochs with the same initialization hash, scribble hash, epoch-wise batch permutation and budget. No test set is loaded.

Selection rule, applied once after both complete:

1. reject a candidate with NaN/Inf or a missing current class in each of its final five validations;
2. compare the mean Benchmark validation Dice over the final five epochs;
3. if means differ by less than 0.01, choose the candidate with lower final-five standard deviation;
4. freeze the selected optimizer and LR unchanged for A--E full 150-epoch runs.

No additional optimizer or LR trial is authorized by this task.
