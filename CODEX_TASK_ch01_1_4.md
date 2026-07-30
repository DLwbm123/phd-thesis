# Codex Task: integrate Chapter 1, Section 1.4

Read and obey `AGENTS.md`, `WORKFLOW_MODES.md`, `THESIS_CONTRACT.md`, `AUTHORSHIP_PROTOCOL.md`, `AUTHOR_VOICE.md`, `STATE.md`, `PROJECT_CONFIG.md`, `SOURCE_MAP.md`, and `chapter_cards/ch01.md` before editing.

## Workflow mode

Use **Mode A: fast section integration** in `WORKFLOW_MODES.md`.

Section 1.4 is a pure-text section. Run the required complete build and changed-text audits once through:

```bash
bash scripts/verify_fast_section.sh --quiet chapters/ch01_introduction.tex
```

Do not duplicate this command with a routine second full build unless it fails and a diagnostic build is necessary. Do not run the Chapter 1 milestone audit, full PDF visual inspection, or rebuild `handoff/CONTEXT_PACKET_FOR_GPT.md` in this task. Chapter 1 is not complete until Section 1.5 has been drafted and verified.

After the verified content commit is pushed, synchronize the compilable LaTeX subset to Overleaf with the verified build fingerprint:

```bash
bash scripts/sync_latex_to_overleaf.sh --skip-local-build "Sync Chapter 1 Section 1.4"
```

Report the GitHub content SHA and Overleaf deployment SHA in the final terminal response. Do not create a second GitHub commit solely to store the deployment receipt.

## Goal

Integrate the GPT Pro-approved draft for Section 1.4 “本文主要研究内容与创新点” into the thesis repository.

This section must accurately synthesize the four source studies into the research content and innovations of Chapters 3--6:

1. ZScribbleSeg: annotation-efficient scribble-supervised medical image segmentation;
2. continual medical image segmentation scenario definition and comprehensive benchmarking;
3. SAMCL: centralized continual medical image registration with limited experience replay;
4. FedSubMerge/FedSubMerge-AD: replay-free federated continual medical image classification.

The section must make the common thesis background clear while preserving the four works’ different tasks, data-access assumptions, methods, evaluation objectives, and claim scopes.

Stop after Section 1.4 is completed and verified. Do not draft Section 1.5 or any later chapter.

## Primary evidence basis

Read the following original source files before editing:

- `sources/zscribble/Zscribble_MEDIA_arxiv/main_clean_new.tex`
- `sources/benchmark/Benchmark_pa/main.tex`
- `sources/samcl/MICCAI 2024: Toward Universal Medical Image Registration/Paper-0150.tex`
- `sources/fedsubmerge/ Subspace Merging for Replay-Free Federated Continual Medical Image Classification 720/FedSubMerge_main_no_appendix.tex`

Also read the corresponding source bibliographies or embedded references only when necessary to verify a method name or source boundary. Do not edit any file under `sources/`.

Use the source files as factual evidence, not as text to translate or paraphrase. The approved Chinese prose below is an original thesis-level synthesis.

The active bibliography already contains the verified self-paper keys:

- `zhang2026zscribbleseg`
- `wang2026benchmark`
- `wang2024samcl`

The current FedSubMerge source is an anonymized manuscript and does not provide a verified final self-citation record. Do not invent its authors, venue, year, DOI, title variant, or BibTeX entry.

The approved Section 1.4 prose intentionally contains no active citation command. This keeps all four thesis contributions in a uniform self-work presentation and avoids creating an unverified FedSubMerge self-reference. Do not add citations to the approved text.

## Strict scientific boundaries

### Overall structure

- Do not imply that the four studies form one algorithm or that each later method is a technical extension of the previous one.
- Do not invent a common mathematical framework that is absent from the source studies.
- Do not introduce formulas, algorithm boxes, figures, tables, hyperparameters, detailed rankings, or quantitative performance gains.
- Do not claim clinical deployment, regulatory approval, formal privacy protection, or universal applicability.
- Do not use promotional expressions such as “全面优于”, “彻底解决”, “充分证明”, or unsupported “显著提升”.
- Do not import prose, citation combinations, figures, tables, metadata, or structure from `sources/reference_thesis/`.

