# ScribbleCL

This independent workspace evaluates scribble-supervised Class-CL on the
MMWHS three-stage protocol.  It does not modify either source tree.  The
implementation reads dense training labels only inside the offline scribble
generator; training datasets expose images, sparse labels, and protocol
metadata only.  See `PROTOCOL.md` before running an experiment.

The source audit and all result claims are deliberately separated: no value in
`results/` is an experiment result unless its run manifest is complete.
