# Domain continual protocol

The fixed order is A BIDMC, B HK, C ISBI, D UCL, E ISBI 1.5 and F I2CVB. All centers share a U-Net backbone and one two-channel background/prostate head; domain identity is never an input.

Evaluation stores a full 6x6 patient-level foreground Dice matrix, including future-center cells for E-FWT. Summary fields are A-Dice, relative BWTR, RMA, E-FWT, current-center Dice and final old-center mean.
