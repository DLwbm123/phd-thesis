# EWC penalty engineering optimization

Date: 2026-08-09

The original implementation summed one Fisher-weighted quadratic tensor per
parameter on every batch. Profiling on the selected ResUNet32 showed that the
many small GPU kernels dominated EWC throughput on LiTS and the larger prostate
centers.

The replacement concatenates the same selected parameters in deterministic
name order and evaluates the same diagonal quadratic in one vector. Fisher,
`theta_star`, lambda, gamma and parameter scope are unchanged. Automated tests
compare both the scalar value and every parameter gradient. Result:
`35 passed`.

Isolated GPU microbenchmark (50 calls, same model/state):

| Implementation | Seconds/call |
|---|---:|
| Parameter-wise | 0.004350 |
| Vectorized | 0.000701 |

Absolute value difference: `0.0`.

The incomplete pre-optimization EWC runs are preserved with status
`diagnostic_aborted_penalty_optimization` and validity
`invalid_engineering`; they are excluded from result aggregation. Replacement
runs start from the exact same paired FT stage-1 checkpoints and repeat every
formal stage. No completed result was discarded or selectively reported.
