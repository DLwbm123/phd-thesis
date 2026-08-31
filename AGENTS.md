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

2026-08-31 按作者提供的最新 ZIP 同步正文、章节顺序和图件；本轮不再自由改写正文或重新绘图。科学边界和发布规则不变。

```text
第一章 绪论
第二章 医学影像深度学习相关理论与关键技术
第三章 持续医学图像分割的场景定义与综合评测研究
第四章 无回放条件下的联邦医学影像持续分类与工程实现研究
第五章 有限回放条件下的医学影像持续分割与配准研究
第六章 总结与展望
```

导师讨论稿中“第五章之后直接进入第七章”属于编号缺口。除非作者提供一个新的实质性第六章，Codex 必须保持连续六章，不得创建空章。

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
8. 完整编译并检查目录是否为连续六章；
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
- 框架迁移优先在独立分支完成，作者审阅第一章和目录后再合并到 `main`；
- `sources/`、构建产物、缓存和导出包不上传；
- Overleaf 只用于查看编译结果，不作为正文修改源；
- 修改任何 Overleaf 编译输入后，必须先完成本地编译与审查，再推送 GitHub，最后运行同步脚本；
- GitHub 与 Overleaf 均禁止强制推送；发生并发更新时先核对差异。

# Definition of done

- 目录与正文均为连续六章，或存在作者明确批准的实质性第六章；
- 第一章与新主线一致，不再出现“第三章不是持续学习、第四至第六章构成持续学习主线”等旧版硬性定位；
- 原始 ZScribbleSeg 与新增 ScribbleCL 扩展的证据边界清楚；
- 全文编译成功，或明确区分既有错误和本次新增错误；
- 没有新增 undefined citation/reference、重复 label、缺失文件或错误章节引用；
- 新事实有来源，新数字与原始结果一致；
- Git diff 不含无关修改；
- `handoff/LATEST_CODEX_REPORT.md` 已更新，并列出尚未完成的 ScribbleCL 实验。
