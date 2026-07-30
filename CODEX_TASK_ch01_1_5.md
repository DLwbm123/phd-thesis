# Codex Task: integrate Chapter 1, Section 1.5 and complete the Chapter 1 milestone

Read and obey `AGENTS.md`, `WORKFLOW_MODES.md`, `THESIS_CONTRACT.md`,
`AUTHORSHIP_PROTOCOL.md`, `AUTHOR_VOICE.md`, `STATE.md`,
`PROJECT_CONFIG.md`, `SOURCE_MAP.md`, `chapter_cards/ch01.md`,
and `chapter_cards/ch02.md` before editing.

Also read the chapter cards for Chapters 3--7 and the actual chapter entry files:

- `chapter_cards/ch03.md`
- `chapter_cards/ch04.md`
- `chapter_cards/ch05.md`
- `chapter_cards/ch06.md`
- `chapter_cards/ch07.md`
- `main.tex`
- `chapters/ch02_foundations.tex`
- `chapters/ch03_zscribble.tex`
- `chapters/ch04_benchmark.tex`
- `chapters/ch05_samcl.tex`
- `chapters/ch06_fedsubmerge.tex`
- `chapters/ch07_conclusion.tex`

## Workflow mode

This task completes Chapter 1. Use **Mode B: chapter milestone audit** in
`WORKFLOW_MODES.md`.

After integrating Section 1.5 and updating the evidence and status files, run:

```bash
bash scripts/build_and_audit.sh
```

This milestone must also include:

- complete Chapter 1 citation--bibliography--evidence consistency checking;
- complete CSV integrity and uniqueness checking;
- full visual inspection of every PDF page containing Chapter 1, together
  with the updated table-of-contents pages and bibliography pages;
- before/after file count and deterministic SHA-256 verification for all
  files under `sources/`;
- rebuilding `handoff/CONTEXT_PACKET_FOR_GPT.md` for the next target,
  Chapter 2, Section 2.1.1;
- review of all previously recorded non-fatal Chapter 1 warnings.

Do not use the fast-section script as a substitute for the chapter milestone
audit. A diagnostic command may be run if the milestone script fails.

After the verified Chapter 1 content commit is pushed and the worktree is clean,
synchronize the compilable LaTeX subset with:

```bash
bash scripts/sync_latex_to_overleaf.sh "Sync completed Chapter 1"
```

Because this is a chapter milestone, record the verified GitHub content commit
and Overleaf deployment commit in the long-term handoff and state files. If
recording those deployment identifiers creates a GitHub-only change, make one
report-only commit and push it. Do not synchronize Overleaf again for that
report-only commit.

## Goal

Integrate the GPT Pro-approved draft for Section 1.5 “论文组织结构”, complete
the first full draft of Chapter 1, and perform the mandatory Chapter 1 milestone
audit.

Section 1.5 must describe what each of the seven chapters does and how the
chapters relate. It must remain an organizational roadmap rather than a second
innovation summary. The descriptions must match the current thesis contract,
chapter cards, `main.tex` include order, and actual chapter titles.

Stop after Chapter 1 is completed and verified. Do not draft Chapter 2 prose.

## Source and authorship policy

Section 1.5 is an author-created structural description. Its factual basis is:

- `THESIS_CONTRACT.md`;
- `main.tex`;
- `chapter_cards/ch01.md` through `chapter_cards/ch07.md`;
- the chapter headings already present in `chapters/ch02_foundations.tex`
  through `chapters/ch07_conclusion.tex`.

Do not use a survey, external thesis, or reference dissertation as the source
of the organization text. Do not copy, translate, or closely paraphrase any
content from `sources/reference_thesis/`.

The approved text contains no citation commands. Do not add citations.

## Strict scientific boundaries

### Overall

- Do not imply that Chapters 3--6 are four stages of one algorithm.
- Do not claim that a later method technically extends an earlier one unless
  the original source explicitly establishes that relation.
