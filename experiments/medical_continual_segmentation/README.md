# Continual medical segmentation

This anonymous runtime exposes one training entry, `main.py`, for class-, domain- and organ-incremental segmentation. Every formal method uses the same dynamic valid-convolution U-Net. The runtime contains no replay, historical-image buffer or test-set model selection.

## Setup and audit

Python 3.10+, PyTorch, h5py, NumPy, SciPy, scikit-image, PyYAML and pytest are required. The H5 root must contain `MMWHS`, `Domain_Prostate` and `Task_incre`.

```bash
python scripts/audit_data.py --scenario class --data-root /data/benchmark --output reports/class_data_audit.json
python scripts/audit_data.py --scenario domain --data-root /data/benchmark --output reports/domain_data_audit.json
python scripts/audit_data.py --scenario organ --data-root /data/benchmark --output reports/organ_data_audit.json
python scripts/generate_sparse_annotations.py --scenario class --data-root /data/benchmark --output-root /data/sparse_annotations --seed 42
```

## Required gates

```bash
python main.py --scenario class --method pce_ft --dry-run --device cuda:0
python main.py --scenario domain --method pce_ewc --dry-run --device cuda:0
python main.py --scenario organ --method pce_ft --dry-run --device cuda:0
python main.py --scenario class --method dense_ft --data-root /data/benchmark --sparse-root /data/sparse_annotations --tiny-overfit --task T1 --supervision dense
python main.py --scenario class --method pce_ft --data-root /data/benchmark --sparse-root /data/sparse_annotations --tiny-overfit --task T1 --supervision pce
```

## Seed-42 sequences

```bash
python main.py --scenario class --method pce_ft --config configs/class/pce_ft.yaml --data-root /data/benchmark --sparse-root /data/sparse_annotations --runs-root runs
python main.py --scenario domain --method pce_ft --config configs/domain/pce_ft.yaml --data-root /data/benchmark --sparse-root /data/sparse_annotations --runs-root runs
python main.py --scenario organ --method pce_ft --config configs/organ/pce_ft.yaml --data-root /data/benchmark --sparse-root /data/sparse_annotations --runs-root runs
```

Use `--stage1-parent RUN/stage_1.pt` for the paired EWC continuation. Use `--resume RUN/last.pt` after an epoch-safe stop. `enhanced_*` always raises `blocked_by_static_gate` until a separately recorded static gate passes. Seeds 43 and 44 are rejected until the seed-42 promotion is complete.
