# Static Task-1 optimizer gate

Both candidates used Task-1 seed 42, v2 S2, initialization SHA-256 `1a4ff6895aa40b51149882142047dd5349da1b44296bb91cafdd70546e09458f`, scribble SHA-256 `6fda328cc736582d1f9c74e0ccc33e2da755d487431ec3aee3e9db402ced3a1f`, level A, 20 full epochs and validation only.

| Candidate | Epochs 15--19 mean | Std | Finite | All classes non-empty |
|---|---:|---:|---|---|
| Adam, lr 1e-4, wd 1e-4 | 0.4819575305 | 0.0245904712 | yes | yes |
| plain SGD, lr 0.004 | 0.5221373958 | 0.0016851284 | yes | yes |

Frozen choice: **plain SGD, lr 0.004, no momentum, no weight decay**. It has a 0.04018 higher final-five validation mean and substantially lower variance. This choice is frozen for A--E and was made without loading the test set.
