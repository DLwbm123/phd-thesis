# Codex 最新报告：ScribbleCL 作者贡献边界与第一章研究现状修订（2026-08-09）

## 本轮交付

- 本轮作者决定取代此前任何与其冲突的第五章组织要求：论文四项工作固定为 Benchmark、FedSubMerge、ScribbleCL、SAMCL。文献 `zhang2026zscribbleseg` 的正式题名、作者、期刊和 DOI 保留在参考文献库；该文献只作为 ScribbleCL 当前任务弱监督模块的引用基础。
- 第一章 1.2 删除作者本人参与的 Benchmark、SAMCL 和静态弱监督论文内容，改为外部持续分割与弱监督文献的协议、评价和研究缺口综述。自动检查确认 1.2 不含自有方法名、自引键、章节前向指引或“本文/本论文”自指。
- 第五章 5.3 现以 ScribbleCL 为唯一分割论文工作：5.3.1 的机制、公式、静态表格和图注均明确标为文献事实，5.3.2 只包含新增持续协议与分析。公开显示名使用 `\mathcal{L}_{\mathrm{WS}}`、`WS-FT`、`ScribbleCL` 和 `PCE/WS`；内部 `ZS` 代码/日志标识仅在 `experiments/scribblecl/PROTOCOL.md` 映射。
- 静态结果数值未改动，ScribbleCL 继续为 `TODO-EXPERIMENT` / `blocked_by_experiments`，未写入任何新增性能数值、方向性结论或完成性结论。
- Mode B 构建成功：`bash scripts/build_and_audit.sh` 生成 123 页 `main.pdf`，无 LaTeX error、未定义 citation/reference、重复标签或缺失文件。MuPDF 视觉复核 PDF 页 19、21、23（第一章 1.2），29、31、32（RQ3 与工作逻辑），89、91、93、95、97（5.3）以及 102、103（5.5/5.6），未见裁切、重叠或标签解析问题。
- `sources/` 排序 SHA-256 清单指纹仍为 `6c5d3c84a5418fffc6f2c3130b0a3939343acc9403b15dd53fe76e18f17ebf8f`，未进入本轮 diff。

# 历史报告：第一、二章 Mode B 对齐修订（2026-08-08）

## 本轮交付

- 基线为 `main` 的 `7d2950dcc86832044fd3489c59e1752a5be235ec`。批准稿为 `CH01_CH02_REVISION_SPEC.md`，执行任务为 `CODEX_TASK_ch01_ch02_alignment_revision.md`；批准正文和 TikZ 代码均按其集成，未自由改写。
- 第一章完成 1.3 的 Benchmark → FedSubMerge → ScribbleCL → SAMCL 重排；更新 1.1.4、1.2.1 限定段落、图 1-1 和图 1-2，并同步契约、章节卡、计划、状态与 claim section_id。第二章完成 HD/HD95/ASSD、Acc/ACC、2.2 严格术语、完整联合训练行与 $d/p$ 投影符号修订。
- 已同步 claims、equations、notation 与 terminology 账本，CSV 模式与键唯一性通过。新公式标签为 `eq:foundations-seg-directed-distance`、`eq:foundations-seg-hd`、`eq:foundations-seg-hd95`、`eq:foundations-seg-assd` 和 `eq:foundations-cls-accuracy`；废弃的 `eq:foundations-seg-boundary` 不在活跃论文源码中。
- Mode B 构建 `bash scripts/build_and_audit.sh` 成功，PDF 为 123 页；无 LaTeX error、未定义引用/交叉引用、重复 label 或缺失文件。已视觉检查图 1-1、图 1-2、HD/HD95/ASSD、Acc/ACC、2.2、表 2-1 与 $\mathbf{I}_p$ 所在页，确认无裁切、重叠或歧义。
- Scribble 保护子节、RQ3、创新点（3）及 TODO 与基线逐字一致；Chapter 5、`evidence/experiments.csv`、`sources/` 均无差异。`sources/` 仍为 237 文件、指纹 `6c5d3c84a5418fffc6f2c3130b0a3939343acc9403b15dd53fe76e18f17ebf8f`。
- ScribbleCL 仍为 `TODO-EXPERIMENT` / `blocked_by_experiments`；未改动其任务、基线、状态、数字、结果或结论。详细审查记录见 `handoff/MODE_B_CH01_CH02_ALIGNMENT_AUDIT.md`，GPT 上下文包已重建。

# 历史报告：第二章剩余内容整章工程集成（2026-08-01）

