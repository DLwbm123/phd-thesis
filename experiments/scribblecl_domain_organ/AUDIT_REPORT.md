# Domain/Organ executable audit

## Fact sources

- Executable code: `/remote-home/wangbomin/CL_Benchmark/code/CL_Benchmark`.
- Data: `/remote-home/wangbomin/CL_Benchmark/data`.
- Final manuscript protocol: `sources/benchmark/Benchmark_pa/main.tex` and
  `supplementary.tex`.
- ZS gate evidence: latest `ZS_STATIC_TASK1_GATE_V2.md`, decision NO-GO-ZS.

Remote executable hashes include `seq_prostate.py=f66405ff...`,
`seq_task_incre.py=1fb93ad5...`, `ResUnet.py=0d99fb0f...`,
`ewc_on.py=80ed8ddd...`, `si.py=63378a9f...`, and
`metrics.py=71819baa...`. Several differ from the old macOS copy, so the remote
files were audited directly.

## Domain-CL

The executable task ids are exactly
`1:BIDMC -> 2:HK -> 3:ISBI -> 4:UCL -> 5:ISBI_1.5 -> 6:I2CVB`.
The Benchmark protocol names these A through F and assigns sources
NCI-ISBI13 (A/B), I2CVB (C), PROMISE12 (D/E/F). Filename comments in the
loader are internally inconsistent; this workspace preserves both the exact
executable filename mapping and the manuscript source grouping instead of
renaming data.

Images are stored as axial 256x256 slices. The protocol reports Center C
cropping/alignment followed by per-case non-zero-voxel mean/std normalization.
The executable loader performs only same-size OpenCV resize and float casting;
it adds no normalization. Prostate HDF5 labels contain interpolated values in
(0,1); the executable `torch.long()` cast makes only stored value 1 foreground.
The adapter reproduces that behavior explicitly.

The model uses one shared two-channel BG/prostate head and never consumes a
domain id. Evaluation after each stage includes all six domains, retaining the
full 6x6 matrix for A-Dice, relative BWTR, RMA and Domain-only E-FWT.

## Organ-CL

The exact executable order is `UtahI -> UCL -> Lits -> brain`, corresponding to
LAScarQS left-atrium LGE MRI, PROMISE12 prostate T2 MRI, LiTS liver CT and FeTS
2021 brain-tumor FLAIR MRI. Images are stored as 256x256 slices; the protocol
reports per-image zero-mean/unit-variance normalization. The loader adds no
further normalization. LiTS/FeTS stored labels are binary; UCL retains the
fractional-boundary behavior described above.

Task identity is known at evaluation. The model has a shared backbone and four
binary heads. Completed heads are frozen. EWC/SI enumerate only backbone
parameters. Organ evaluation stores a 4x4 matrix and does not define E-FWT.

## Training and regularizers

Benchmark training is plain SGD, 150 epochs/task, batch 8, initial LR 0.008,
factor 0.5 after epoch 80. EWC is online, with diagonal consolidation
`F <- gamma*F + F_current`. The executable parser default is gamma 1.0, while
the final supplementary protocol states the actually selected lambda 1 and
gamma 0.1. Formal configs freeze lambda 1, gamma 0.1 and record this conflict.
SI freezes the Benchmark values c=5 and xi=1.

The original Benchmark Fisher uses dense CE and does not normalize the summed
diagonal. That access rule is invalid for this weak-supervision task. Here the
only intentional change is the required sparse Fisher contract: eval mode, no
augmentation, current training images, known BG/FG pixels, PCE only, batch
average, finite nonnegative diagonal. No dense mask, pseudo label, shape or
spatial loss can enter the function.

Patient-level Dice follows the executable volume grouping and averages BG and
FG classes with epsilon 1e-5. A-Dice, relative BWTR, RMA and E-FWT match the
final manuscript equations and the remote `metrics.py` corrected relative
BWTR implementation.