- Do not repeat the complete contribution list from Section 1.4.
- Do not introduce formulas, figures, tables, experimental numbers,
  comparative rankings, or new scientific claims.
- Do not describe planned but unverified work as already completed beyond the
  scope recorded in the chapter cards and source studies.
- Do not claim clinical deployment, universal applicability, or regulatory
  approval.

### Chapter-specific

- Chapter 2 provides shared theory and technical foundations; it does not
  replace the literature review in Section 1.2 or disclose the later chapters'
  innovations in advance.
- Chapter 3 is weakly supervised and annotation-efficient medical image
  segmentation, not continual learning.
- Chapter 4 is scenario definition, evaluation design, and systematic empirical
  study, not a single anti-forgetting algorithm.
- Chapter 5 is centralized continual medical image registration with limited
  experience replay, not replay-free or federated learning.
- Chapter 6 is replay-free federated continual medical image classification;
  it does not provide a formal privacy guarantee.
- Chapter 7 summarizes conclusions, limitations, and future directions; it
  must not convert unverified future combinations into completed contributions.

## Strict file scope

Files that may be modified or added:

- `CODEX_TASK_ch01_1_5.md`
- `chapters/ch01_introduction.tex`
- `evidence/claims.csv`
- `qa/chapter_status.csv`
- `qa/style_audit_report.md`
- `qa/reference_overlap_report.md`
- `STATE.md`
- `handoff/LATEST_CODEX_REPORT.md`
- `handoff/CONTEXT_PACKET_FOR_GPT.md`

Read-only verification targets:

- `bibliography/references.bib`
- `qa/terminology.csv`
- `qa/notation.csv`
- `config/build_flags.tex`
- `main.tex`
- all chapter cards
- all Chapter 2--7 `.tex` files
- all files under `sources/`

Do not modify another chapter, template/class file, bibliography record,
bibliography style, build script, figure, table, or source file.

Except for a strictly necessary LaTeX syntax correction, integrate the approved
Section 1.5 text exactly. Do not freely rewrite Sections 1.1--1.4.

## Step 0: repository and baseline preflight

1. Run:

   ```bash
   git status --short
   git branch --show-current
   git fetch origin
   ```

2. The worktree must be clean except that `CODEX_TASK_ch01_1_5.md` may be
   the only untracked file.
3. Confirm the current branch is `main`.
4. Confirm local `HEAD` is not behind or divergent from `origin/main`.
   - If the remote is ahead and the worktree is otherwise clean, use
     `git pull --ff-only origin main`.
   - Stop on divergence, conflict, or unrelated local changes.
   - Do not reset, rebase, overwrite, or force-push.
5. Record the exact baseline commit SHA.
6. Confirm:
   - Sections 1.1, 1.2, 1.3, and 1.4 are all
     `drafted_and_verified`;
   - the full approved body of Section 1.4 is present;
   - the title and label of Section 1.5 already exist;
   - the body after `\label{sec:intro-organization}` is empty.
7. Save byte-for-byte hashes of:
   - all Chapter 1 content before the Section 1.5 label;
   - the existing Section 1.5 title and label.
8. Confirm `qa/chapter_status.csv` records:
   - `1.4` as `drafted_and_verified`;
   - `1.5` as `queued`;
   - Chapter 2 as `not_started` or an equivalent pre-writing state.
9. Confirm `evidence/claims.csv` contains `C1-108` through `C1-124`
   exactly once and that the next unused Chapter 1 claim ID is `C1-125`.
10. Confirm all active thesis citations currently resolve and record the actual
    number of distinct active citation keys.
11. Confirm no bibliography change is required and that
    `config/build_flags.tex` still contains:

    ```latex
    \thesisbibliographytrue
    ```

12. Confirm the chapter titles and include order in `main.tex` agree with
    `THESIS_CONTRACT.md` and the chapter cards.
13. Record the session-start count and deterministic SHA-256 fingerprint of
    every file under `sources/`.

If Section 1.4 has not yet been integrated and verified, stop. Do not execute
Sections 1.4 and 1.5 together.

