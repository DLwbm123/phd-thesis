# ScribbleCL Domain-CL / Organ-CL

This independent, replay-free workspace implements sparse PCE, online EWC and
SI for the executable Benchmark Domain-CL and Organ-CL scenarios. It does not
implement MiB, ScribbleMiB, experience replay, generated replay, or historical
image caching.

The remote Benchmark code and HDF5 files are read-only. Dense training labels
are reachable only from the audit, offline scribble generator and tiny dense
gate. Formal weak training and Fisher loaders expose only current images and
FG/BG/unknown sparse labels.

Current global decision is `NO-GO-ZS`. ZS configuration files are deliberate
blocked records and the runner raises if asked to use them.

The selected formal PCE backbone is `resunet32`: the ZS U-Net dense sanity gate
passes, but the required static ZS gate does not. Both backbones and the
single/multi-head adapters remain implemented and tested.
