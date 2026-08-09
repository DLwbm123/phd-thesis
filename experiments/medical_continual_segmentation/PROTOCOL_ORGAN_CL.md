# Organ continual protocol

The fixed order is T1 left atrium MRI, T2 prostate MRI, T3 liver CT and T4 brain-tumor MRI. The U-Net backbone is shared and each task has a separate two-channel head. Old heads are frozen and excluded from EWC and SI.

Evaluation stores a lower-triangular 4x4 patient-level foreground Dice matrix. Summary fields are A-Dice, relative BWTR, RMA, current-task Dice, final old-task mean and head growth. E-FWT is undefined and is not computed.
