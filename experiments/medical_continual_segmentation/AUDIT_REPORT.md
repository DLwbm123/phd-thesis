# Audit report

The executable task definitions and H5 inventory were audited on 2026-08-09. Class order and shifts are T1 labels 1-3, T2 labels 1-2 shifted to 4-5, and T3 labels 1-2 shifted to 6-7. Domain and organ file order matches the protocol documents. All images are single-channel 256x256 slices; patient boundaries come from the split-specific H5 arrays.

The prostate H5 masks contain fractional boundary values introduced upstream. The executable Benchmark applies a same-size OpenCV resize and then converts the target to Torch `long`, which truncates those values and retains only exact `1.0` as foreground. The unified loader deliberately reproduces that conversion without a redundant same-size resize. Audit output records both raw values and post-conversion values, avoiding the misleading duplicate-zero display produced by casting a unique-value list.

The previous training implementation is not a final evidence source because it used a different backbone. Its data-order, split, sparse-annotation, EWC/SI, Fisher, metrics and infrastructure logic were reviewed and reimplemented under the anonymous runtime, then subjected to U-Net-specific tests and gates. Diagnostic run preservation is recorded separately.