## 第五章 ZScribbleSeg、ScribbleCL 与 SAMCL 集成状态（2026-08-05）

- 已将作者批准稿 `CH05_DRAFT_FOR_REVIEW.tex`（SHA-256 `2f377a56ffb4970dbf839a8511da18e24301003ce34c99167c571ffdcd5d7e23`）完整写入 `chapters/ch05_scribble_samcl.tex`；仅为消除一处数学行溢出，将式（5.16）的等价减项拆行，未改语义、数值或作者结论。
- 本章登记 19 个公式、8 张表和 108 个原始静态实验数值。ZScribbleSeg 的 Decathlon-Prostate Dice 以表格事实 `0.706` 登记；正文中相冲突的 `0.726` 已明确标为待作者核对，不作替换或推断。
- ScribbleCL 仅纳入任务协议、监督/历史访问边界、配对设计和评价定义；当前没有可核验的 ScribbleCL 结果、性能表或结论，状态保持 `blocked_by_experiments`，不得将静态 ZScribbleSeg 结果外推为持续学习结果。
- 仅逐字节复制两张可直接使用的 SAMCL 原始 PDF 图：`samcl_framework.pdf`（SHA-256 `bd950fcf8320c604e577f92d47d2b0bf17a6141457896c1debbbe2e8f0704559`）和 `samcl_qualitative.pdf`（SHA-256 `321fa6987a264182351685ee443f9489b135ce57347adb24c5e34da82afe6930`）。未转换 ZScribbleSeg PNG，亦未拼接 SAMCL 消融/泛化两图，因此两个不可安全构造的图位被 `\\IfFileExists` 保持省略。
- 已执行指定审计、清理与 XeLaTeX 完整构建。当前 `main.pdf` 为 121 页，SHA-256 `7528a362f4376fe07033ee1961384afed026c40558a0caebe4982643613b3596`；章节页码为印刷页 71--88。MuPDF 已逐页复核该范围及相邻过渡页，中文、公式、表格和两张原始图均正常。`pdffonts` 确认 Fandol CJK 字体嵌入并子集化。
- `sources/zscribble`（26 文件，`48367f5b56a12cffe357ea9c6f5c26a9947781467c7b9b7f61ef53de6bd8ff9d`）、`sources/samcl`（12 文件，`d043158cf22668283643da294d40dba5505279ee41b7bfe567f65a733750a4a6`）与 `sources/benchmark`（31 文件，`b9a529ada136e552fcd183df573d98c32048b0db53d3b0169a8490af879e8cad`）的开始/结束排序清单指纹一致。未修改 `sources/`、第一至第四章或字体配置。本轮尚未提交、推送或同步 Overleaf，须等待作者明确授权。

## 第四章 FedSubMerge 集成状态（2026-08-05）

- 已将作者批准稿写入 `chapters/ch04_fedsubmerge.tex`，并复制并校验三张最终矢量图；最终主稿、附录、文献库和三张图均通过指定 SHA-256 校验。
- 已补入最终文献库中 17 条实际被第四章引用的记录，并复用既有的 4 条同一文献记录，避免重复题名；数值账本已登记 196 个主表、40 个异质性、27 个规模和 28 个消融值，30 个公式和章节状态已登记。
- `latexmk` 成功生成 105 页 PDF（SHA-256 `14c5ca7194c96b09febe7f72e41abf4ce388237facf4ef2797eaaa7cd8d9428d`），章节交叉引用和引文均已解析，风格审查未报告第四章规则命中，参考论文重合审查未发现达到阈值的长文本重合。
- `config/thesis_info.tex` 保持 `cjk-font = fandol` 未改。`pdffonts` 确认 FandolSong、FandolHei、FandolKai 等 CJK 字体均已嵌入并子集化；MuPDF 逐页复核第三章代表页 34 与第四章印刷页 51--69，中文、公式、表格和图件均正常。macOS Quick Look/PDFKit 复核亦正常。
- 结论：Poppler `pdftoppm` 的 CJK 空白是该工具的渲染/映射限制，不是论文或 Fandol 字体配置缺陷；未使用 macOS 专用字体规避。视觉验收已关闭，可按发布流程提交、推送并同步 Overleaf。

## FedSubMerge 最终事实源替换（2026-08-05）

