# ScribbleCL fixed core protocol

## Paper display names and internal identifiers

The thesis display name **ScribbleCL** denotes the configuration that combines
the cited weak-supervision current-task loss with old-model continual
protection.  Internal code and log identifiers remain unchanged: `ZS` maps to
the cited weak-supervision loss (`\mathcal{L}_{\mathrm{WS}}` in the thesis),
`ZS-FT` maps to `WS-FT`, and `ZS-ScribbleMiB` maps to `ScribbleCL`.
`PCE/ZS` in internal analysis maps to `PCE/WS` in the thesis.  These mappings
do not alter configurations, checkpoints, raw logs, or results.

## MMWHS Class-CL

The task order is read from the Benchmark implementation: task 1 uses local
labels 1--3 from `myo_lv_la.h5` as global classes 1--3; task 2 uses local
labels 1--2 from `ra_rv.h5` shifted to global classes 4--5; task 3 uses local
labels 1--2 from `ao_pa.h5` shifted to global classes 6--7.  Channel 0 is
background and the model always has eight output channels.

Each training HDF5 has its original train/validation/test split.  The local
adapter reads the original arrays without changing the split.  Dense training
masks are loaded only by `generate_mmwhs_scribbles.py`, which writes sparse
`int16` labels (`-100` is ignore).  The training dataset never opens a dense
training-label dataset.

## Sparse-label protocol

Foreground scribbles are deterministic skeleton pixels from only the current
stage's active labels, with one-pixel dilation constrained to the source class.
No background scribble is used in the core protocol: body/background cannot be
identified safely without using old or future dense labels.  All other pixels,
including real background and old/future structures, are `ignore_index=-100`.
The same `(scribble_seed, model_seed)` pair uses the same generated scribbles
for all paired methods.

## Losses and history access

PCE is cross entropy only on non-ignore sparse labels.  ZS adds image-space
consistency and active-class spatial-ratio regularization; these terms only use
the active current-stage channels.  ScribbleMiB freezes the preceding-stage
model.  On pixels without a current foreground scribble it distils only old
channels (background plus already-seen foreground), and never includes future
channels.  Current scribble pixels are excluded from distillation.  No method
stores or replays old images.

Task-1 checkpoints are shared by each supervision family and seed: PCE is
shared by PCE-FT/PCE-ScribbleMiB, ZS by ZS-FT/ZS-ScribbleMiB, and dense by
Dense-FT/Dense-MiB.  Parent checkpoint SHA256 is recorded in every child run.