## Step 1: cross-check the seven-chapter organization

Before editing Section 1.5, verify the following structure.

1. **Chapter 1 — 绪论**
   - research background and significance;
   - domestic and international research status;
   - key problems and technical challenges;
   - main research content and innovations;
   - thesis organization.

2. **Chapter 2 — 医学影像学习相关理论与关键技术**
   - medical image segmentation, registration, and classification;
   - weak supervision and annotation-efficient learning;
   - continual learning;
   - federated and federated continual learning;
   - meta-learning, sharpness-aware minimization, gradient subspaces,
     and orthogonal projection.

3. **Chapter 3 — 基于监督增强与先验正则化的涂鸦监督医学图像分割研究**
   - ZScribbleSeg;
   - efficient scribble principles;
   - supervision augmentation and global consistency;
   - class-mixture estimation, spatial prior, and shape regularization;
   - experiments and analysis for 2D and 3D medical segmentation.

4. **Chapter 4 — 持续医学影像分割的场景定义与综合评测研究**
   - Domain-CL, Class-CL, and Organ-CL as this benchmark's named
     scenarios;
   - unified task protocols and multidimensional evaluation;
   - systematic comparison and research implications.

5. **Chapter 5 — 基于锐度感知元持续学习的医学影像配准研究**
   - centralized sequential registration;
   - limited experience replay;
   - meta-continual learning and sharpness-aware optimization;
   - knowledge retention and cross-task generalization.

6. **Chapter 6 — 基于梯度子空间融合的无回放联邦持续医学影像分类研究**
   - replay-free federated continual classification;
   - principal gradient subspaces;
   - server-side uniform and adaptive layer-wise subspace fusion;
   - orthogonal-complement projected local training;
   - global history protection under client heterogeneity.

7. **Chapter 7 — 总结与展望**
   - summary and main conclusions;
   - limitations;
   - future directions.

If a current chapter card or actual chapter title conflicts with this approved
organization, stop and report the exact conflict rather than silently editing
the approved prose.

## Step 2: integrate the approved Section 1.5 text exactly

Preserve the existing title and label:

```latex
\section{论文组织结构}
\label{sec:intro-organization}
```

Insert the following approved text immediately after that label:

```latex
全文共分为七章，各章内容安排如下。

第一章为绪论。首先说明医学影像智能分析的临床功能及其对训练数据和监督信息的依赖，从标注获取、历史数据访问和跨医疗中心共享三个维度分析训练信息受限问题，并讨论数据分布与医学任务的持续演化。随后，围绕标注高效与弱监督医学图像分割、医学影像持续学习和联邦持续医学影像学习梳理国内外研究现状，归纳本文需要解决的四项关键技术挑战。在此基础上，概括本文的主要研究内容与创新点，并说明全文的章节安排。

第二章介绍医学影像学习相关理论与关键技术。该章首先给出医学图像分割、配准和分类三类任务的基本概念与建模目标，继而介绍弱监督标注形式、涂鸦监督分割、一致性正则化和先验约束。对于后续持续学习研究，该章说明持续学习的问题定义、灾难性遗忘、稳定性—可塑性权衡、正则化、回放和参数隔离等基础策略，并进一步介绍联邦学习、客户端异质性和联邦持续学习。最后，对元学习、锐度感知最小化、梯度子空间建模和正交投影等后续章节使用的关键技术进行说明。

第三章研究基于监督增强与先验正则化的涂鸦监督医学图像分割。该章分析涂鸦覆盖不足、标注类别比例偏差和结构信息缺失对分割结果的影响，介绍 ZScribbleSeg 的总体框架以及高效涂鸦原则、监督增强、全局一致性、类别混合比例估计、空间先验和形状正则化。在此基础上，给出整体优化与训练流程，并通过二维和三维医学图像分割实验分析各组成部分的作用及方法的适用范围。

第四章研究持续医学图像分割的场景定义与综合评测。该章围绕顺序跨中心域变化、新增分割结构和跨器官任务，构建 Domain-CL、Class-CL 和 Organ-CL 三类基准场景，并统一任务序列、数据划分和测试协议。随后，从总体性能、知识保持、当前任务可塑性、前向泛化、参数效率和回放负担等维度建立评价体系，对代表性持续学习方法开展系统比较，并分析不同方法路线在场景和资源条件变化下的能力取舍。

第五章研究基于锐度感知元持续学习的医学图像配准。该章将多解剖区域和多模态配准任务组织为允许有限经验回放的集中式顺序学习问题，介绍 SAMCL 的总体框架、经验回放驱动的元持续学习过程以及锐度感知优化机制。实验部分分别考察模型的综合配准性能、历史任务保持和未见任务泛化，并分析有限回放、元学习和损失景观约束的作用边界。

第六章研究基于梯度子空间融合的无回放联邦持续医学图像分类。该章在多医疗中心原始数据不集中、客户端任务序列异质且历史原始样本不回放的条件下，介绍主梯度子空间构建、服务器端统一子空间融合、自适应逐层子空间融合以及正交补投影式本地训练。随后，从综合性能、异质性、客户端参与、超参数和资源开销等方面分析方法在跨客户端历史知识保护与当前任务学习之间的取舍。该章讨论的是协同优化和知识保护机制，不把子空间交换表述为形式化隐私保证。

第七章总结全文工作，归纳各项研究的主要结论与适用条件，分析仍然存在的局限，并围绕稀疏监督与持续学习结合、任务无关和开放世界学习、医学基础模型的持续适配，以及安全联邦持续学习等方向讨论后续研究。
```