### ZScribbleSeg

- Treat ZScribbleSeg as weakly supervised and annotation-efficient medical image segmentation, not continual learning.
- Do not use stability, plasticity, catastrophic forgetting, old task, or new task to characterize this work.
- Describe efficient scribble properties, supervision augmentation, global consistency, class-mixture estimation, spatial prior, and shape regularization only within the source-supported scope.
- Do not claim that any fixed class proportion, spatial prior, or shape prior is valid for every anatomy, modality, or pathology.
- Do not claim dense-label equivalence or clinical replacement.

### Continual segmentation benchmark

- Treat Chapter 4 as scenario definition, metric design, unified protocol, and systematic empirical evaluation, not a single anti-forgetting algorithm.
- `Domain-CL`, `Class-CL`, and `Organ-CL` are names used by this benchmark; do not present them as a field-wide exhaustive standard.
- Keep `Restricted Modeling Ability (RMA)` as a plasticity metric that compares current-task performance under continual constraints with an independently trained reference.
- Keep `Extended Forward Transfer (E-FWT)` as the paper’s metric name. When explaining the evaluated capability, use the thesis term “前向泛化” for direct performance on domains not yet used in optimization.
- Do not use “前向迁移” and “前向泛化” as synonyms.
- Do not claim that any method family is universally best.

### SAMCL

- Describe SAMCL as centralized continual registration with limited experience replay, not replay-free or federated learning.
- Do not classify registration mechanically as class-incremental learning.
- Do not claim that a limited memory buffer reconstructs the full historical distribution.
- Do not claim that loss-landscape flatness alone guarantees universal registration.
- Present the work as an initial exploration toward universal 3D registration in sequential learning conditions.
- Do not claim that forgetting, task-order sensitivity, or out-of-domain registration has been fully solved.

### FedSubMerge

- Describe the task as replay-free federated continual medical image classification, not segmentation or registration.
- Define replay-free as no reuse of historical raw training samples during later task updates; compact model-derived summaries are not thereby prohibited.
- Preserve the current receive--project--update--merge logic: the server-returned PGS protects local training and also contributes historical information to the next task-boundary client PGS update.
- Do not describe each client as maintaining a purely independent local-history PGS after the first server return.
- Distinguish uniform FedSubMerge from layer-wise adaptive FedSubMerge-AD.
- Do not claim that merging every client direction is always beneficial.
- Do not claim that transmitting low-rank PGS bases and singular values provides a formal privacy guarantee.
- Keep the current empirical scope limited to medical image classification and the source-reported heterogeneity settings.

## Strict file scope

Files that may be modified or added:

- `CODEX_TASK_ch01_1_4.md`
- `chapters/ch01_introduction.tex`
- `evidence/claims.csv`
- `qa/terminology.csv`
- `qa/chapter_status.csv`
- `qa/style_audit_report.md`
- `qa/reference_overlap_report.md`
- `STATE.md`
- `handoff/LATEST_CODEX_REPORT.md`

Read-only verification targets:

- `bibliography/references.bib`
- `config/build_flags.tex`
- all files under `sources/`

Do not modify another chapter, template/class file, build script, figure, table, bibliography record, bibliography style, or the GPT context packet.

Do not rewrite approved prose outside Section 1.4. Except for a strictly necessary LaTeX syntax correction, integrate the approved text exactly.

## Step 0: repository and baseline preflight

1. Run:

   ```bash
   git status --short
   git branch --show-current
   git fetch origin
   ```

2. The worktree must be clean except that `CODEX_TASK_ch01_1_4.md` may be the only untracked file.
3. Confirm the current branch is `main`.
4. Confirm local `HEAD` is not behind or divergent from `origin/main`.
   - Use `git pull --ff-only origin main` only when the remote is ahead and the worktree is otherwise clean.
   - Stop on divergence, conflict, or unrelated modification. Do not reset, rebase, overwrite, or force-push.
