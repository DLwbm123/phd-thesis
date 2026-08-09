# Method and gate protocol

`supervision=dense|pce|zs` is explicit. Dense is restricted to audit,
generation, evaluation and sanity references. PCE is sparse CE on values 0/1;
-100 is ignored. `zs` raises at runtime while the static gate is NO-GO.

v2 S2 generation uses a 3px foreground skeleton clipped to the current binary
foreground plus deterministic sparse BG strokes at least 5px away. Generation
receives only one current-task binary mask and cannot encode future identities.
S1/S3 are permitted only as a bounded diagnosis after a task-specific PCE
failure.

EWC uses online diagonal consolidation. Domain selects all trainable backbone
and shared-head parameters. Organ selects only shared-backbone parameters.
Fisher accepts only a weak loader and uses sparse PCE, eval mode, no
augmentation and current training data.

SI follows the executable accumulation `small_omega += lr * grad^2`, with
`big_omega += small_omega / (delta_theta^2 + xi)`. Its scope matches EWC.

Seed 42 must complete all implementation, tiny and stage-2 gates before a full
sequence is valid. Seeds 43/44 are blocked until the corresponding seed-42
report begins with GO. SI remains seed-42 only. No seed may be selectively
omitted after launch.
