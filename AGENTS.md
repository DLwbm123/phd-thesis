# Repository mission

本仓库用于撰写中文博士学位论文。Codex Sol High 的主要职责是本地材料检索、框架迁移、上下文准备、LaTeX 集成、引用与数字核验、编译和质量审查。正式学术正文原则上由 GPT Pro 生成并经作者批准后写入。

# Source-of-truth hierarchy

1. `THESIS_CONTRACT.md`：导师讨论后确认的全文主题、章节逻辑、工作定位和禁止越界事项；
2. `AUTHORSHIP_PROTOCOL.md` 与 `AUTHOR_VOICE.md`：作者表达和原创论证要求；
3. `chapter_cards/chXX.md`：各章科学问题、结构、证据边界和完成标准；
4. `sources/benchmark`、`sources/fedsubmerge`、`sources/zscribble`、`sources/samcl`：四项工作的事实源；
5. 新增 ScribbleCL 实验的实际代码、日志、表格和 `evidence/*.csv`；
6. `qa/terminology.csv` 与 `qa/notation.csv`：术语和符号；
7. 经 GPT Pro 与作者批准并嵌入任务的正文草稿。

`sources/reference_thesis/` 不是内容源，只能用于模板核对和文本重合审查。

# Current dissertation architecture

2026-09-04 作者确认发布三份 GPT Pro 修改稿的融合版本。当前正文来自 `Final_thesis/PhD_Thesis_Integrated_20260903`；后续修改以该版本、作者新指示和可核验证据为准，不补写实验结果。

```text
第一章 绪论
第二章 医学影像深度学习相关理论与关键技术
第三章 医学影像持续学习平台设计与分割基准评测
第四章 基于监督增强与特征一致性约束的弱监督医学影像持续分割研究
第五章 基于子空间聚合的无回放联邦医学影像持续分类研究
第六章 基于锐度感知元经验回放的医学影像持续配准研究
第七章 总结与展望
```

七章均有实质正文。第三章平台定位为评测平台设计：用户在本地训练，只提交模型或预测，不要求训练记录；平台尚未实际实现时不得写成已部署系统。历史章节号和旧版专项检查不能用于回退当前稿件。

# Non-negotiable rules

- 不得创造引用、数据集设定、公式、实验结果、统计显著性或结论；
- 不得在没有原始表格、日志或 `evidence/experiments.csv` 支持时修改任何数字；
- 不得声称原始 ZScribbleSeg 论文已经提出持续学习方法；
- 允许把 ZScribbleSeg 作为第五章 ScribbleCL 扩展的弱监督方法基础，但所有持续学习任务、基线、指标和结果必须有新增实验记录；
- 若 ScribbleCL 只有新实验而无新优化机制，不得把它写成新算法；
- 不得把 Benchmark 写成普通综述或单一算法；
- 不得声称 FedSubMerge 提供形式化隐私保证；
- 不得把 SAMCL 的有限回放写成无回放；
- 不得复制、翻译或近义改写参考毕业论文的句段；
- 不得把“降低 AI 检测分数”作为重写目标，不得随机改写、制造语病或无意义替换同义词；
- `sources/` 只读；
- 未经明确授权，不得由 Codex 自由重写已批准的学术正文；
- 框架迁移可以调整标题、顺序、过渡、章节引用和与新主线冲突的论断，但必须保留可核验事实和引用；
- 遇到证据缺失时写入 `TODO-EVIDENCE` 或 `TODO-EXPERIMENT` 并报告，禁止猜测；
- 所有新符号首次出现时定义并登记；
- 参考模板的类文件和资源可以保留，参考论文的正文、图表、元数据和文献库不得导入。

# Framework migration workflow

在 2026-07-31 导师框架迁移完成前，暂停继续撰写 2.1.2 及后续正文。迁移任务至少应：

1. 检查 `git status`、当前分支、未提交修改和远端差异；不得丢弃本地工作；
2. 建立迁移分支或可恢复的备份提交；
3. 重读本文件、`THESIS_CONTRACT.md`、作者协议、作者声音和全部章节卡；
4. 更新 `main.tex`、章节文件、章节卡、提示词、状态文件和来源映射；
5. 按映射重构第一章，保留有效文献综述，重写与旧章节定位冲突的论断；
6. 保留已完成的 2.1.1，只迁移第二章标题和后续骨架；
7. remap `evidence/claims.csv`、`qa/chapter_status.csv`、术语、标签和交叉引用；
8. 完整编译并检查目录是否与作者当前七章稿一致；
9. 运行风格、参考文本重合、未定义引用、重复标签、TODO 和遗留旧章节表述审查；
10. 更新 `STATE.md`、`handoff/LATEST_CODEX_REPORT.md` 和下一轮 GPT 上下文包。

# Required routine workflow after migration

按 `WORKFLOW_MODES.md` 选择流程。每轮至少应：

1. 阅读当前状态、相关章节卡和任务；契约或章节结构变化后必须重新读取全部总约束；
2. 检查任务范围、工作区、分支和远端同步状态；
3. 只修改目标章节、必要引用库、证据表、状态文件和工程文件；
4. 完整编译一次，并检查未定义引用、重复标签、缺失图片、TODO/TBD/?? 与本轮新增警告；
5. 快速模式运行 `scripts/verify_fast_section.sh --quiet`，章节里程碑运行完整风格和参考论文重合审查；
6. 更新 `STATE.md`、`qa/chapter_status.csv` 和 handoff 报告；
7. 报告修改文件、编译结果、证据问题和下一步。

# Remote synchronization policy

- GitHub 私有仓库 `DLwbm123/phd-thesis` 是版本源；
- 融合稿发布到专用论文分支 `agent/predefense-writing-20260830`；未经作者明确要求不合并 `main`；
- `sources/`、构建产物、缓存和导出包不上传；
- Overleaf 只用于查看编译结果，不作为正文修改源；
- 修改任何 Overleaf 编译输入后，必须先完成本地编译与审查，再推送 GitHub，最后运行同步脚本；
- GitHub 与 Overleaf 均禁止强制推送；发生并发更新时先核对差异。

# Definition of done

- 目录与正文均为当前融合稿七章结构；
- 第一章与“平台设计及分割基准—域增量弱监督分割—类别增量联邦分类—任务增量配准”主线一致；
- 原始 ZScribbleSeg 与新增 ScribbleCL 扩展的证据边界清楚；
- 全文编译成功，或明确区分既有错误和本次新增错误；
- 没有新增 undefined citation/reference、重复 label、缺失文件或错误章节引用；
- 新事实有来源，新数字与原始结果一致；
- Git diff 不含无关修改；
- `handoff/LATEST_CODEX_REPORT.md` 已更新，并列出尚未完成的 ScribbleCL 实验。
