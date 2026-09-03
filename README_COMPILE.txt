编译方式
========

本项目使用用户提供的 FDSDSthesis v1.1 模板。推荐在完整 TeX Live 环境中使用 XeLaTeX：

    latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex

也可运行：

    make thesis

主文件：main.tex
参考文献：bibliography/references.bib
