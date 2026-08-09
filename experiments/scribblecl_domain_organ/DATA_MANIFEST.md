# Executable data manifest

Read-only root: `/remote-home/wangbomin/CL_Benchmark/data` on
`root@10.12.208.231:20048`. The executable source hard-codes a stale
`/data4/zhouhangqi/CL_Benchmark_data` root; no such directory exists on the
audited host, so this workspace takes the root explicitly without changing any
split.

| Scenario | Task | HDF5 | train/val/test slices | train/val/test cases |
|---|---|---|---:|---:|
| Domain | A | BIDMC.h5 | 301/94/126 | 7/2/3 |
| Domain | B | HK.h5 | 168/48/72 | 7/2/3 |
| Domain | C | ISBI.h5 | 345/75/158 | 18/4/8 |
| Domain | D | UCL.h5 | 166/52/100 | 7/2/4 |
| Domain | E | ISBI_1.5.h5 | 582/130/254 | 18/4/8 |
| Domain | F | I2CVB.h5 | 704/192/320 | 11/3/5 |
| Organ | T1 | UtahI.h5 | 762/153/298 | 25/5/10 |
| Organ | T2 | UCL.h5 | 166/52/100 | 7/2/4 |
| Organ | T3 | Lits.h5 | 1421/343/496 | 17/4/7 |
| Organ | T4 | brain.h5 | 1963/894/1223 | 50/20/30 |

`patient_info_{split}` stores inclusive final-slice indices. These arrays are
used directly for patient-volume Dice. The FeTS training boundary array has
repeated ends for cases with no retained slice; training is slice-based and no
new split is inferred.

Full-file SHA-256 values are frozen in `scribblecl_do/data/protocols.py`.
Notably, Domain D and Organ T2 are the same byte-identical PROMISE12 HDF5
(`76ef6354...`).

The paper states a nominal 60/15/25 case split, but the executable HDF5 case
counts do not always equal those percentages (FeTS is 50/20/30). The HDF5
arrays, not the nominal percentages, are the executable split fact source.
