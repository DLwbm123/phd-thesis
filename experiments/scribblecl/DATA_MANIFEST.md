# Data and environment manifest

| Item | Verified value |
|---|---|
| MMWHS data root (not committed to config) | `/remote-home/wangbomin/CL_Benchmark/data/MMWHS` |
| HDF5 files | `myo_lv_la.h5`, `ra_rv.h5`, `ao_pa.h5`, `whole_heart_test.h5` |
| Train/validation/test slices per stage | 1500 / 200 / 900 |
| Training image shape | `256 x 256` axial slices |
| Task map | T1 local 1--3 -> global 1--3; T2 local 1--2 -> 4--5; T3 local 1--2 -> 6--7 |
| ZS data root | `/root/ZScribble/data` |
| GPU | four NVIDIA A100-PCIE-40GB cards |
| Python/PyTorch/CUDA | 3.12.7 / 2.6.0+cu124 / CUDA available |
| Benchmark split SHA | HDF5 datasets are embedded; per-file checksums are recorded by each remote run manifest before launch. |

No real absolute path is placed in tracked runnable config; use `.env.example`.
