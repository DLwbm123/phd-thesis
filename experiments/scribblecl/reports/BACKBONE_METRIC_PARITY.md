# Backbone, preprocessing and metric parity

The hand-written `ResUNet32` is numerically equivalent to Benchmark `resunet32('mid')` after replacing its head with 8 channels. Both have 2,916,000 parameters in 47 tensors with identical shape order. Copying parameters by order and evaluating the same `(2,1,256,256)` input produced maximum and mean absolute output differences of 0.

Preprocessing was not equivalent: Benchmark reads the H5 slice, resizes it to 256 and performs no intensity normalization; ScribbleCL added per-slice z-score normalization. Since the H5 arrays are already 256x256, formal ScribbleCL now returns the raw float slice.

Optimization was not equivalent: Benchmark uses plain SGD at lr 0.008, no momentum, StepLR at epoch 80 with factor 0.5. The archived ScribbleCL runner used momentum 0.9. The ZS source instead uses Adam at lr 1e-4 and weight decay 1e-4. A formal A-E comparison must choose one optimizer once and hold it constant; results produced under different optimizers are confounded.

Metric aggregation was not equivalent. Benchmark groups validation slices into patient volumes using `patient_info_val=[99,199]`, computes Dice for background and current classes with epsilon `1e-5`, then averages classes and patients. ScribbleCL averaged per-slice foreground-only Dice. The formal evaluator now uses patient-volume aggregation and includes background for the Benchmark main metric; foreground per-class Dice remains separately logged.

Status: backbone parity passes; formal preprocessing and metric code are aligned and covered by tests. Archived results are not retroactively relabeled.
