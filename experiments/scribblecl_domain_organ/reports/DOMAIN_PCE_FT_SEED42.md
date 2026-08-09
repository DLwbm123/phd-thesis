# Domain PCE-FT seed-42 result

Run: `domain_pce_ft_seed42_20260809T082951Z`

Status: complete. This single method does not constitute the full Domain
seed-42 gate; PCE-EWC and RMA references are still running/pending.

| After stage | A | B | C | D | E | F |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.488680 | 0.522295 | 0.503328 | 0.476820 | 0.479050 | 0.484015 |
| 2 | 0.472287 | 0.539035 | 0.542974 | 0.476216 | 0.493092 | 0.475587 |
| 3 | 0.430966 | 0.494251 | 0.525723 | 0.463676 | 0.516007 | 0.441163 |
| 4 | 0.448571 | 0.436454 | 0.516448 | 0.484742 | 0.554164 | 0.447558 |
| 5 | 0.406596 | 0.445199 | 0.516349 | 0.490721 | 0.574600 | 0.452473 |
| 6 | 0.496370 | 0.548689 | 0.598462 | 0.551903 | 0.511083 | 0.580850 |

| Metric | Value |
|---|---:|
| A-Dice | 0.547893 |
| BWTR | 0.040004 |
| E-FWT | 0.448459 |
| mean current-domain Dice | 0.532271 |
| final old-domain mean | 0.541302 |
| RMA | pending independent PCE references |

The run used the shared binary head and evaluated all six domains after every
stage. Test data were used only for fixed-stage evaluation, never for
checkpoint selection or hyperparameter tuning. Provenance was backfilled after
normal completion with six HDF5 split hashes, six canonical S2 scribble hashes,
the order checksum and the original loaded source-tree hash.