5. Record the exact baseline commit SHA.
6. Confirm:
   - Sections 1.1, 1.2, and 1.3 are `drafted_and_verified`;
   - Sections 1.3.1--1.3.4 are present and verified;
   - the title and label for Section 1.4 already exist;
   - the body between `\label{sec:intro-contributions}` and the Section 1.5 command is empty;
   - the body of Section 1.5 is empty.
7. Save byte-for-byte hashes of:
   - all text before the Section 1.4 label;
   - the existing Section 1.4 title and label;
   - the empty body of Section 1.5.
8. Confirm `qa/chapter_status.csv` records:
   - `1.3` and `1.3.1`--`1.3.4` as `drafted_and_verified`;
   - `1.4` as `queued`;
   - `1.5` as `not_started`.
9. Confirm `evidence/claims.csv` ends the Chapter 1 sequence at `C1-107`.
10. Confirm that the English terminology keys added by the four Section 1.3 tasks are present and unique.
11. Confirm the three verified self-paper keys listed above exist in `bibliography/references.bib`, with no duplicate key, DOI, or normalized title.
12. Confirm no active FedSubMerge self-citation key exists unless a verified record was independently added to the repository before this task. If such a record now exists, report it but do not add a citation to the approved prose.
13. Confirm `config/build_flags.tex` contains `\thesisbibliographytrue`.
14. Confirm all four primary source files exist and are readable. For the FedSubMerge path, preserve the leading space in the directory name after `sources/fedsubmerge/`.
15. Record the session-start `sources/` file count and deterministic SHA-256 fingerprint.

Stop rather than combining tasks if Section 1.3 is incomplete or the source files cannot be read.

## Step 1: read and cross-check the four source studies

Before editing the thesis, locate and record the source passages supporting the following points.

### 1.1 ZScribbleSeg

Confirm:

- the two efficient-scribble considerations concerning effective annotation proportion and spatial randomness;
- supervision augmentation through the source-described mixing and occlusion operations;
- the global consistency constraint;
- EM-based class-mixture-ratio estimation;
- spatial-prior and shape-regularization components;
- the reported validation scope across multiple 2D and 3D medical image segmentation tasks.

### 1.2 Continual segmentation benchmark

Confirm:

- the definitions and intended roles of Domain-CL, Class-CL, and Organ-CL;
- the unified comparison of regularization, replay, and parameter-isolation families;
- evaluation of general performance, stability, plasticity, forward generalizability, parameter efficiency, and replay burden;
- the exact meanings of RMA and E-FWT;
- the distinction between metric naming and the thesis terminology for forward generalization.

### 1.3 SAMCL

Confirm:

- the centralized sequential registration setting;
- limited experience replay and meta-continual learning;
- incorporation of sharpness-aware minimization into the meta-continual process;
- the intended link between neighborhood robustness and cross-task generalization;
- the four source-reported registration task types;
- the paper’s cautious “initial attempt” scope.

### 1.4 FedSubMerge

Confirm against the current source version:

- the replay-free federated continual classification setting;
- the current receive--project--update--merge cycle;
- low-rank principal gradient subspace construction and server-side merging;
- uniform FedSubMerge and adaptive layer-wise FedSubMerge-AD;
- local orthogonal-complement gradient projection;
- the first-order analysis scope;
- the reported label-distribution, quantity, and multi-center feature heterogeneity settings;
- the explicit statement that PGS exchange is not a formal privacy guarantee.

If the current source conflicts with any approved sentence below, stop and report the exact conflict instead of silently rewriting the approved prose.

## Step 2: integrate the approved Section 1.4 draft exactly

Preserve the existing title and label:

```latex
\section{本文主要研究内容与创新点}
\label{sec:intro-contributions}
```

Insert the following text immediately after the label and before Section 1.5:

