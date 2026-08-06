# MMWHS Task-1 label mapping audit

Commit audited: `dcf4aa68993e4915381a96bbac173dea4c9e0409`.  This audit uses no test labels for model selection.

## Decision

The Task-1 mapping is confirmed as `ID 1 = MYO`, `ID 2 = LV`, and `ID 3 = LA`.

## Independent evidence chain

1. Benchmark's read-only `datasets/seq_mmwhs.py` selects `myo_lv_la.h5` for Task 1 and maps its local foreground labels 1--3 into the global class space without reordering.  The executable HDF5 has no semantic attributes, so this fact alone does not prove the local-name order.
2. The official [MM-WHS data description](https://zmiclab.github.io/zxh/0/mmwhs/data.html) defines the seven manually segmented structures and distinguishes LV blood cavity, LA blood cavity, and LV myocardium.  The project chapter's Benchmark task description independently states the Task-1 semantic set as LV/LA/MYO.
3. The HDF5 filename orders the three Task-1 local structures as `myo_lv_la`; together with the unchanged local IDs, this yields `1/2/3 = MYO/LV/LA`.
4. The three validation-GT visual audits in `results/figures/label_semantics_audit/` are anatomically consistent: ID 1 is the annular myocardium surrounding a cavity, ID 2 is the LV cavity, and ID 3 is the LA cavity.  Each image contains three maximum-area validation slices and was generated from the validation HDF5 only.

The mapping is frozen for subsequent ScribbleCL work.  No class name is inferred from model prediction or test data.