- 作者提供的 `FedSubMerge_final.zip` 已完整替换 `sources/fedsubmerge/ Subspace Merging for Replay-Free Federated Continual Medical Image Classification 720/` 的早期无附录稿。当前事实源入口为 `FedSubMerge_final.tex`，并包括 `FedSubMerge_appendix.tex`、`references.bib`、样式文件及 `Figs/` 下的三张最终图。
- 安装文件逐项 SHA-256 已与压缩包解出的文件一致。替换前版本已保留在 `/Users/bominwang/Desktop/Supspace Merging 文章投稿/check_appendix/FedSubMerge_project_source_before_final_20260805`，未删除。
- `SOURCE_MAP.md` 与证据账本 C1-120--C1-124 已将事实源定位更新为最终主稿；本轮未改论文正文、实验数字、第四章状态或其他原始材料。

## 第二章剩余内容整章工程集成

- 已将批准稿从 `\subsection{医学图像分类}` 至第二章末尾完整写入 `chapters/ch02_foundations.tex`；2.1.1/2.1.2 的保护段落将以提交前差异核验确认逐字未改。新增 12 个公式标签和 2 张比较表，第二章整体及 2.1.3、2.2--2.4 均为 `drafted_pending_review`。
- 新增 8 条经任务指定元数据核验的文献：Goodfellow、Fawcett、Brodersen、Geiping、Bonawitz、Abadi、Finn、Foret；其余正文引用均复用现有 key。新增 claims C2-021--C2-036（16 条）与 equations E2-005--E2-016（12 条），未写入实验账本或虚构结果。
- 已登记 13 个当前不存在的术语和 26 个实际首次使用的符号；第三章状态/正文不变，ScribbleCL 继续 `TODO-EXPERIMENT` / `blocked_by_experiments`，TRE/Jacobian 两项 TODO 继续开放。构建、视觉、风格和重合审查结果将在完成后补入本报告；下一步仅为第二章整章复审，不开始第四章。
- 已执行 `bash scripts/build_and_audit.sh`、`latexmk -C main.tex` 与完整 XeLaTeX 构建，并通过 `scripts/verify_fast_section.sh --quiet chapters/ch02_foundations.tex`。最终 `main.pdf` 为 85 页；日志无 undefined citation/reference、duplicate label、missing file 或新增 overfull/underfull 警告。第二章新增内容使全文比集成前增加 8 页；新增内容覆盖日志页 22--30，第三章从第 32 页开始。
- 已核验 12 个公式标签和 2 个表标签均唯一；两张表采用纯列宽调整且未改变表意。Poppler 对 CJK 正文仍受字形映射限制，故结合 XeLaTeX 成功构建、无溢出日志和公式/表格可见内容进行视觉核验；未发现裁切、重叠或异常空白。
- `git diff --unified=0` 确认第二章改动仅从 2.1.3 标题后的原空骨架开始，2.1.1/2.1.2 未改；第三章和其他正文 `.tex` 未改。风格审查、与参考毕业论文的文本重合审查已由里程碑脚本运行；本轮新增文本的快速审查通过。四个 `sources/` 目录在开始和结束时文件数及 SHA-256 清单指纹一致。

# 历史报告：第二章剩余内容整章证据上下文准备（2026-08-01）

## 第二章剩余内容整章证据上下文准备