```latex
本文以医学影像学习中的任务持续演化与训练信息受限为总体问题，围绕标注获取、历史数据访问和跨中心共享三类限制开展研究。四项工作分别对应涂鸦监督医学图像分割、持续医学图像分割的场景定义与综合评测、有限回放下的持续医学图像配准，以及无回放联邦持续医学图像分类。第三章研究静态稀疏监督条件下如何充分利用有限标注；第四至第六章依次研究持续分割问题如何定义和评价、集中式顺序配准如何兼顾知识保持与跨任务泛化，以及联邦环境如何保护分散于不同中心的历史知识。本文的主要研究内容与创新点如下。

\textbf{（1）提出基于监督增强与先验正则化的涂鸦监督医学图像分割框架。}
针对涂鸦监督像素覆盖不足、标注类别比例偏差以及结构信息缺失，本文分析有效标注比例和空间随机性对涂鸦监督的影响，并据此设计监督增强策略。该策略通过混合与遮挡增加可参与训练的监督信息，利用全局一致性约束相关输入与预测之间的对应关系。在此基础上，本文采用期望最大化算法估计类别混合比例，结合空间能量构建空间先验损失，并引入形状正则化以缓解欠分割和结构碎片化。上述机制被统一到 ZScribbleSeg 框架中，使有限涂鸦既提供局部像素监督，也参与全局类别分布与结构约束，并在多种二维和三维医学图像分割任务上进行验证。该研究的主要创新在于将高效涂鸦建模、监督覆盖扩展和先验引导校正纳入同一弱监督分割框架。

\textbf{（2）建立持续医学图像分割的场景定义与综合评测框架。}
针对既有研究中场景名称、任务协议和评价维度不统一的问题，本文从输入分布、标签空间和分割对象的变化出发，将第四章基准组织为 Domain-CL、Class-CL 和 Organ-CL 三类场景，分别研究顺序跨中心域变化、新增解剖结构和跨器官分割任务。这三类名称服务于本研究的基准组织，不作为穷尽医学持续学习问题的统一分类。在一致的任务定义、数据划分和评价协议下，本文比较正则化、回放与参数隔离等代表性路线，并建立覆盖总体性能、稳定性、当前任务可塑性、前向泛化、参数效率和回放负担的评价体系。进一步地，本文提出受限建模能力（RMA），以持续约束下的当前任务性能相对于独立训练参考的比例衡量可塑性；提出扩展前向迁移（E-FWT）指标，在 Domain-CL 中汇总模型对多个尚未参与优化域的直接表现，用于评价前向泛化。该研究的创新在于把场景定义、协议统一和多维能力评价结合起来，使持续分割方法的比较不再由单一最终性能或遗忘指标决定。

\textbf{（3）提出基于锐度感知元持续学习的顺序医学图像配准方法。}
面向不同解剖区域与模态组合的配准任务顺序到达，本文将医学图像配准表述为允许有限经验回放的集中式持续学习问题，并研究单一配准网络如何累积不同任务的空间匹配能力。SAMCL 在元持续学习过程中联合使用当前任务图像对与记忆缓冲区中的历史样本，通过元更新协调当前任务学习和历史任务保持。针对非凸配准目标中局部解跨任务泛化不足的问题，本文将锐度感知最小化嵌入元持续学习过程，使优化不仅降低当前参数处的配准损失，还约束其邻域内的较大损失，从而寻求对参数扰动更不敏感的解。该方法把有限回放下的知识保持与跨任务泛化纳入同一训练框架，并在脑部 MR、腹部 CT、肺部 CT 和腹部 MR--CT 等三维配准任务上进行验证。该研究为通用医学图像配准提供了顺序学习条件下的初步探索，而不把有限回放或损失景观平坦性视为已经解决全部配准变化。

\textbf{（4）提出基于梯度子空间融合的无回放联邦持续医学图像分类方法。}
针对客户端本地保护无法覆盖其他中心任务历史、而统一保护又可能压缩新任务更新空间的问题，本文将跨客户端全局灾难性遗忘作为无回放联邦持续医学图像分类的核心研究对象。FedSubMerge 在任务边界利用当前任务梯度与服务器此前返回的历史保护信息更新低秩主梯度子空间，服务器再融合各客户端更新后的子空间，并将共享保护子空间返回客户端。在后续本地训练中，客户端把选定网络层的梯度投影到返回子空间的正交补，以减少当前更新对跨中心历史知识的一阶干扰。为适应客户端任务构成和不同网络层相关性的差异，FedSubMerge-AD 根据逐层子空间距离选择相关客户端并构建客户端特定的保护子空间，避免把相关性较低的方向无差别加入约束。本文还从一阶近似角度分析子空间保留能量、相关客户端数量与稳定性—可塑性权衡之间的关系，并在标签分布偏斜、样本数量偏斜和真实多中心特征偏移条件下进行验证。该框架在标准模型更新之外交换低秩子空间基与奇异值，不重新调用历史原始样本；这一设计减少了对回放数据的依赖，但不构成形式化隐私保证。

四项研究共享任务持续演化与训练信息受限的总体背景，但研究对象和数据访问条件并不相同。第三章解决静态稀疏监督中的信息利用问题，第四章提供持续分割的场景与评价基础，第五章研究有限回放下的集中式持续配准，第六章研究无回放联邦环境中的跨中心历史知识保护。上述边界用于保证后续各章分别在相应的任务变化、历史访问和协作条件下展开论证，而不把四项工作表述为同一方法的连续扩展。
```