After insertion, verify:

- all content before the Section 1.5 label is byte-for-byte unchanged;
- the Section 1.5 title and label remain unique;
- the approved text contains exactly eight natural paragraphs:
  one introductory paragraph and one paragraph for each chapter;
- no citation command, formula, figure, table, experimental number, ranking,
  or new technical claim has been introduced;
- every chapter title and role matches the contract and chapter cards;
- the scientific boundaries for Chapters 3--6 remain correct;
- no prose is added to Chapter 2 or another chapter.

## Step 3: bibliography and terminology verification

Do not add, delete, or modify any bibliography record.

Verify:

- all existing active citations in Chapter 1 resolve in the active `.bib`
  and generated `.bbl`;
- no duplicate bibliography key, DOI, or normalized title exists;
- Section 1.5 contains no citation command;
- `config/build_flags.tex` remains `\thesisbibliographytrue`.

Do not add or modify a row in `qa/terminology.csv` or `qa/notation.csv`.
Section 1.5 introduces no new technical term or symbol requiring registration.
Confirm both files remain parseable and unchanged.

## Step 4: append Chapter 1 organization evidence records

Append the following rows to `evidence/claims.csv` after checking that the IDs
are absent:

```csv
C1-125,1,1.5,全文按照绪论理论基础四项研究章节和总结展望组织为七章,THESIS_CONTRACT.md;main.tex,Seven-chapter structure and include order,,author_structure,confirmed,drafted,用于说明论文整体结构而不引入新的科学结论
C1-126,1,1.5,第一章依次完成研究背景研究现状关键挑战主要内容创新点和论文组织结构,chapter_cards/ch01.md;chapters/ch01_introduction.tex,Chapter 1 structure and completed headings,,author_structure,confirmed,drafted,概括绪论功能
C1-127,1,1.5,第二章提供医学影像任务弱监督持续学习联邦学习及关键优化方法的理论基础,chapter_cards/ch02.md;chapters/ch02_foundations.tex,Chapter 2 card and heading skeleton,,author_structure,confirmed,drafted,不重复第一章研究现状且不提前泄露方法创新
C1-128,1,1.5,第三章研究监督增强与先验正则化的涂鸦监督医学图像分割,chapter_cards/ch03.md;chapters/ch03_zscribble.tex,Chapter 3 card and chapter title,,author_structure,confirmed,drafted,第三章不属于持续学习
C1-129,1,1.5,第四章研究持续医学图像分割场景定义多维评价和系统性实证比较,chapter_cards/ch04.md;chapters/ch04_benchmark.tex,Chapter 4 card and chapter title,,author_structure,confirmed,drafted,第四章不是单一抗遗忘算法
C1-130,1,1.5,第五章研究有限回放条件下的锐度感知元持续医学图像配准,chapter_cards/ch05.md;chapters/ch05_samcl.tex,Chapter 5 card and chapter title,,author_structure,confirmed,drafted,保持集中式有限回放边界
C1-131,1,1.5,第六章研究无回放联邦持续医学图像分类中的梯度子空间融合与跨中心知识保护,chapter_cards/ch06.md;chapters/ch06_fedsubmerge.tex,Chapter 6 card and chapter title,,author_structure,confirmed,drafted,不声称形式化隐私保证
C1-132,1,1.5,第七章总结主要结论适用条件局限性并讨论未来研究方向,chapter_cards/ch07.md;chapters/ch07_conclusion.tex,Chapter 7 card and chapter title,,author_structure,confirmed,drafted,未来方向不得写成已完成贡献
```