- 已创建 `handoff/CH02_REMAINING_CONTEXT_FOR_GPT.md`，其范围为 2.1.3、2.2、2.3 与 2.4 的一次性证据化写作蓝图：章节论证链、去重映射、十个部分的段落级提纲、分类/访问条件/持续学习候选公式、两张候选比较表、临时论断与限制、最小文献集以及 GPT Pro 交付清单均已给出；它不是正式博士论文正文。
- 上下文严格保留 2.1.1 和 2.1.2 的既有符号、标签和过渡；不复用第三章的三类具体基准、A-Dice、BWTR、RMA、E-FWT 或实验结果；不提前给出 FedSubMerge、ZScribbleSeg、ScribbleCL 或 SAMCL 的特有机制和实验结论。FedSubMerge 的事实边界为历史原始图像无回放，SAMCL 的事实边界为有限经验回放，ZScribbleSeg 的事实边界为静态涂鸦弱监督。
- 2.2 标题建议暂保留，并在首段将“数据不全”严格限定为训练信息受限的概括；若作者需要标题完全术语一致，再决定是否改为“训练信息受限场景下的学习问题”。本轮未改正式标题、正文或 `qa/chapter_status.csv`。
- 已记录待正式集成前处理的限制：分类 CE/BCE 和分类指标的原始公式来源补核、多标签阈值/汇总与临床效用不可外推、安全聚合/差分隐私不能被写成 FedAvg 自带属性。没有阻止 GPT Pro 输出受限草稿的 BLOCKER；2.1.2 的 TRE/Jacobian 两项既有 TODO 保持开放且与本轮无关。
- 只读事实源在开始时的排序 SHA-256 清单指纹为：`sources/fedsubmerge/`（18 文件）`e52bbd5c257bfed343a6092c4d22f0c1232d12051b2b7cfeecd6c7eccf4d9ef5`，`sources/zscribble/`（26 文件）`48367f5b56a12cffe357ea9c6f5c26a9947781467c7b9b7f61ef53de6bd8ff9d`，`sources/samcl/`（12 文件）`d043158cf22668283643da294d40dba5505279ee41b7bfe567f65a733750a4a6`，`sources/benchmark/`（31 文件）`b9a529ada136e552fcd183df573d98c32048b0db53d3b0169a8490af879e8cad`。结束前必须复核一致。
- 已以 `latexmk -g -xelatex -interaction=nonstopmode -file-line-error main.tex` 强制完整构建：退出码 0，`main.pdf` 为 77 页、1,547,689 字节、SHA-256 `41725ece9b69873440cf5e0cf246f222527224890744a0b1db1047f31d379439`；最终日志无未解析引用或交叉引用。由于本轮没有 LaTeX 输入改动，视觉检查复核现有第二章 PDF 页，并未发现本轮可能引入的版式变化；Poppler 对 CJK 正文仍受字形映射限制。未运行会读取 `sources/reference_thesis/` 的重合审查，也未进行 Overleaf 同步。
- 上下文包为 192 行、26,716 字节；含 16 条临时论断、16 条候选公式与 2 张候选表。限制台账计数为：无实际 BLOCKER（表中用 1 条“无 BLOCKER”汇总项），HIGH 3、MEDIUM 4、LOW 4；正式集成时须逐项关闭或维持严格限定。
- 结束复核的四个源清单指纹与开始值完全一致。`git diff --check` 通过；受保护的 `chapters/ch02_foundations.tex`、`chapters/ch03_benchmark.tex`、所有其他 `.tex`、文献库、`evidence/*.csv`、术语/符号表和 `qa/chapter_status.csv` 均无差异。仅 `STATE.md`、本报告和新的上下文包待提交。
- 下一步：将上下文交给 GPT Pro 一次性写作第二章剩余内容；之后才可进行全章 LaTeX 集成。第三章继续 `drafted_pending_review`；ScribbleCL 继续 `TODO-EXPERIMENT` / `blocked_by_experiments`。

# 历史报告：第三章 Benchmark 整章工程集成（2026-08-01）

## 第三章 Benchmark 整章工程集成

- 已将 GPT Pro 批准的第三章全文完整集成至 `chapters/ch03_benchmark.tex`；仅将 9 个占位 citation key 映射为库内已核验 key，未改写学术内容。第三章及其 3.1--3.8、3.3.1--3.3.3 均为 `drafted_pending_review`，不得视为已验证。
- 已复制并逐字节核验四个原始图：`benchmark_overview_new.pdf`、`task_robustness_adice.pdf`、`task_robustness_bwt_from_bottom.pdf`、`domain_memory_size_adice.pdf`。8 个公式标签为 `eq:benchmark-task-distribution`、`eq:benchmark-adice`、`eq:benchmark-bwtr`、`eq:benchmark-rma`、`eq:benchmark-efwt`、`eq:benchmark-wcd`、`eq:benchmark-mpe`、`eq:benchmark-drr`。6 个表为 `tab:benchmark-scenarios`（第28页）、`tab:benchmark-datasets`（第30页）、`tab:benchmark-methods`（第31页）、`tab:benchmark-domain-results`（第34页）、`tab:benchmark-class-results`（第36页）、`tab:benchmark-organ-results`（第37页）；4 个图为 `fig:benchmark-overview`（第26页）、`fig:benchmark-order-adice`（第38页）、`fig:benchmark-order-bwtr`（第38页）、`fig:benchmark-memory`（第39页）。
- 实际复用并重命名的 citation key：`wang2024continualsurvey`、`kumari2025medicalcl`、`yuan2024continualseg`、`gonzalez2023lifelong`、`kirkpatrick2017ewc`、`li2018lwf`、`saha2021gpm`、`cermelli2020mib`、`douillard2021plop`；其余本章实际引用均已按源稿信息补齐 author/title/year/venue 元数据。
- 已追加 C3B-001--C3B-015、E3B-001--E3B-008、256 条 Benchmark 实验记录和 LIM-BM-001--LIM-BM-008，并登记本章术语与符号。所有数字仅转录原始活动表；不补造样本量、种子、硬件、代码版本或统计检验。
- 原始材料指纹在开始和结束时一致：`sources/benchmark/` 共 31 个文件，排序 SHA-256 清单指纹为 `b9a529ada136e552fcd183df573d98c32048b0db53d3b0169a8490af879e8cad`；主稿 `main.tex` SHA-256 为 `b88ae877066b6e826f968a2239c9047d56c32e33bacfe94ffa2c3b10c2b8a1ee`，补充材料 `supplementary.tex` 为 `34813f5d264b97b6404a9b74fca5fdf889ec33d97c4ff8c5b101073cf7fcba4b`。源码只读，未进入 Git diff。
- 证据限制仍然成立：归档源没有指标实现代码、配置、代码版本、随机种子、硬件、完整样本量或统计检验；因此不能声称公式—代码复现。原 Benchmark 工程在当前环境因缺少 `makecell.sty` 及 Palatino 字体度量而未成功编译，未修改其任何文件。
- 已运行 `bash scripts/build_and_audit.sh`，并运行 `latexmk -C main.tex` 后完整 XeLaTeX 构建。`main.pdf` 共 77 页，第三章为第25--41页（17 页），大小 1,547,689 字节，SHA-256 为 `41725ece9b69873440cf5e0cf246f222527224890744a0b1db1047f31d379439`。最终日志无未解析引用、交叉引用或 overfull 警告；三张宽表已仅作缩放级排版修复。已逐页核查第三章及与第四章的过渡、四张图、六张表和公式页；Poppler 渲染器不能显示 CJK 正文，故以 XeLaTeX 完整构建、无溢出日志和可见图表/数学内容共同核验，未见裁切、重叠、异常空白或不可读图表。
- 下一步仅为第三章作者/GPT Pro 整章复审，重点复核公式、三张结果表、图表和结论边界；复审前不得开始第四章。

