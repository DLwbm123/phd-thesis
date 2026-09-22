# Overleaf 编译说明

1. 编译器选择 **XeLaTeX**。
2. 主文件设置为 `main.tex`。
3. 本工程优先使用原项目 `FontStyle/` 中的字体；该目录不存在时，`FDSDSthesis.cls` 会自动回退到 Overleaf/TeX Live 自带的 Fandol 字体。
4. 三张新增图采用 EPS 文本格式，XeLaTeX 可直接处理，不需要额外转换脚本。
5. 建议首次上传后执行“从头重新编译”，以重建目录、图表目录、交叉引用和参考文献。
