# MMWHS sparse-label protocol v2

Formal labels are `0=annotated background`, `1..7=annotated current foreground`, and `-100=unknown`. The generator accepts only the current-stage local H5 label map. Consequently no global future-class identity is available to its API.

Foreground strokes are class skeletons clipped to the same local class. Background candidates are `local==0` pixels at least five pixels from current foreground; deterministic short border and interior strokes are selected. The background rule is identical for FG widths 1, 3 and 5. All remaining pixels stay unknown. Dense local background is never used as supervision.

On the three train H5 files, each with 1500 slices, all nine stage/width combinations have zero unsupervised slices. Background supervision is exactly 168000 pixels per combination and therefore independent of FG width. The complete counts, coverage, zero-FG counts and per-slice extrema are in `results/background_scribble_audit.csv`.

The isolated server test suite passed 12 tests. It verifies deterministic output, actual BG/FG/unknown labels, no BG/FG overlap, positive-slice FG supervision, zero-FG background supervision, count conservation, unknown preservation, and that unavailable identities cannot enter generation.

These statistics validate label semantics only. They do not select S1/S2/S3 and contain no validation or test performance.
