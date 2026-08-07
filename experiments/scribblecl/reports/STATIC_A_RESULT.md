# Static Task-1 level A result

Run: `static_A_sgd_seed42`, source commit `951b182`, Task-1 seed 42, v2 S2, plain SGD lr 0.004, 150 full epochs, validation only. Manifest completed normally with no resume and no test-set access.

| Checkpoint | Epoch | Benchmark mean (BG+MYO+LV+LA) | MYO | LV | LA | Foreground-class mean | BG prediction fraction | FG prediction fraction |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `best_val.pt` | 56 | 0.549196 | 0.253517 | 0.457623 | 0.546393 | 0.419177 | 0.854312 | 0.145688 |
| `last.pt` | 149 | 0.526362 | 0.240803 | 0.446473 | 0.487353 | 0.391543 | 0.837737 | 0.162263 |

Checkpoint SHA-256 values are `d036a26509a307c6f832c0b066b264cf6c840fa663c8e609ca14e1ae57f95289` (best) and `e7dad4255c512822a7451dec9a28f70f96ece18b5096f886a73530679d5ddfc5` (last). Both store best epoch 56 and best value 0.5491962131.

Epochs 130--149 have mean 0.5348086621, std 0.0051567419, median 0.5354081220, min 0.5263615900, max 0.5462748085, range 0.0199132186 and linear slope +0.00043919 per epoch. Mean BG prediction fraction is 0.842011 (std 0.003736); foreground fraction is 0.157989. MYO and LA non-empty rates are 1.0 throughout; LV has minimum 0.995 and mean 0.9995.

The best point is higher than its epoch 54--58 neighborhood mean (0.529704), so both best and last/stability statistics must be reported. It is not used as evidence that the curve is uniformly at the peak.
