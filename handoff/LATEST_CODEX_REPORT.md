# Codex 最新报告

- 执行任务：CODEX_TASK_ch01_1_3_4.md
- 执行时间：2026-07-30 CST
- 流程：Mode A 快速小节集成；一次完整构建与差异范围审查，不运行章节里程碑审查、全 PDF 巡检或上下文包重建。
- 基线：`e3bfe11bb64e7c7d0fbe302815c1a8440bf2da20`；预检时 `main` 与 `origin/main` 同步，工作区仅有允许的未跟踪任务文件。

## 本轮内容

- 修改：`CODEX_TASK_ch01_1_3_4.md`、`chapters/ch01_introduction.tex`、`evidence/claims.csv`、`qa/terminology.csv`、`qa/chapter_status.csv`、`STATE.md`、本报告。
- 批准的 1.3.4 正文已逐字插入既有标题和 `subsec:intro-challenge-fedsubmerge` 标签之后；1.3.1--1.3.3 保持不变，1.4 和 1.5 保持为空，未起草 1.4。
- 复用既有 BibTeX 条目 `yang2024fclsurvey`、`yoon2021fedweit`、`dong2022glfc`、`saha2021gpm`、`rieke2020future`；未修改文献库或构建开关。key、DOI 与归一化题名无重复。
- 新增证据 `C1-099`--`C1-107`，新增术语 7 项：本地历史知识保护、跨客户端历史知识、全局保护子空间、过度约束、逐层相关性、子空间距离、紧凑梯度摘要。1.3 与 1.3.1--1.3.4 均为 `drafted_and_verified`；1.4 为 `queued`。

## 验证与边界

- 命令 `bash scripts/verify_fast_section.sh --quiet chapters/ch01_introduction.tex` 成功，完成一次 XeLaTeX/BibTeX 构建与差异范围作者表达、参考论文重合检查；`main.pdf` 为 53 页、663,071 字节，SHA-256 为 `4a8df965f5eedea7599bf9f88f469ebfe50be91ea795696d25b3354e477f700b`。
- 45 个活动引文及五个本节引文均在 `.bbl` 解析；无未定义引文/交叉引用、重复标签、缺失文件、TODO/TBD/??、BibTeX key/DOI/归一化题名重复或 CSV 架构错误。`git diff --check` 通过。
- 差异范围作者表达与参考论文重合检查均无命中。纯文本小节按 Mode A 不做例行人工 PDF 巡检；日志仅有此前已有的 106.4171 pt `Overfull \vbox`，没有本节引入的新布局警告。
- 正文将 Yang 等的时间/空间遗忘概括明确归因，本文采用“跨客户端全局灾难性遗忘”；无回放仅指后续训练不调用历史原始样本，未将其扩展为医院删除义务或禁止紧凑统计。
- 未将联邦学习或压缩子空间表述为形式化隐私保证，也未披露 FedSubMerge 实现、公式、实验结果或贡献列表。
- `sources/` 开始与结束均为 243 个文件、指纹 `cfb7d9ae63df5465365eceb494bd4258041636c4a83574197de8c470dc0d0058`，未修改，也未导入参考毕业论文内容。
- 保留既有非致命警告：`gbt7714-numerical` 样式名弃用、`ctexpatch` 兼容性警告、`wang2026benchmark` 的 `empty urldate` 及其他章节的 106.4171 pt `Overfull \vbox`。本任务不迁移样式或改写既有批准稿。

第一章的 1.3 已完成当前草稿阶段；下一目标为 1.4“本文主要研究内容与创新点”，本轮不写入 1.4 或 1.5。
