# 原图内嵌医学示例

`example-000.png` 至 `example-003.png` 由本目录上级既有的 `medical_mllm_continual_learning.pdf` 使用 `pdfimages -png` 直接提取，按原对象顺序对应超声影像、胸部 X 线、消化内镜和皮肤镜示例。它们仅复用原论文图件中的示意缩略图，不是新增实验数据，未做图像生成、重采样或病灶修改。原图 PDF 与 PNG 保留供追溯。

文字、图块和连线由 `../medical_mllm_continual_learning.tex` 绘制；三层研究路线由 `../future_three_level_roadmap.tex` 绘制。修改这些 TikZ 源文件后，在论文根目录执行 `latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error main.tex`，检查图 7.1 和图 7.2 所在页即可。
