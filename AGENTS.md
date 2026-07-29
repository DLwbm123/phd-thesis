# Repository mission

本仓库用于撰写中文博士学位论文。Codex Sol High 的主要职责是本地材料检索、上下文准备、LaTeX 集成、引用与数字核验、编译和质量审查。正式学术正文原则上由 GPT Pro 生成并经批准后写入。

# Source-of-truth hierarchy

1. `THESIS_CONTRACT.md`：全文主题、章节定位和禁止越界的总契约；
2. `AUTHORSHIP_PROTOCOL.md` 与 `AUTHOR_VOICE.md`：作者表达和原创论证要求；
3. `chapter_cards/chXX.md`：每章科学问题、结构和完成标准；
4. `sources/zscribble`、`sources/benchmark`、`sources/samcl`、`sources/fedsubmerge`：方法、公式、实验和原始引用的事实源；
5. `evidence/*.csv`：正文论断、数字、公式和局限的证据账本；
6. `qa/terminology.csv` 与 `qa/notation.csv`：术语和符号；
7. 经 GPT Pro 批准并嵌入任务的正文草稿。

`sources/reference_thesis/` 不是内容源，只能用于模板核对和文本重合审查。

# Non-negotiable rules

- 不得创造引用、数据集设定、公式、实验结果、统计显著性或结论；
- 不得在没有原始表格或 `evidence/experiments.csv` 支持时修改任何数字；
- 不得将 ZScribbleSeg 描述为持续学习、可塑性或灾难性遗忘方法；
- 不得声称 FedSubMerge 提供形式化隐私保证；
- 不得复制、翻译或近义改写参考毕业论文的句段；
- 不得把“降低 AI 检测分数”作为重写目标，不得随机改写、制造语病或无意义替换同义词；
- `sources/` 只读；
- 未经明确授权，不得由 Codex 自由重写已批准的学术正文；
- 遇到证据缺失时写入 `TODO-EVIDENCE` 并报告，禁止猜测；
- 所有新符号首次出现时定义并登记；
- 所有新术语符合术语表；
- 参考模板的类文件和资源可以保留，参考论文的正文、图表、元数据和文献库不得导入。

# Required workflow

按 `WORKFLOW_MODES.md` 选择流程。默认是单小节的快速集成模式；章节完成、对外发送或用户明确要求时使用章节里程碑审查。

每轮至少应：

1. 阅读 `AGENTS.md`、当前状态、相关章节卡和本轮任务；总契约、作者协议、作者声音与项目配置在会话首次任务或这些文件发生变化后重读；
2. 检查任务范围、工作区、分支和远端同步状态；
3. 只修改目标章节、必要的引用库、证据表、状态文件和工程文件；
4. 完整编译一次，并检查未定义引用、重复标签、缺失图片、TODO/TBD/?? 与本轮新增警告；
5. 在快速模式运行 `scripts/verify_fast_section.sh`，在里程碑模式运行完整的风格与参考论文重合审查；
6. 更新 `STATE.md`、`qa/chapter_status.csv` 和 handoff 报告；
7. 报告修改文件、编译结果、证据问题和下一步。

# Remote synchronization policy

- GitHub 私有仓库 `DLwbm123/phd-thesis` 的 `main` 分支是 GPT Pro/Codex 写作工程的远端版本源；所有已完成并通过核验的写作、证据、提示词、状态和工程修改都应提交并推送到 `origin/main`。
- `sources/` 始终只读且只保留在本机，不上传 GitHub 或 Overleaf；LaTeX 构建产物、缓存和导出包也不进入版本库。
- Overleaf 项目 `6a69ac75d6170c19b9e2711a` 只用于作者查看编译结果，不作为正文修改源。不要在 Overleaf 中进行需要保留的编辑。
- 当任务修改任何 Overleaf 编译输入（包括 `.tex`、`.bib`、模板类文件、配置、图或表）时，必须先完成编译与审查并推送 GitHub，再执行 `bash scripts/sync_latex_to_overleaf.sh`。
- Overleaf 只同步可编译 LaTeX 子集；不得同步提示词、handoff、证据表、QA 数据或 `sources/`。
- GitHub 与 Overleaf 均禁止强制推送。若远端发生并发更新，停止并先核对差异。

# Definition of done

- 全文编译成功，或明确区分既有错误和本次新增错误；
- 没有引入新的 undefined citation/reference、重复 label 或缺失文件；
- 新事实有来源，新数字与原始结果一致；
- 已按 `WORKFLOW_MODES.md` 完成快速差异审查，或在里程碑节点完成全量风格与文本重合审查；
- Git diff 不含无关修改；
- `handoff/LATEST_CODEX_REPORT.md` 已更新。
- 已完成 `origin/main` 推送；若本轮修改了 Overleaf 编译输入，也已完成 Overleaf 同步并回读核验。
