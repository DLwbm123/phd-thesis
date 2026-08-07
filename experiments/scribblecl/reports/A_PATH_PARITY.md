# Level-A path parity across commits

Compared deployed commit `951b182` with the candidate that adds A0, A-ratio, Dense-v2 and component logging. Both used the same Task-1 S2 file, seed 42, initial model, first 10 shuffled batches, PCE and plain SGD lr 0.004.

CUDA SHA comparison is not a valid exact criterion here: repeated `951b182` runs already differ at the first backward gradient because CUDA `nll_loss2d` is nondeterministic, and PyTorch explicitly rejects it under deterministic-algorithm mode. Step-0 logits and loss were nevertheless identical before backward.

The definitive parity run used CPU deterministic algorithms on the same ten full 8x256x256 batches. All 10 steps matched exactly for:

- logits SHA-256;
- scalar loss;
- full concatenated gradient SHA-256;
- parameters before the optimizer step;
- parameters after the optimizer step.

Losses for steps 0--9 were respectively 1.3739324808, 1.2932025194, 1.2295217514, 1.1253805161, 1.0512695312, 1.0645277500, 1.0454133749, 0.9617375731, 0.9794874191 and 0.9244201183 in both versions.

Verdict: the standard A computation path is unchanged; the completed 150-epoch A run from `951b182` remains valid and does not require rerunning.