# 历史报告：第一章作者复审定向精修（2026-07-31）

## 第三章 Benchmark 整章证据上下文准备（2026-08-01）

- 已创建 `handoff/CH03_BENCHMARK_CONTEXT_FOR_GPT.md`：覆盖第三章 3.1--3.8 的论证链、段落级提纲、三类场景、数据/任务序列、统一协议、八个候选公式、完整结果表账本、图像账本、文献最小集合、证据候选和 GPT 整章写作清单；未生成正式学术正文。
- 实际采用 Benchmark 主入口为 `sources/benchmark/Benchmark_pa/main.tex`（1,431 行），补充材料为同目录 `supplementary.tex`（119 行），引用为主文件内嵌 `thebibliography`。已核查所有活动表和图的源定位，并实际视觉检查基准概览、任务顺序 A-Dice 和缓存规模图。
- 在仓库外临时副本编译原始主稿受本机 TinyTeX 缺少 `makecell.sty` 与 Palatino 字体度量阻塞；未修改 `sources/`，也未报告虚假的 PDF 页数。原始目录亦无实验脚本、指标实现、配置、代码版本、种子、硬件或运行日志；RMA/E-FWT 完成公式—表格与最小索引核验，但不能完成公式—代码一致性核验，已作为 `BLOCKER` 明示。
- 主要阻塞项为 2 个（代码不可得、原稿本机无法编译）；另有 3 个 HIGH（样本/种子/硬件缺失、Class-CL 访问协议不完整、统计重复数缺失）、2 个 MEDIUM 和 1 个 LOW。第三章状态保持 `not_started`；第二章状态和 ScribbleCL `TODO-EXPERIMENT` / `blocked_by_experiments` 均未变。
- 本轮只允许修改上下文、状态和 handoff 报告；没有修改 `chapters/ch03_benchmark.tex`、任何正式证据 CSV、术语/符号表、文献库或其他 LaTeX 输入，也不执行 Overleaf 同步。下一步是将本上下文和本报告交给 GPT Pro 一次性撰写第三章全文。

## 2.1.2 医学图像配准正文集成（2026-07-31）

