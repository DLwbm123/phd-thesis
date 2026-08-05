# Porting plan and boundaries

`protocol` ports the Benchmark map as explicit metadata. `model` ports the
ResUNet32 topology with a fixed eight-channel head. PCE is sparse-label
supervision. ZS uses only current-class ratio/consistency terms. ScribbleMiB
distils only old channels on non-scribble pixels and is an adaptation, not
standard MiB. Shape correction/pseudo-label expansion are deliberately absent:
their original dense/inferred masks are not yet proven safe for old/future
class non-access.
