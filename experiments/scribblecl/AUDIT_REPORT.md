# Source audit

The local paper fact sources are `sources/benchmark/Benchmark_pa/` (main.tex
SHA256 `b88ae877066b6e826f968a2239c9047d56c32e33bacfe94ffa2c3b10c2b8a1ee`)
and `sources/zscribble/Zscribble_MEDIA_arxiv/` (main_clean_new.tex SHA256
`a0774d17703e81ecb8c090c80f46eefdec9ba8941df80d2ca777f4fb11791976`).
They are paper sources, not executable trees, and were not modified.

Executable Benchmark code/data are `/remote-home/wangbomin/CL_Benchmark/code/CL_Benchmark`
and `/remote-home/wangbomin/CL_Benchmark/data/MMWHS`. `seq_mmwhs.py` maps
`myo_lv_la.h5`, `ra_rv.h5`, `ao_pa.h5` to global classes 1--3, 4--5, 6--7,
and uses an eight-channel head. Its `/data4/...` root is stale; the new
adapter is necessary. Each stage has 1500 training and 200 validation slices.

ZS executable source is `/root/ZScribble/ZScribbleSeg_MSCMR`. It implements
sparse supervision, augmentation, consistency, mixture-ratio/spatial-prior
and shape components but fixes class/task/device metadata. Only dynamic,
current-task-safe components are ported. Original ZS is not a CL method.

Fingerprints: Benchmark `seq_mmwhs.py` is
`2a9f74298cdc1b8ad451b24718bb63c4c533eb3b70deb206f89b33fa62058b2a` and
`models/mib.py` is `76e4901aeeca74132184554eafffdb40c2a6910bb341f3a9d22665cbbe7201c3`.
ZS `main.py` is `598f3be4bda82107917c6de7f44c38fe07abc97ac9cb736965bd888e52908df5`.