Preserve the existing header and exact 11-column schema. Validate with Python's
standard-library CSV parser:

- every row has exactly 11 columns;
- IDs `C1-125`--`C1-132` occur exactly once;
- no existing evidence row is changed;
- all claim IDs in the entire file are unique;
- the complete Chapter 1 sequence `C1-001`--`C1-132` is present exactly once;
- empty citation-key fields remain empty.

Do not normalize or rewrite pre-existing mixed line endings merely to satisfy a
different CSV implementation.

## Step 5: update chapter status and state

### 5.1 Update `qa/chapter_status.csv`

Set:

- add `1,绪论,drafted_and_verified,chapters/ch01_introduction.tex`
  if a Chapter 1 aggregate row does not already exist;
- `1.1` → preserve `drafted_and_verified`;
- `1.2` → preserve `drafted_and_verified`;
- `1.3` → preserve `drafted_and_verified`;
- `1.4` → preserve `drafted_and_verified`;
- `1.5` → `drafted_and_verified`,
  artifact `chapters/ch01_introduction.tex`;
- `2` → `queued`, artifact empty.

Preserve the existing four-column schema and all unrelated rows.

### 5.2 Update `STATE.md`

Record concisely but completely:

- Chapter 1 is complete at the current full-draft stage;
- Sections 1.1--1.5 and all registered subsections are
  `drafted_and_verified`;
- Chapter 1 passed the milestone build, full audits, evidence/citation checks,
  and visual inspection;
- the exact PDF page count, byte size, and SHA-256;
- the exact GitHub content commit and Overleaf deployment state;
- all unresolved scientific, source, template, bibliography, and layout
  warnings;
- the next chapter is Chapter 2;
- the next writing target is
  2.1.1 “医学图像分割” under
  2.1 “医学影像智能分析任务基础”;
- no Chapter 2 prose was drafted in this task.

## Step 6: rebuild the GPT context packet for Chapter 2

Replace `handoff/CONTEXT_PACKET_FOR_GPT.md` with an up-to-date context packet
for:

```text
第二章“医学影像学习相关理论与关键技术”
→ 2.1“医学影像智能分析任务基础”
→ 2.1.1“医学图像分割”
```

The packet must include:

1. current repository and Chapter 1 completion status;
2. target subsection and neighboring headings;
3. the role of Chapter 2 as shared theoretical and technical foundation;
4. boundaries:
   - do not repeat the research-status narrative of Section 1.2;
   - do not introduce Chapter 3's ZScribbleSeg method in 2.1.1;
   - distinguish medical image from medical imaging;
   - provide technical definition, common formulation, output structure,
     and evaluation foundations for medical image segmentation;
5. current terminology conventions;
6. relevant active bibliography and evidence already available;
7. source paths that may be consulted;
8. facts or references still requiring primary-source verification;
9. the next planned subsection, 2.1.2 “医学图像配准”;
10. explicit prohibition on using the reference thesis as a content or
    language source.