- 已在 `chapters/ch02_foundations.tex` 的 `\subsection{医学图像配准}` 标签后、`\subsection{医学图像分类}` 前精确集成批准正文；2.1.1 与 2.1.3 正文经差异核验未修改。
- 实际复用 `balakrishnan2019voxelmorph` 和 `wang2024samcl`；新增并经 DOI/原始元数据核验的条目为 `sotiras2013deformable`、`rueckert1999ffd`、`pluim2003mi`、`avants2008syn`、`jaderberg2015stn`、`klein2009evaluation` 与 `rohlfing2012surrogates`。Klein 条目采用已核验的完整作者表。
- 已追加 C2-010--C2-020 和 E2-001--E2-004，并登记 $I_F$、$I_M$、$\Omega_F$、$\Omega_M$、$\phi$、$\mathbf{x}$、$\mathbf{u}$、$W$、$g_\theta$、$D$、$\mathcal{R}$、$\lambda$ 与 $\mathcal{D}_{\mathrm{reg}}$；$\theta$ 复用既有登记。变换方向统一为 $\phi:\Omega_F\to\Omega_M$，配准后移动图像为 $I_M\circ\phi$。
- `TODO-EVIDENCE-REG-001`（TRE 通用数学定义）和 `TODO-EVIDENCE-REG-002`（非正 Jacobian 比例统计形式）保持未闭合；它们均未写入正文或 `evidence/equations.csv`。
- 已完成 `latexmk -xelatex -interaction=nonstopmode -file-line-error main.tex`（59 页，PDF SHA-256 `1eff2d692448ff17108cf0741a4bf8b05262d5ec72caced1da1b1ffbf703d765`）及 `bash scripts/verify_fast_section.sh --quiet chapters/ch02_foundations.tex`（53 个 BibTeX 键、99 个术语键）。最终日志无未解析引用或交叉引用警告；CSV 账本无重复 ID，四个新公式标签各出现一次，活动引用键均存在，`git diff --check` 通过。
- 已视觉核验 2.1.1 末页至 2.1.2 起始、2.1.2 的连续公式页及 2.1.3 起始页，未见裁切、重叠或空白异常；参考文献页也已检查。Poppler 临时渲染器缺少 Adobe-GB1 映射而不能显示 CJK 正文，因此以 XeLaTeX 成功构建、无版面警告和 macOS 本地 PDF 渲染共同确认中文排版。`sources/` 保持只读且不在 Git diff 中。下一步只允许准备 2.1.3“医学图像分类”的证据上下文，不得直接自由撰写。

## 2.1.2 医学图像配准证据上下文准备（2026-07-31）

- 本轮只更新 `handoff/CONTEXT_PACKET_FOR_GPT.md` 与 `STATE.md`，未修改任何正式学术正文、2.1.1、2.1.3、文献库、LaTeX 输入或 `sources/`。
- 已只读核查本地 SAMCL 源：`sources/samcl/MICCAI 2024: Toward Universal Medical Image Registration/Paper-0150.tex` 第 3 节给出固定图像、移动图像、$\phi:\Omega_F\to\Omega_M$、$m\circ\phi_\theta$ 和 $D+R$ 的一般配准写法；其顺序任务、有限回放、元学习、锐度感知、网络配置和实验设置均明确留在第五章 5.4，不进入 2.1.2。
- 已核验的外部原始文献最小候选集合：Sotiras et al. (2013, DOI `10.1109/TMI.2013.2265603`)、Rueckert et al. (1999, DOI `10.1109/42.796284`)、Pluim et al. (2003, DOI `10.1109/TMI.2003.815867`)、Avants et al. (2008, DOI `10.1016/j.media.2007.06.004`)、现有 VoxelMorph 条目 (2019, DOI `10.1109/TMI.2019.2897538`)、Jaderberg et al. (2015, NeurIPS)、Klein et al. (2009, DOI `10.1016/j.neuroimage.2008.12.037`) 与 Rohlfing (2012, DOI `10.1109/TMI.2011.2163944`)。
- 统一候选方向为 $\phi:\Omega_F\to\Omega_M$，在固定坐标 $\mathbf{x}$ 上重采样移动图像 $I_M\circ\phi$；候选公式包括重采样、位移场、经典/学习式目标、TRE 和非正 Jacobian 比例。TRE 通用公式和非正 Jacobian 统计形式各保留一项 `TODO-EVIDENCE`，尚不能作为已核实正文内容。
- `qa/chapter_status.csv` 保持 2.1.2=`queued`，因现有状态体系没有“上下文已准备”枚举；`STATE.md` 记录 `context_ready`。下一步推荐提示词：**开始撰写 2.1.2 医学图像配准**。

## GPT Pro 学术复审批准与合并前核验

