# ZS fidelity audit

Decision: **NO-GO-ZS**. The archived method named `zs` is not ZScribbleSeg; it is `PCE-Ratio-Flip-Legacy` and `diagnostic_only`. No continual-learning run is authorized.

| Item | Original ZScribbleSeg | Current legacy | Verdict |
|---|---|---|---|
| output | U-Net Softmax probabilities | ResUNet32 logits | incompatible without adaptation |
| objective | sparse CE, PuzzleMix, Cutout/rotation consistency, integrity, warm-up EM, spatial ranking, pseudo correction | PCE, foreground-ratio MSE, flip MSE | not a port |
| scribble | explicit BG/FG/unknown channels | FG/unknown only | mismatch |
| optimization | Adam, lr 1e-4, wd 1e-4 | SGD; prior PCE/ZS LR differed | confounded |
| checkpoint | validation-Avg selection | final epoch called `best.pt` | incorrect |

The legacy ratio compares class fractions among annotated pixels with mean foreground probability over the whole image. Fixed-batch tests show gradients on unknown pixels and whole-image foreground suppression on a background-only annotated slice. It is excluded from the formal rebuild.

Original checkpoint evaluation is recorded separately in `ORIGINAL_ZS_REPRO_AUDIT.md`. The earlier connection diagnosis used the wrong address and is superseded. No metric is inferred from checkpoint filenames. A-E training remains forbidden until the label-protocol and static gates pass.
