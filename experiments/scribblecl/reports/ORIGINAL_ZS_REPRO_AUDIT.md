# Original ZScribbleSeg reproduction audit

Date: 2026-08-06. Host: `root@10.12.208.231:20048`. Source checkout and data were treated as read-only.

The original `main.py --eval` route was not used because it deletes and rewrites `/root/ZScribble/data/MSCMR_scribble_v2/predicts/`. Instead, the audit instantiated the original `build_model`, `data.mscmr.build("val")`, `inference.evaluate`, collate function and sequential sampler in an in-memory script. TensorBoard writing was replaced with a no-op writer.

Evaluated checkpoint:

- path: `/root/ZScribble/ZScribbleSeg_MSCMR/outputs/best_checkpoint.pth`
- SHA-256 prefix: `492592f8924c87af`
- saved epoch: 706
- checkpoint provenance: seed 42; Adam; lr `1e-4`; weight decay `1e-4`; batch size 4; `lambda2=0.1`; nominal 1000 epochs; resumed from root `best_checkpoint.pth` at epoch 537
- runtime: PyTorch 2.6.0+cu124, GPU 1; original validation set, 58 batches

| Metric | Reproduced value |
|---|---:|
| Rv Dice | 0.6432909711 |
| Lv Dice | 0.8724234104 |
| Myo Dice | 0.7865928422 |
| Avg Dice | 0.7674357706 |
| sparse CE | 0.0569637127 |

This value is not replaced by the filename `0.8117high_checkpoint.pth` and is not the maximum line in a training log. The `outputs/log.txt` historical maximum is Avg 0.7982517387 at epoch 541; the evaluated checkpoint is epoch 706. Those are distinct evidence records.

The root `0.8117high_checkpoint.pth` was also evaluated under the identical protocol to avoid checkpoint selection. Its SHA-256 prefix is `24a555c5428aec5f`, saved epoch is 468, and reproduced metrics are Rv 0.6598258630, Lv 0.8691124335, Myo 0.7871000993, Avg 0.7720128123, sparse CE 0.0485785267. Thus the filename value `0.8117` is not reproduced by the current checkout/data/evaluator and must not be reported as a verified metric.

The checkpoints form a continuation chain rather than independent clean runs. This must be preserved when interpreting the original implementation and when choosing the clean MMWHS static protocol.
