# Class continual protocol

The fixed order is T1 MYO/LV/LA, T2 RA/RV, and T3 AO/PA. A shared background head is concatenated before class blocks of sizes 3, 2 and 2. Only blocks up to the active stage are called. The final semantic order is BG, MYO, LV, LA, RA, RV, AO, PA.

The 3x3 patient-level foreground Dice matrix yields A-Dice, relative BWTR and RMA. WCD is the final seven-class patient-level Dice on the immutable `whole_heart_test.h5` cohort; it is evaluation-only. Stage 2 must pass the current-learning gate before stage 3.