The context packet is not thesis prose. Do not insert unverified claims merely
to make it complete.

## Step 7: Chapter 1 milestone build and audits

Run:

```bash
bash scripts/build_and_audit.sh
```

Then perform and report all of the following.

### 7.1 Build integrity

- full build exit code 0;
- BibTeX actually runs or is correctly reused by `latexmk`;
- no undefined citation or cross-reference;
- no duplicate LaTeX label;
- no missing input, class, figure, table, bibliography, or other required file;
- no new `TODO`, `TBD`, or `??`;
- `git diff --check` passes;
- record final PDF page count, byte size, and SHA-256.

### 7.2 Bibliography and citation consistency

- parse every active `\cite{}` key in all thesis chapters;
- verify each key exists exactly once in `bibliography/references.bib`;
- verify every active key appears in the generated `.bbl`;
- check duplicate key, DOI, and normalized title;
- verify Section 1.5 adds no citation;
- distinguish pre-existing BibTeX/template warnings from new warnings.

### 7.3 Chapter 1 evidence consistency

- validate `evidence/claims.csv` using Python's CSV parser;
- verify 11 columns for every row and globally unique claim IDs;
- verify `C1-001`--`C1-132` are present exactly once;
- verify every non-empty Chapter 1 evidence citation key exists in the active
  bibliography;
- cross-check all active Chapter 1 citation keys against the Chapter 1 evidence
  ledger;
- report any claim whose source location is missing or whose confidence/status
  is inconsistent;
- do not rewrite approved prose merely to conceal an evidence warning.

### 7.4 Terminology and notation consistency

- validate `qa/terminology.csv` with exactly 5 columns per row and unique
  English keys;
- validate `qa/notation.csv` according to its current schema;
- check Chapter 1 for inconsistent preferred terms, especially:
  - 医学影像 / 医学图像;
  - 前向迁移 / 前向泛化;
  - 有限回放 / 无回放;
  - 跨客户端全局灾难性遗忘;
  - 主梯度子空间 / 子空间融合;
- report rather than freely rewriting approved text unless the issue is a
  deterministic typo.

### 7.5 Full Chapter 1 style and overlap audits

Use the reports generated by `build_and_audit.sh`.

- report every style-rule hit in Chapter 1;
- distinguish accepted repeated technical terminology from avoidable
  mechanical phrasing;
- do not mechanically replace repeated words solely to reduce counts;
- report the full reference-thesis overlap result;
- do not paraphrase approved prose merely to hide overlap;
- confirm `sources/reference_thesis/` was used only by the audit.

### 7.6 Full visual inspection

Render and inspect:

- all table-of-contents pages affected by Chapter 1 completion;
- every physical PDF page containing Chapter 1;
- all bibliography pages.

Check:

- Chinese character rendering;
- heading hierarchy and numbering;
- paragraph breaks;
- bold numbered contribution headings in Section 1.4;
- Section 1.5 chapter-by-chapter paragraph layout;
- citation rendering in Sections 1.1--1.3;
- overfull or clipped text;
- unusual blank areas;
- page breaks around Sections 1.4 and 1.5;
- overlap, missing content, or duplicated content;
- transition from Chapter 1 to the empty Chapter 2 skeleton.

Record the exact pages inspected and the result.

### 7.7 `sources/` integrity

At the end of the milestone:

- recount every file under `sources/`;
- recompute the deterministic SHA-256 fingerprint;
- compare with the session-start snapshot;
- confirm `sources/` is absent from `git diff`;
- report any mismatch and stop before commit if a source file changed.

### 7.8 Review known warnings

Recheck and report, without unauthorized template changes:

- the `gbt7714-numerical` deprecated-style warning;
- the `ctexpatch` / `natbib` compatibility warning;
- the previously recorded `Overfull \vbox`;
- the mixed CRLF/LF line endings in `evidence/claims.csv`;
- the `empty urldate` warning associated with the benchmark arXiv entry;
- any Chapter 1 style-rule counts such as repeated “同时”;
- all warnings newly introduced by Section 1.5.

