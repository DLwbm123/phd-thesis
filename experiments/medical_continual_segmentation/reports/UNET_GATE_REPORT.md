# U-Net gate report

Date: 2026-08-09. Seed: 42. Device class: NVIDIA A100 40 GB.

## Static and unit gates

- Anonymous runtime lint: PASS, including project aliases and author-name tokens.
- Pytest: 29 passed. This includes 212x212 original-weight probability parity at tolerance `1e-6`, 256x256 same-size output, static four-channel Class stage-1 parity, future-block inactivity, logits-only cross entropy, scenario-specific EWC/SI scope, sparse-only Fisher, checkpoint state and enhanced-method blocking.
- Dry-runs: Class PCE-FT PASS with 4 channels; Domain PCE-EWC PASS with nonnegative Fisher; Organ PCE-FT PASS with a two-channel task head.

## Tiny overfit

All required U-Net dense gates passed the aggregate foreground Dice threshold of 0.95. Class T1 reached 0.960382. Domain A-F reached 0.954812-0.960518. Organ T1-T4 reached 0.950361-0.963526; Liver required the declared extended retry and passed at step 1375 with 0.951025.

All PCE tiny gates passed with known-pixel accuracy 0.983080-1.000000, finite decreasing loss, nonempty current foreground, and a loader whose `exposes_dense` contract is false. Dense-mask Dice is logged only as a diagnostic and is not a PCE pass threshold. Sparse archive/unit evidence separately verifies background `0`, current foreground, and unknown `-100`.

Exact per-task values are in `results/unet_tiny_gates.csv`.

## Full-data one-epoch PCE smoke

Class PCE-FT, Domain PCE-EWC and Organ PCE-FT each completed one full training epoch, validation/test evaluation, an atomic `last.pt`, and a stage checkpoint. The Domain smoke Fisher used two current-task sparse-only batches: 6,825 known pixels, 25,759,262 scoped parameters, minimum 0, maximum 0.124042, and finite nonnegative values.

The first stage-copy attempt exposed a filesystem extended-attribute error after valid `last.pt` files had been written. Replacing metadata-copying `copy2` with content-only `copyfile`, then resuming through `main.py --resume last.pt`, completed all three smokes. This is direct resume-path evidence; no checkpoint was deleted and no epoch was retrained for the successful Organ/Class resumptions.

Smoke checkpoint SHA-256 values are:

- Class: `72219ca50cac04a3870f22c711ca391668477d88f4954c6b149a9bc13cc138e8`
- Domain EWC: `d079621cf1e104598b2a59eec1f4cb3e49638de6d6d067d8604f505b7b3fe1b2`
- Organ: `eb2f17f7be1735614620d0300ed6ee4f7db94744e0051089f750dba9746d060a`

Enhanced methods remain `blocked_by_static_gate` and were not trained.
