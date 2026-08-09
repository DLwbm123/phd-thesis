# Method protocol

- Backbone: one dynamic U-Net implementation for every scenario and method. Training APIs return logits; Softmax is evaluation-only.
- Sparse PCE: labels are explicit background `0`, current foreground `1..C`, and unknown `-100`.
- EWC: online Fisher uses `model.eval()`, the current task's training sparse-PCE loader, known pixels only, no augmentation, no dense target, and no auxiliary loss. Lambda is 1 and gamma is 0.1.
- SI: `c=5`, `xi=1`; its parameter scope is identical to EWC.
- Class scope: backbone, shared background head and previously activated class blocks. A newly activated block is absent from the old penalty.
- Domain scope: backbone and the shared binary head.
- Organ scope: backbone only; old binary heads are frozen.
- Replay, historical images and test-set hyperparameter selection are prohibited. Enhanced methods remain blocked.
