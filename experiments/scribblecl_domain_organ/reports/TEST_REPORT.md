# Test report

Date: 2026-08-09

Command run on the experiment server:

```bash
cd /remote-home/wangbomin/ScribbleCL/experiments/scribblecl_domain_organ_20260809
BENCHMARK_ROOT=/remote-home/wangbomin/CL_Benchmark/code/CL_Benchmark \
ZS_ORIGINAL_ROOT=/root/ZScribble/ZScribbleSeg_MSCMR \
PYTHONPATH=. /root/anaconda3/bin/python -m pytest -q tests
```

Result after adding the persisted-regularizer-state and vectorized-penalty
contracts: `35 passed in 52.08s`.

This includes parity against the executable Benchmark ResUNet32 feature path,
212x212 four-channel parity against the original ZS U-Net, the 256x256 output
contract, shared/task-specific head behavior, weak-loader access boundaries,
sparse-only Fisher, online consolidation, SI/EWC parameter scope, and the
Domain/Organ metric definitions. The canonical three-pixel v2 artifact is also
checked to carry the registered S2 strategy name. EWC state is checked to
contain both the Fisher diagonal and `theta_star`; the pilot persists that state
after every stage without placing it under Git. The vectorized EWC penalty is
also checked against the original parameter-wise value and every parameter
gradient.
