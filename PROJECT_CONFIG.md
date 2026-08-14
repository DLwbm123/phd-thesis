# 项目配置

- Repository root: `.`
- Main LaTeX entry: `main.tex`
- Thesis class/template: `FDSDSthesis` v1.1（用户提供；模板实现与复旦标识资源随工程保留，CJK 字体由 TeX Live/ctex 提供）
- Chapter directory: `chapters/`
- Bibliography file: `bibliography/references.bib`
- Figure directory: `figures/`
- Bibliography backend: `bibtex`
- Full build command: `latexmk -xelatex -interaction=nonstopmode -file-line-error main.tex`
- Fast build command: `xelatex -interaction=nonstopmode -file-line-error main.tex`
- Fast section verification: `bash scripts/verify_fast_section.sh chapters/chXX_name.tex`（一次完整构建、差异范围审查与元数据检查；完整流程见 `WORKFLOW_MODES.md`）
- Clean command: `latexmk -C main.tex`
- Git repository: 是；GitHub 私有仓库 `https://github.com/DLwbm123/phd-thesis`
- Git default branch: `main`
- GitHub remote: `origin` → `https://github.com/DLwbm123/phd-thesis.git`
- Overleaf remote: `overleaf` → `https://git@git.overleaf.com/6a69ac75d6170c19b9e2711a`
- Overleaf project: `https://www.overleaf.com/project/6a69ac75d6170c19b9e2711a`（只用于查看）
- Overleaf sync command: `bash scripts/sync_latex_to_overleaf.sh`
- Local TeX toolchain: TeX Live 2026（用户级安装于 `~/Library/TinyTeX`；`~/.zprofile` 已加入 `bin/universal-darwin`）
- Tool versions: `latexmk 4.88`、`XeTeX 0.999998`、`BibTeX 0.99e`
- TeX package repository: `https://mirrors.ustc.edu.cn/CTAN/systems/texlive/tlnet`
- Full build verification: 2026-08-14 已在 FDSDSthesis v1.1 模板下完成 XeLaTeX/BibTeX 构建，生成 163 页 `main.pdf`。

## Remote sync policy

- GitHub 保存完整写作工程，包括契约、提示词、章节卡、handoff、证据、QA、脚本和 LaTeX 源文件。
- 本地只读 `sources/`、LaTeX 构建产物、缓存和导出压缩包不上传 GitHub。
- Overleaf 只接收完整编译所需的 LaTeX 子集。每次 LaTeX 内容更新并通过本地编译与审查后，先推送 GitHub，再运行同步脚本。
- Overleaf 不是正文修改源；不得通过强制推送覆盖并发更新。

## Source paths

- Reference thesis root: `sources/reference_thesis/Thesis reference/`（仅模板核对与文本重合审查；禁止作为内容源）
- ZScribbleSeg root: `sources/zscribble/Zscribble_MEDIA_arxiv/`
- Benchmark root: `sources/benchmark/Benchmark_pa/`
- SAMCL root: `sources/samcl/MICCAI 2024: Toward Universal Medical Image Registration/`
- FedSubMerge root: `sources/fedsubmerge/ Subspace Merging for Replay-Free Federated Continual Medical Image Classification 720/`（目录名在斜杠后含一个前导空格）

## Initialization note

以上路径、Git 状态、远端同步策略和工具链状态已于 2026-07-29 通过本地检查与实际编译核对。原始工程的入口文件与参考文献位置见 `SOURCE_MAP.md`。
