# 原始材料映射

| 材料 | 已核实工程根目录 | 主 TeX / 参考文献 | 用途 | 内容写作权限 |
|---|---|---|---|---|
| 参考毕业论文 | `sources/reference_thesis/Thesis reference/` | `main.tex`；`main.bib`、`strings.bib` | 模板核对、文本重合审查 | 禁止作为正文来源；主文件、文献库和章节均不得导入 |
| ZScribbleSeg | `sources/zscribble/Zscribble_MEDIA_arxiv/` | `main_clean_new.tex`；`cas-refs.bib` | 第三章事实、公式、实验、图和原始引用；第一章弱监督问题背景 | 允许，需证据定位 |
| Benchmark | `sources/benchmark/Benchmark_pa/` | `main.tex`；文献表内嵌于该文件第 1073 行起的 `thebibliography` 环境 | 第四章场景、指标、实验与讨论；第一章持续学习问题背景 | 允许，需证据定位 |
| SAMCL | `sources/samcl/MICCAI 2024: Toward Universal Medical Image Registration/` | `Paper-0150.tex`；`Paper-0150.bib` | 第五章方法与实验；第一章持续配准问题背景 | 允许，需证据定位 |
| FedSubMerge | `sources/fedsubmerge/ Subspace Merging for Replay-Free Federated Continual Medical Image Classification 720/` | `FedSubMerge_main_no_appendix.tex`；`references.bib` | 第六章方法与实验；第一章联邦持续学习问题背景 | 允许，需证据定位 |

## 原始工程构建入口核验

- ZScribbleSeg：主文件声明 `elsarticle` 与 `\bibliography{cas-refs}`；对应流程为 `pdflatex main_clean_new.tex`、`bibtex main_clean_new`、再运行两次 `pdflatex`。
- Benchmark：主文件使用本地 `IEEEtran.cls`，参考文献已内嵌；对应流程为至少运行两次 `pdflatex main.tex`。
- SAMCL：主文件使用本地 `llncs.cls`，并声明 `\bibliography{Paper-0150}`；对应流程为 `pdflatex Paper-0150.tex`、`bibtex Paper-0150`、再运行两次 `pdflatex`。
- FedSubMerge：主文件使用本地 `ieeecolor.cls`，并声明 `\bibliography{references}`；对应流程为 `pdflatex FedSubMerge_main_no_appendix.tex`、`bibtex FedSubMerge_main_no_appendix`、再运行两次 `pdflatex`。
- 上述命令依据实际入口和参考文献声明核对，但本轮未编译原始工程，也未修改 `sources/`。本机现已具备 `pdflatex` 和 `bibtex`；这些命令可在后续需要时执行。
- FedSubMerge 同目录另有 `FedSubMerge_main_no_appendix_tense_checked.tex`；它请求当前不存在的 `Figs/fig0_method_overview_1.pdf`，因此本轮将资源匹配的 `FedSubMerge_main_no_appendix.tex` 记为主入口。
- 当前论文根目录及四项用户工作均不是 Git 工作区。参考毕业论文子目录是独立 Git 工作区，核实分支为 `main`、提交为 `a315ed5`；该信息只用于来源状态记录。

## 使用规则

1. 原始论文是事实源，不是可直接粘贴的博士论文正文；
2. 英文论文内容必须按中文博士论文论证重新组织，不逐句翻译；
3. 第一章研究现状中新增的外部文献必须核实原始论文元数据和具体结论；
4. 参考毕业论文正文不得被 GPT 或 Codex 用作语言示例；
5. 图可复用时必须确认来源和版权，并重写中文图注；参考毕业论文的图不得复用。