After insertion, verify:

- all content before the Section 1.4 label is byte-for-byte unchanged;
- the Section 1.4 title and label remain unique;
- Section 1.5 remains body-empty;
- no `\cite`, formula, table, figure, experiment number, performance ranking, or detailed hyperparameter has been introduced in Section 1.4;
- ZScribbleSeg is not characterized as continual learning;
- Chapter 4 is not characterized as a new anti-forgetting algorithm;
- RMA and E-FWT are described consistently with the source paper;
- SAMCL remains centralized and limited-replay;
- FedSubMerge remains replay-free federated medical image classification;
- the FedSubMerge update cycle and privacy boundary match the current source;
- the final paragraph preserves the four works’ non-sequential scientific relationship.

## Step 3: bibliography verification

Do not add, delete, or modify a bibliography record.

Verify:

- `zhang2026zscribbleseg`, `wang2026benchmark`, and `wang2024samcl` exist exactly once;
- their DOI or arXiv metadata remain unchanged;
- no duplicate key, DOI, or normalized title is introduced;
- no unverified FedSubMerge self-reference is created;
- Section 1.4 contains no active citation command;
- `config/build_flags.tex` remains `\thesisbibliographytrue`.

## Step 4: append evidence records

Append the following rows to `evidence/claims.csv` after verifying that the IDs are absent:

```csv
C1-108,1,1.4,本文四项研究分别对应静态涂鸦监督分割持续分割基准有限回放持续配准和无回放联邦持续分类,THESIS_CONTRACT.md;SOURCE_MAP.md,Four-work positioning and chapter mapping,,author_synthesis,confirmed,drafted,用于保持第三至六章研究边界而非建立虚构方法依赖
C1-109,1,1.4,高效涂鸦建模同时考虑有效标注比例和标注位置的空间随机性,sources/zscribble/Zscribble_MEDIA_arxiv/main_clean_new.tex,Introduction motivation and contributions,zhang2026zscribbleseg,method,confirmed,drafted,第三章工作不表述为持续学习
C1-110,1,1.4,ZScribbleSeg通过混合遮挡和全局一致性实施监督增强,sources/zscribble/Zscribble_MEDIA_arxiv/main_clean_new.tex,Method overview and supervision augmentation sections,zhang2026zscribbleseg,method,confirmed,drafted,用于扩展可靠监督覆盖而不宣称密集标签等价
C1-111,1,1.4,ZScribbleSeg利用期望最大化估计类别混合比例并结合空间先验和形状正则化校正预测,sources/zscribble/Zscribble_MEDIA_arxiv/main_clean_new.tex,Prior-guided correction sections,zhang2026zscribbleseg,method,confirmed,drafted,不声称固定先验对所有目标普遍有效
C1-112,1,1.4,ZScribbleSeg将监督增强与先验校正统一并在多种二维和三维医学图像分割任务上验证,sources/zscribble/Zscribble_MEDIA_arxiv/main_clean_new.tex,Abstract introduction and experiment sections,zhang2026zscribbleseg,experiment_scope,confirmed,drafted,第一章只概括验证范围不写性能数值
C1-113,1,1.4,第四章基准将持续医学图像分割组织为Domain-CL Class-CL和Organ-CL三类研究场景,sources/benchmark/Benchmark_pa/main.tex,Introduction contributions and scenario definitions,wang2026benchmark,benchmark,confirmed,drafted,三类名称服务于本研究而非宣称穷尽领域分类
C1-114,1,1.4,第四章评价总体性能稳定性可塑性前向泛化参数效率和回放负担并以RMA衡量受限条件下的新任务学习能力,sources/benchmark/Benchmark_pa/main.tex,Introduction contributions and evaluation metrics,wang2026benchmark,benchmark,confirmed,drafted,RMA以独立训练参考限定可塑性解释
C1-115,1,1.4,E-FWT在Domain-CL中汇总模型对多个尚未训练域的直接表现并用于评价前向泛化,sources/benchmark/Benchmark_pa/main.tex,Generalizability metric definition,wang2026benchmark,benchmark,confirmed,drafted,保留指标原名并与前向迁移的一般概念区分
C1-116,1,1.4,统一任务定义数据划分和评价协议能够揭示正则化回放与参数隔离路线的多维取舍,sources/benchmark/Benchmark_pa/main.tex,Benchmark protocol results and discussion,wang2026benchmark,author_synthesis,confirmed,drafted,第四章是系统性实证研究而不是单一抗遗忘算法
C1-117,1,1.4,SAMCL在集中式顺序配准中结合有限经验回放与元持续学习协调当前和历史任务更新,sources/samcl/MICCAI 2024: Toward Universal Medical Image Registration/Paper-0150.tex,Introduction method and Algorithm 1,wang2024samcl,method,confirmed,drafted,有限回放不等同完整联合训练
C1-118,1,1.4,SAMCL把锐度感知最小化嵌入元持续学习以寻求对参数扰动更不敏感的配准解,sources/samcl/MICCAI 2024: Toward Universal Medical Image Registration/Paper-0150.tex,Method and generalization study,wang2024samcl,method,confirmed,drafted,损失景观平坦性不单独保证通用注册
C1-119,1,1.4,SAMCL在脑部MR腹部CT肺部CT和腹部MR-CT三维配准任务上验证知识保持与泛化,sources/samcl/MICCAI 2024: Toward Universal Medical Image Registration/Paper-0150.tex,Materials comparison and generalization study,wang2024samcl,experiment_scope,confirmed,drafted,表述为顺序学习条件下的初步探索
C1-120,1,1.4,FedSubMerge在任务边界结合服务器返回历史与当前梯度更新客户端主梯度子空间并由服务器融合,sources/fedsubmerge/ Subspace Merging for Replay-Free Federated Continual Medical Image Classification 720/FedSubMerge_main_no_appendix.tex,Introduction contributions and method overview,,method,confirmed,drafted,遵守当前receive-project-update-merge逻辑
C1-121,1,1.4,FedSubMerge在本地训练中执行正交补梯度投影以降低当前更新对跨客户端历史的一阶干扰,sources/fedsubmerge/ Subspace Merging for Replay-Free Federated Continual Medical Image Classification 720/FedSubMerge_main_no_appendix.tex,Projected local training and first-order analysis,,method,confirmed,drafted,不创建缺少核实元数据的FedSubMerge自引条目
C1-122,1,1.4,FedSubMerge-AD依据逐层子空间距离选择相关客户端并构建客户端特定保护子空间,sources/fedsubmerge/ Subspace Merging for Replay-Free Federated Continual Medical Image Classification 720/FedSubMerge_main_no_appendix.tex,Adaptive layer-wise merging method,,method,confirmed,drafted,用于降低无差别全局保护造成的过度约束
C1-123,1,1.4,FedSubMerge从一阶近似分析保护强度与可塑性并在标签分布样本数量和多中心特征异质性条件下验证,sources/fedsubmerge/ Subspace Merging for Replay-Free Federated Continual Medical Image Classification 720/FedSubMerge_main_no_appendix.tex,Theory experiments and discussion,,author_synthesis,confirmed,drafted,当前实证范围限于医学图像分类
C1-124,1,1.4,FedSubMerge不调用历史原始样本但低秩梯度子空间交换不构成形式化隐私保证,sources/fedsubmerge/ Subspace Merging for Replay-Free Federated Continual Medical Image Classification 720/FedSubMerge_main_no_appendix.tex,Replay-free setting and privacy scope,,author_definition,confirmed,drafted,区分原始数据不传输与形式化隐私保护
```