## Step 8: write the Chapter 1 milestone handoff report

Replace `handoff/LATEST_CODEX_REPORT.md` with a complete milestone report
containing:

1. task name and execution timestamp;
2. baseline commit and repository preflight;
3. exact modified and added files;
4. confirmation that the approved Section 1.5 prose was integrated exactly;
5. hash confirmation that Sections 1.1--1.4 were unchanged;
6. confirmation that no Chapter 2 prose was drafted;
7. evidence rows `C1-125`--`C1-132`;
8. chapter-status and `STATE.md` changes;
9. rebuilt Chapter 2 context packet;
10. build command, exit code, PDF pages, bytes, and SHA-256;
11. bibliography, citation, reference, label, file, and placeholder checks;
12. complete Chapter 1 evidence consistency result;
13. terminology and notation consistency result;
14. full style-audit result;
15. full reference-overlap result;
16. full visual-inspection pages and result;
17. before/after `sources/` count and fingerprint;
18. all unresolved scientific, source, bibliography, template, style, and
    layout issues;
19. confirmation that Chapter 1 is complete at the current draft stage;
20. next target 2.1.1 “医学图像分割”;
21. GitHub content commit and Overleaf deployment commit after synchronization.

## Step 9: commit, push, synchronize, and record deployment

After all content and milestone checks pass:

```bash
git diff --check
git status --short
```

Stage only the permitted files. Create a Chapter 1 content commit, for example:

```bash
git commit -m "Complete Chapter 1"
git push origin main
```

Verify that `origin/main` contains the content commit and the worktree is clean.
Then run:

```bash
bash scripts/sync_latex_to_overleaf.sh "Sync completed Chapter 1"
```

Record the exact Overleaf deployment SHA and verify the remote branch.

Update `handoff/LATEST_CODEX_REPORT.md`, `handoff/CONTEXT_PACKET_FOR_GPT.md`,
and `STATE.md` with the final GitHub and Overleaf identifiers if those values
were not known at the content-commit stage. If this produces GitHub-only
changes, create and push one report-only commit, for example:

```bash
git add handoff/LATEST_CODEX_REPORT.md handoff/CONTEXT_PACKET_FOR_GPT.md STATE.md
git commit -m "Record Chapter 1 milestone deployment"
git push origin main
```

Do not rerun the Overleaf synchronization for this report-only commit.

At the end verify:

```bash
git status --short
git rev-parse HEAD
git rev-parse origin/main
```

The worktree must be clean and local `HEAD` must equal `origin/main`.
No force-push is allowed.

If the GitHub content push fails, do not synchronize Overleaf. If Overleaf
synchronization fails, preserve the verified GitHub content commit, report the
exact error, and do not bypass the deployment checks.

## Definition of done

This task is complete only when:

- Section 1.4 was already complete before execution;
- the approved Section 1.5 text is integrated exactly;
- Sections 1.1--1.4 remain byte-for-byte unchanged;
- no Chapter 2 prose is drafted;
- the seven-chapter description matches the contract, chapter cards, and
  actual chapter titles;
- no bibliography or terminology record is modified;
- `C1-125`--`C1-132` occur exactly once;
- the complete Chapter 1 evidence sequence is valid;
- Section 1.5 and aggregate Chapter 1 status are
  `drafted_and_verified`;
- Chapter 2 is `queued`;
- the full milestone build, citation/evidence/terminology checks, style audit,
  overlap audit, and visual inspection are complete;
- the Chapter 2 context packet is rebuilt;
- `sources/` remains unchanged;
- Chapter 1 is pushed to GitHub and synchronized to Overleaf, or an exact
  non-bypassed failure is reported;
- the worktree is clean;
- the next target is 2.1.1 “医学图像分割”.

Do not continue drafting Chapter 2 in this task.
