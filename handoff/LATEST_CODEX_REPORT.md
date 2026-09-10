# 作者最新项目 ZIP 发布记录（2026-09-10）

来源：作者上传 `PhD_Thesis_updated.zip`。基线 GitHub `09f9094`，Overleaf `d97a21e`。

导入包内 69 份项目源码与资源，Git 中实际更新 21 份已有项目文件、新增 3 份表格源；其余源码和资源未产生内容变更。附带的 `main.pdf` 与 `MANIFEST.sha256` 留在本地解包目录，不作为 GitHub/Overleaf 编译输入上传。保留现有仓库的实验代码和管理文件。

本次按作者最新版本原样导入正文、数值、图源和章节卡，不沿用旧清单回退作者更改，不重算实验。

## 更新的项目文件

- `SRC/abstract_en_body.tex`
- `SRC/abstract_zh_body.tex`
- `chapter_cards/ch01.md`
- `chapter_cards/ch02.md`
- `chapter_cards/ch03.md`
- `chapter_cards/ch04.md`
- `chapter_cards/ch05.md`
- `chapter_cards/ch06.md`
- `chapter_cards/ch07.md`
- `chapters/ch01_introduction.tex`
- `chapters/ch02_foundations.tex`
- `chapters/ch03_medcl_benchmark.tex`
- `chapters/ch04_scribble.tex`
- `chapters/ch05_fedsubmerge.tex`
- `chapters/ch06_registration.tex`
- `chapters/ch07_conclusion.tex`
- `figures/ch01/thesis_work_logic.tex`
- `figures/ch03/medcl_platform_architecture.tex`
- `figures/ch03/medcl_workflow_design.tex`
- `figures/ch05/fedsubmerge_engineering.tex`
- `main.tex`
- `tables/FedCL.tex`（新增）
- `tables/SAMCL.tex`（新增）
- `tables/ScribbleCL.tex`（新增）

另更新 `STATE.md`、`qa/chapter_status.csv` 和本报告。

## 验证

XeLaTeX/latexmk 全文构建成功，183 页；最终日志无 LaTeX 错误、未定义引用、重复标签、缺字或 Overfull。检查了弱监督分割表、联邦分类长表与配准主表的渲染，跨页表头正常。本轮是作者项目版本同步，不是新增实验或原始结果复核。

本地重新编译文件：`../zip_update_20260910/PhD_Thesis_updated_compiled_20260910.pdf`。GitHub 与 Overleaf 均使用非强制推送，远端回执见最终回复及本地 `release_receipt.json`。