Preserve the existing header and exact 11-column schema. Validate with Python’s standard-library CSV parser:

- every row has exactly 11 columns;
- IDs `C1-108`--`C1-124` occur exactly once;
- no existing evidence row is changed;
- every non-empty citation key exists in the active bibliography;
- empty citation-key fields for FedSubMerge remain empty rather than being filled with invented metadata.

Do not normalize or rewrite pre-existing mixed line endings merely to satisfy a different CSV implementation.

## Step 5: terminology and section status

### 5.1 Add terminology rows

Add the following non-duplicate rows to `qa/terminology.csv`:

```csv
spatial randomness,空间随机性,第一章与第三章,空间分布随机性（可作解释）,稀疏涂鸦在目标区域内分散覆盖而非集中于少量位置的程度
restricted modeling ability,受限建模能力,第一章与第四章,受限学习能力（避免混用）,RMA；比较持续约束下当前任务表现与独立训练参考以衡量可塑性
extended forward transfer,扩展前向迁移,第一章与第四章,扩展前向泛化（不是指标原名）,E-FWT；在Domain-CL中汇总多个尚未训练域上的直接表现并用于评价前向泛化
orthogonal-complement projection,正交补投影,第一章与第六章,正交投影（范围不完全等同）,移除梯度在保护子空间内的分量并保留其正交补分量
first-order interference,一阶干扰,第一章与第六章,一级干扰（错误）,一阶近似下当前参数更新对历史任务损失的影响
```

Validate with a CSV parser:

- exactly 5 columns per row;
- unique English-term keys;
- no existing preferred Chinese term, scope, avoid-field, or note is changed.

### 5.2 Update `qa/chapter_status.csv`

Set:

- `1.1`, `1.2`, and `1.3` → preserve existing verified state;
- `1.3.1`--`1.3.4` → preserve `drafted_and_verified`;
- `1.4` → `drafted_and_verified`, artifact `chapters/ch01_introduction.tex`;
- `1.5` → `queued`.

Preserve the existing four-column schema and all unrelated rows.

### 5.3 Update `STATE.md`

Keep the update concise. Record:

- Sections 1.1--1.3 remain complete and unchanged;
- Section 1.4 is integrated and verified;
- the four works’ boundaries were checked against their original source files;
- no new bibliography entry or active Section 1.4 citation was introduced;
- Section 1.5 remains body-empty;
- the next target is 1.5 “论文组织结构”;
- the fast verification/build result and any new warning;
- `sources/` remained read-only, outside the diff, and fingerprint-identical.

Do not rebuild `handoff/CONTEXT_PACKET_FOR_GPT.md`.

## Step 6: fast verification

Run exactly:

```bash
bash scripts/verify_fast_section.sh --quiet chapters/ch01_introduction.tex
```

