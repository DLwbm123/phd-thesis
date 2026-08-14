# 启动包烟雾测试

- 干净模板：FDSDSthesis v1.1 使用 XeLaTeX + BibTeX 编译成功；
- 六章与附录 A：全部可被 `main.tex` 正确包含；
- 字体设置：使用 ctex/TeX Live 提供的 CJK 字体，不随工程分发字体文件；
- 参考文献：`bibliography/references.bib` 由 `plainurl` BibTeX 样式输出；
- Python QA 脚本：语法检查通过；
- 作者表达基线：空章节未命中预设套话规则；
- 文本重合基线：打包时使用用户提供的参考论文源码测试，未发现达到 28 个归一化字符的长文本精确重合。

本报告只是工程烟雾测试。写入真实正文后必须重新运行 `make qa`。
