# Frozen Organ-CL protocol

- Order: LAScarQS LA -> PROMISE12 prostate -> LiTS liver -> FeTS brain tumor.
- Network: shared ResUNet32 backbone plus one two-channel BG/foreground head per
  task. Task identity is supplied at evaluation; this is not task-free.
- Completed heads are frozen. Only the current head and shared backbone train.
- EWC and SI constrain only the shared backbone. Current head Fisher is derived
  from current sparse PCE but head parameters are not stored or penalized.
- No old images, old-image distillation, replay or historical cache.
- Training/checkpoint policy matches Domain-CL.
- Matrix: evaluate every seen task with its corresponding head after each
  stage; future cells are inactive. Metrics are A-Dice, relative BWTR, RMA,
  current-task Dice, final old mean, parameter/head growth and resources.
- E-FWT is prohibited because output semantics differ.