The command’s complete build and changed-text checks must succeed. Review its summary and additionally verify:

1. all active citations in the thesis resolve;
2. no undefined citation or cross-reference;
3. no duplicate label;
4. no missing input, class, figure, table, bibliography, or other required file;
5. no new `TODO`, `TBD`, or `??`;
6. no duplicate BibTeX key, DOI, or normalized title;
7. `git diff --check` passes;
8. claims CSV has 11 columns and unique IDs;
9. terminology CSV has 5 columns and unique English keys;
10. all preserved baseline hashes match;
11. no body text was added outside Section 1.4;
12. Section 1.5 remains body-empty;
13. the approved text contains no active citation command;
14. no unverified FedSubMerge bibliographic metadata was introduced;
15. the four scientific boundaries in the strict rules are satisfied;
16. `sources/` is absent from `git diff`;
17. the session-end `sources/` file count and deterministic fingerprint match the session-start snapshot;
18. no new layout warning is introduced by this pure-text change.

Do not perform routine manual PDF inspection. If the build reports a new overfull box, abnormal page break, missing content, or another layout anomaly attributable to Section 1.4, inspect only the affected pages and report the result.

## Step 7: concise handoff report

Replace `handoff/LATEST_CODEX_REPORT.md` with a concise report containing:

- task name and timestamp;
- baseline SHA and preflight result;
- exact changed files;
- confirmation that the approved Section 1.4 prose was integrated exactly;
- confirmation that Sections 1.1--1.3 were preserved and Section 1.5 remains empty;
- source cross-check result for all four studies;
- confirmation that no new bibliography entry or Section 1.4 citation was added;
- evidence and terminology additions;
- chapter-status and state changes;
- fast verification command and result;
- citation/reference/label/file/CSV status;
- changed-text author-voice and reference-overlap result;
- `sources/` unchanged result;
- unresolved scientific, source, build, or layout issues;
- next target Section 1.5 and confirmation it was not drafted.

The content commit must include this handoff report. Do not create a later report-only commit merely to store the Overleaf SHA.

## Step 8: commit, push, and synchronize

After successful verification:

```bash
git diff --check
git status --short
```

Stage only permitted files and create one content commit, for example:

```bash
git commit -m "Draft Chapter 1 Section 1.4"
git push origin main
```

Verify that the content commit exists on `origin/main` and the worktree is clean. Within 30 minutes of the verified build, run:

```bash
bash scripts/sync_latex_to_overleaf.sh --skip-local-build "Sync Chapter 1 Section 1.4"
```

Record the GitHub content SHA and Overleaf deployment SHA in the final terminal response. Do not make a second GitHub commit solely for the deployment receipt.

Final checks:

```bash
git status --short
git rev-parse HEAD
git rev-parse origin/main
```

Local `HEAD` must equal `origin/main`. No force-push is allowed.

## Definition of done

This task is complete only when:

- all four original source studies have been read and cross-checked;
- the approved Section 1.4 prose is integrated exactly;
- Sections 1.1--1.3 are byte-for-byte unchanged;
- Section 1.5 remains body-empty;
- the four studies’ task and data-access boundaries remain correct;
- ZScribbleSeg is not described as continual learning;
- Chapter 4 remains a benchmark and evaluation study rather than an algorithm claim;
- SAMCL remains centralized and limited-replay;
- FedSubMerge remains replay-free federated medical image classification and is not described as formally private;
- no formula, figure, table, detailed result, or unverified self-citation is introduced;
- no bibliography entry is modified or added;
- `C1-108`--`C1-124` occur exactly once;
- the five terminology rows are valid and unique;
- Section 1.4 is `drafted_and_verified` and Section 1.5 is `queued`;
- fast verification succeeds;
- `sources/` is unchanged;
- the verified content is pushed to GitHub;
- the LaTeX subset is synchronized to Overleaf or an exact non-bypassed failure is reported;
- the worktree is clean;
- Section 1.5 is not drafted.

Do not continue beyond Section 1.4.
