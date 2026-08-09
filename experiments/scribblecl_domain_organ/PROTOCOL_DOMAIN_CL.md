# Frozen Domain-CL protocol

- Order: A -> B -> C -> D -> E -> F, using the immutable HDF5 arrays listed in
  `DATA_MANIFEST.md`.
- Network: ResUNet32 backbone plus one shared two-channel BG/prostate head.
- Current supervision: deterministic v2 S2 scribbles; PCE only on explicit BG
  and FG; unknown=-100.
- History access: parameters and regularizer state only; no old image or label.
- EWC scope: backbone and shared head. Fisher uses current sparse PCE only.
- Training: SGD, 150 epochs, batch 8, LR 0.008, x0.5 after epoch 80.
- Checkpoint: fixed last epoch; test data never selects a checkpoint or
  hyperparameter.
- Matrix: evaluate all six domains after every stage, including future domains.
- Metrics: A-Dice, relative BWTR, RMA, E-FWT, current-domain Dice, final old
  mean, per-domain Dice, annotation ratio, time, peak memory, parameter count
  and regularizer bytes.
