# ScribbleCL current protocol

## Scope

ScribbleCL uses the Benchmark Domain-CL, Class-CL and Organ-CL task sequences, splits, backbone and evaluation metrics. Current-task training uses sparse scribble labels. ZSDERpp additionally has access to a capacity-limited historical buffer; the full historical training sets remain unavailable.

## Current-task supervision

The direct supervision is partial cross entropy on valid scribble pixels. The only additional weak-supervision terms are the global-consistency loss and the spatial-prior loss cited through `zhang2026zscribbleseg`:

```text
L_cur = L_PCE + lambda_g L_global + lambda_s L_spatial
```

No other loss from the source weak-supervision work is used in the current method, and its original experiment values are not evidence for ScribbleCL.

## Unified ZSDERpp objective

Each historical entry contains an image, its scribble label, a stored reference feature and a task identifier. For every stage after the first, the buffer objective is fixed as:

```text
L_buffer = 0.5 L_feature
         + 0.5 L_PCE^buffer
         + 1.0 L_global^buffer
         + 0.1 L_spatial^buffer

L_ZSDERpp = L_cur + L_buffer
```

The first stage has an empty buffer, so `L_buffer=0`. The task identifier routes replay samples to the appropriate output head when required.

## Setting-specific output handling

- Domain-CL uses one shared output head and unchanged label semantics.
- Organ-CL uses task-specific output heads; the stored task identifier selects the historical head during replay.
- Class-CL uses an expanding shared label space. Current background probability aggregates the model background and previously learned classes, while old-model consistency matches old classes individually and matches the old background to the sum of current background and newly introduced classes. This background-semantic correction is an internal component of ZSDERpp, not a separate method.

## Training and evaluation

All compared methods use the same data split, task order, scribble files, ResUNet32 backbone and 150-epoch task budget. The current implementation uses `lambda_g=0.05`, `lambda_s=1`, and activates the spatial term after a 15-epoch warm-up. The buffer uses the fixed `0.5/0.5/1.0/0.1` coefficients above.

Domain-CL reports A-Dice, BWTR, RMA and E-FWT. Class-CL reports A-Dice, BWTR, RMA and WCD. Organ-CL reports A-Dice, BWTR and RMA. Dense test labels are used only for evaluation.

## Current result boundary

The completed Domain-CL point estimates are:

| Method | A-Dice | BWTR | RMA | E-FWT |
|---|---:|---:|---:|---:|
| Dense-Sequential | 0.676 | -0.237 | 1.086 | 0.260 |
| PCE-Sequential | 0.248 | -0.545 | 0.776 | 0.133 |
| ZS-Sequential | 0.510 | -0.324 | 0.732 | 0.234 |
| ZS-EWC | 0.543 | -0.298 | 0.761 | 0.216 |
| ZS-GPM | 0.612 | -0.206 | 0.808 | 0.241 |
| ZSDERpp | 0.701 | -0.152 | 0.899 | 0.225 |

These are point estimates from the author-updated chapter table. No dispersion or statistical test is supplied in the current archive. Class-CL and Organ-CL method applicability is defined, but their result values must not be inferred from Domain-CL.
