# Codex 最新报告：第二章 2.1.1

- 执行任务：`CODEX_TASK_ch02_2_1_1.md`
- 执行时间：2026-07-30 CST
- 基线提交：`235bcfa05463f96fef8e5410a63a4b3ec12c1974`；预检时 `main` 与 `origin/main` 同步，工作区仅有允许的任务文件 `CODEX_TASK_ch02_2_1_1.md`。

## 集成范围

- 在 `chapters/ch02_foundations.tex` 中加入 2.1 标签及批准的 2.1 引言，并在 2.1.1 中加入批准的医学图像分割正文、四个显示公式和四个唯一公式标签：预测、交叉熵、区域重叠、边界距离。
- 2.1.1 正文在标签之后与任务文件批准稿逐字一致；没有写入 2.1.2 或其他第二章正文。2.1.2、2.1.3 及后续章节小节仍为空骨架。
- 第一章文件内容哈希保持不变：`chapters/ch01_introduction.tex` SHA-256 `0cbe6694a5d833ef17cf418f5790ec4cef79c5990b2c6e87dacb7d9e57662378`。
- 实际修改/新增文件：`CODEX_TASK_ch02_2_1_1.md`、`chapters/ch02_foundations.tex`、`bibliography/references.bib`、`evidence/claims.csv`、`qa/terminology.csv`、`qa/notation.csv`、`qa/chapter_status.csv`、`STATE.md`、`handoff/LATEST_CODEX_REPORT.md`。`qa/style_audit_report.md` 和 `qa/reference_overlap_report.md` 本轮未产生新差异。

## 参考文献、证据与 QA 登记

- 新增唯一 BibTeX 条目 `taha2015metrics`（DOI `10.1186/s12880-015-0068-x`）；`litjens2017survey` 和 `ronneberger2015unet` 复用既有条目。共 46 个 BibTeX key，无重复 key、DOI 或归一化题名。
- `evidence/claims.csv` 新增 `C2-001`--`C2-009`，每个恰好一次；全表保持 11 列，Python CSV 解析通过。
- `qa/terminology.csv` 新增 9 个语义分割、二值/多类分割、标签/概率图、Dice、IoU、HD95 和 ASSD 术语；保持 5 列和全局英文键唯一。
- `qa/notation.csv` 将 `theta` 首次定义更新为 2.1.1，并新增 `Omega`、`I`、`Y`、`K`、`f_theta`、`p_theta_k`、`Y_hat`、`L_CE`、`P_k`、`G_k`、`d_a_B`、`Q_q`；保持 7 列和符号唯一。
- `qa/chapter_status.csv` 更新为：`2=in_progress`、`2.1=in_progress`、`2.1.1=drafted_and_verified`、`2.1.2=queued`、`2.1.3=not_started`；第一章状态保持完成。

## 验证结果

- 命令：`bash scripts/verify_fast_section.sh --quiet chapters/ch02_foundations.tex`；退出码 0，快速元数据和完整本地构建均通过。PDF 为 59 页、725,025 字节、SHA-256 `00809254b3c157d1016a3720ab5fa679a97b91c69008f657b63e99f059ab52af`。
- 活动引文均可解析；无未定义引文、未定义交叉引用、重复标签、缺失输入、缺失类/参考文献/图表、`TODO`/`TBD`/`??` 或重复公式标签。`sources/` 未出现在 diff 中。
- 通过 `git diff --check`；保留 Chapter 2 骨架中 2.1.2、2.1.3 与后续小节的空正文。`config/build_flags.tex` 仍为 `\thesisbibliographytrue`。
- 定向视觉检查使用 macOS Quartz：实体 PDF 页 35--36（2.1 引言和 2.1.1 全部内容）以及实体参考文献页 54（条目 [46] `taha2015metrics`）。公式未发生越界或异常断行，中文、标题、页码和引用均可读，无裁切、重叠或异常分页。
- `sources/` 任务前后均为 243 个文件，确定性指纹均为 `cfb7d9ae63df5465365eceb494bd4258041636c4a83574197de8c470dc0d0058`；未修改或导入 `sources/reference_thesis/` 内容。

## 未解决事项与下一目标

- 保留既有样式弃用、`ctexpatch` 兼容性和其他章节 `Overfull \\vbox` 警告；本轮目标页面未发现版面异常。
- `evidence/claims.csv` 的既有混合行尾未规范化；不影响 Python CSV 解析。
- 下一目标为 2.1.2“医学图像配准”。本轮没有撰写 2.1.2 或任何后续第二章正文。
- GitHub 内容提交和 Overleaf 部署将在本报告提交后完成；本轮不创建仅用于部署回执的第二个 GitHub 提交。
