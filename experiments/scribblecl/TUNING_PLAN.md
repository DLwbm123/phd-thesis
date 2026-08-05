# One bounded pilot adjustment

The initial PCE Task-1 seed-42 run at `lr=0.008` became non-finite at epochs
148--149 and is invalid for branching. One validation-only stability adjustment
is authorised: rerun the PCE family at `lr=0.004`, freeze it for all its seeds,
and do not use a test metric to select it. ZS remains at 0.008.