- 题目、第一章和连续六章框架已于 2026-07-31 通过 GPT Pro 学术复审。第一章现可标记为 `drafted_and_verified`；本轮未修改任何学术正文、引用或 LaTeX 配置。
- 合并 `main` 前的核验已确认当前分支为 `framework/supervisor-2026-07-31`，工作树起始时干净，并包含 `4afd1353f5b3f35dcb1027573c436ce3ef08d4fe` 和 `898a828650aec8d88eba2c6aaa21dfe8a064309c`。
- `git fetch origin` 后，`origin/main...HEAD` 为 `0 4`：`origin/main` 没有新的并发提交，因此未执行 rebase、merge 或强制推送。本轮下一步是合并 `main`；合并后才由 Codex 准备 2.1.2“医学图像配准”的证据上下文。
- 2.1.2 仍为 `queued`，本轮未撰写正文。ScribbleCL 仍为 `TODO-EXPERIMENT` / `blocked_by_experiments`，须先具备任务协议、代码版本、数据划分、随机种子、逐阶段日志、性能矩阵、表格和可复现证据。

## 本轮范围与分支保护

- 分支始终为 `framework/supervisor-2026-07-31`，以已完成迁移的 `abee962cccaf9a29fa5b72f43fbf643ce0cc1ca0` 为起点；未重建分支、未合并或覆盖 `main`，也未执行 reset、clean 或 checkout 丢弃本地工作。
- 本轮只精修论文题目与第一章的定向内容；未重迁章节，未修改第二章 `2.1.1`，未撰写 `2.1.2`，未生成或声称任何 ScribbleCL 实验结果。

## 作者复审结论已落盘

- 工作题目已统一为：中文 **面向任务持续演化与训练信息受限的医学影像持续学习研究**；英文 **Continual Learning for Medical Image Analysis under Evolving Tasks and Limited Training Information**。
- “训练信息受限”作为正文严格技术术语，限定为训练阶段无法完整调用潜在可用的监督、历史或跨中心原始信息；“数据不全”仅作为背景概括，不等同随机缺失值或物理删除。题目、`THESIS_CONTRACT.md`、`STATE.md`、章节卡、提示词、上下文包、证据账本和启动说明均已同步。
- 连续六章结构保持不变。第一章状态继续保持作者复审中，未越过作者确认门槛。

## 第一章定向修订

- `1.1.2` 已压缩为：全量离线训练假设为何失效、当前阶段可调用性的相对性、集合定义与过渡；监督生成、时间可访问性和跨机构治理的三类细分移至 `1.1.3` 承接。
- `1.2.3` 已改为“弱监督与部分监督医学图像分割研究现状”；`1.3.2` 已改为“部分监督下的监督覆盖不足与结构信息缺失”。
- 贡献（3）已改为“提出基于监督增强与先验正则化的涂鸦监督医学图像分割方法，并研究其持续学习扩展。”已完成的 ZScribbleSeg 与待补齐任务协议、日志、性能矩阵和证据的 ScribbleCL 严格分开；`TODO-EXPERIMENT` 保留。
- 对“同时”逐处复审：从 30 处降为 22 处，仅修改语义上不应表示并发的 8 处。其余 22 处均表达真实的时间并发、共同变化或并列要求，未作机械替换。

## 构建与 QA

- 已执行 `latexmk -C main.tex`，随后执行 `latexmk -xelatex -interaction=nonstopmode -file-line-error main.tex`，退出码均为 0。
- `main.pdf`：55 页、728,203 字节、SHA-256 `875d9c348ec255ffdca56a3735fea8a2755320f6a56c19985e63f81665502b05`。最终 `main.log` 无 undefined citation/reference、missing file、duplicate label 或 overfull/underfull 警告。
- 静态引用检查：46 个活动引用键全部存在；84 个活动标签无重复。`style_audit.py` 已更新报告，第一章“同时”为 22 处且无段首重复；`reference_overlap_audit.py` 未发现达到阈值的参考文本重合。
- macOS Quick Look 已视觉核验封面：中英文题目均正确显示。其余关键页面与章节入口结合 XeLaTeX 完整构建日志和无版面告警检查；未观察到裁切或异常空白。

## 后续受控动作

- GitHub 已推送提交 `4afd1353f5b3f35dcb1027573c436ce3ef08d4fe` 至 `origin/framework/supervisor-2026-07-31`；Overleaf 已完成干净副本完整构建和非强制同步，远端提交 `574d4fb8b3859b3cd3fe492e6c1a4bf2539998c5` 来源于该 GitHub 提交。
- 作者应只复审题目、第一章术语与贡献边界；不得据此继续撰写 `2.1.2`。
- ScribbleCL 仍必须先补齐任务协议、代码版本、数据划分、随机种子、逐阶段日志、性能矩阵、表格和可复现证据，才可进入实验性表述。

