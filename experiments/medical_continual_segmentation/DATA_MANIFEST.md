# Data manifest

The runtime reads the Benchmark H5 files without rewriting them. `scripts/audit_data.py` verifies the immutable SHA-256 values in `medcl/data/protocols.py`, the train/validation/test tensors, the true `patient_info_<split>` arrays, label sets, finite values, and normalization statistics. Test data is evaluation-only and never selects epochs or hyperparameters.

Sparse archives contain exactly one `annotations` array and are generated into a neutral external data root. Each sidecar records foreground, background and unknown pixels, zero-foreground slices, minimum/maximum valid pixels and a content digest.