---

# 历史记录：导师框架迁移（2026-07-31）

## 分支、保护与范围

- 分支：`framework/supervisor-2026-07-31`；迁移基线：`c74d0b2`。未切换或合并 `main`，未执行 reset、clean 或 checkout 丢弃工作。
- 未提交工作开始前已保存可恢复补丁：`/Users/bominwang/Downloads/phd-thesis-framework-migration-20260731-162417.patch`，SHA-256 `38f301511f65a5bef35b4c254dd1eb12662d22dc292a05c051f3736015593d5a`。该补丁未加入仓库。
- GitHub 迁移提交：`0a839010742f85bde98fc2e167d836cf5bea8316`，已推送至 `origin/framework/supervisor-2026-07-31`；未合并或覆盖 `main`。
- Overleaf 已在完整部署构建后同步，远端提交：`9b394141049b58fda5379cd868378ad73a5c4ac5`，部署来源为上述 GitHub 迁移提交。

## 结构与内容迁移

- 正文入口已改为连续六章：Benchmark（旧第4章）→ 第3章；FedSubMerge（旧第6章）→ 第4章；ZScribbleSeg（旧第3章）与 SAMCL（旧第5章）→ 第5章的5.3.1与5.4；总结（旧第7章）→ 第6章。旧章节文件不再被 `main.tex` 引用，`chapter_cards/ch07.md` 已退役。
- 第一章按 1.1.1--1.1.4、1.2.1--1.2.3、1.3.1--1.3.4 和 1.4 重构；原 1.5 已并入 1.4 末尾。保留已核实引用与审慎边界，并首次定义“数据不全”不等于缺失值或物理删除。
- 第一章贡献顺序为 Benchmark → FedSubMerge → ZScribbleSeg/ScribbleCL → SAMCL。原始 ZScribbleSeg 仍为静态弱监督方法；ScribbleCL 保持 `TODO-EXPERIMENT`。SAMCL 明确有限回放；FedSubMerge 不声称形式化隐私。
- 第二章 2.1.1 保持迁移前已验证正文和公式；只调整章名和2.1.2后的骨架。2.1.2 状态仍为 `queued`。

## 账本与状态

- `evidence/claims.csv`：151 条记录均保留；10 条 ZScribbleSeg 记录人工映射至 5.3.1；旧 1.2/1.3 记录按语义重映射，8 条旧 1.5 结构记录并入 1.4 并改写为六章说明。
- `evidence/experiments.csv` 与 `evidence/equations.csv` 为空，未虚构实验或公式；`evidence/limitations.csv` 已重映射至 4.7、5.6 和 6.3。
- `qa/chapter_status.csv` 标记第一章为 `drafted_pending_review` / `drafted_pending_reverification`，2.1.1 为 `drafted_and_verified`，2.1.2 为 `queued`。

## 构建与 QA

- 执行：`latexmk -C main.tex`，随后 `latexmk -xelatex -interaction=nonstopmode -file-line-error main.tex`；退出码均为 0。
- PDF：55 页，730,359 字节，SHA-256 `c56578652aed221e1a8cb23e0cd1de07740e180f7433b367948cfff167527e64`。
- 静态检查：46 个活动引用键全部存在；84 个活动标签无重复；无 undefined citation/reference、missing file、duplicate label 或 overfull/underfull 警告。
- 已运行 `style_audit.py` 与 `reference_overlap_audit.py`。前者只提示第一章“同时”30 次，需作者结合文意复审；后者未发现达到 28 个规范化字符阈值的参考论文长文本重合。
- PDF 视觉核验覆盖封面、目录/前置部分、第一章页、第二章 2.1.1 页、第三至第六章首页与参考文献首页；Quick Look 正常渲染中文封面和新暂定题目。基于 Poppler 的临时渲染器未显示正文 CJK 字形，故以 XeLaTeX 构建日志、Quick Look 和无版面警告共同核验；未观察到裁切或异常空白。

## 作者待审与下一动作

- `AUTHOR-DECISION-REQUIRED`：暂定题目是否采用候选一；是否正式采用连续六章；“数据不全”定义与第一章 1.1.2--1.1.4、1.2.3、1.3.2、1.4 的表述强度。
- ScribbleCL 仍缺任务协议、代码版本、数据划分、种子、逐阶段日志、性能矩阵、表格与可复现证据；在这些材料齐备前不得写结果或称为新算法。
- 下一步只能是作者复审第一章、题目与六章目录；不得直接继续 2.1.2。
