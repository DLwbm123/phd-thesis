# Codex Task: integrate Chapter 1, Section 1.3.2

Read and obey `AGENTS.md`, `WORKFLOW_MODES.md`, `THESIS_CONTRACT.md`, `AUTHORSHIP_PROTOCOL.md`, `AUTHOR_VOICE.md`, `STATE.md`, `PROJECT_CONFIG.md`, and `chapter_cards/ch01.md` before editing.

## Workflow mode

Use **Mode A: fast subsection integration** in `WORKFLOW_MODES.md`.

Run the single required build and changed-text audits with:

```bash
bash scripts/verify_fast_section.sh --quiet chapters/ch01_introduction.tex
```

This is a pure-text subsection. Do not duplicate routine full-repository audits or manual PDF inspection. Inspect affected PDF pages only if a newly introduced build/layout warning requires it.

After the verified content commit is pushed, synchronize with:

```bash
bash scripts/sync_latex_to_overleaf.sh --skip-local-build "Sync Chapter 1 Section 1.3.2"
```

Report the remote SHA in the final response; do not create a second deployment-receipt commit.

## Goal

Integrate the GPT Pro-approved draft for Section 1.3.2 “持续分割场景和评价维度不完备”.

The subsection must synthesize 1.2.2 into the second thesis challenge: existing continual medical image segmentation studies use non-uniform scenario definitions and often evaluate only a subset of stability, plasticity, forward generalization, and resource conditions. It must motivate Chapter 4 as a scenario-definition and comprehensive-benchmark study, not as a single anti-forgetting algorithm.

Stop after 1.3.2. Do not draft 1.3.3, 1.3.4, 1.4, or 1.5.

## Evidence basis

Reuse already verified bibliography entries:

- `wang2024continualsurvey`
- `kumari2025medicalcl`
- `yuan2024continualseg`
- `gonzalez2023lifelong`
- `wang2026benchmark`

No new bibliography entry is expected. Stop if a required key is missing.

## Strict scientific boundaries

- Do not present `Domain-CL`, `Class-CL`, or `Organ-CL` as field-wide universal standards. They are named scenarios in the author’s benchmark study.
- Do not equate all cross-center datasets with domain continual learning. Sequential arrival, model updating, and retention requirements must be present.
- Do not equate external-domain generalization failure with catastrophic forgetting.
- Do not assume all continual segmentation data use partial labels or exhibit background semantic drift; this depends on the annotation protocol.
- Do not equate forward transfer with forward generalization.
- Do not claim that final average accuracy, forgetting, or backward transfer alone is sufficient.
- Do not treat joint training and methods with different replay, parameter-growth, task-ID, or historical-access conditions as directly comparable without reporting those conditions.
- Do not describe the Chapter 4 benchmark as a method that eliminates forgetting.
- Do not introduce Chapter 4 tables, formulas, numerical rankings, or experimental conclusions in detail.
- Do not modify `sources/` or import any content from `sources/reference_thesis/`.

## Strict file scope

Files that may be modified or added:

- `CODEX_TASK_ch01_1_3_2.md`
- `chapters/ch01_introduction.tex`
- `evidence/claims.csv`
- `qa/terminology.csv`
- `qa/chapter_status.csv`
- `qa/style_audit_report.md`
- `qa/reference_overlap_report.md`
- `STATE.md`
- `handoff/LATEST_CODEX_REPORT.md`

`bibliography/references.bib` and `config/build_flags.tex` are read-only verification targets. Do not modify other files.

## Step 0: repository and baseline preflight

1. Run `git status --short`, `git branch --show-current`, and `git fetch origin`.
2. Require a clean `main` worktree except the untracked task file.
3. Fast-forward only with `git pull --ff-only origin main`; stop on divergence or unrelated changes.
4. Record the baseline SHA.
5. Confirm:
   - Sections 1.1 and 1.2 are verified;
   - 1.3.1 is present and `drafted_and_verified`;
   - the 1.3.2 body is empty;
   - 1.3.3, 1.3.4, 1.4, and 1.5 remain body-empty.
6. Save byte-for-byte hashes of:
   - all text through the end of 1.3.1;
   - the empty bodies of 1.3.3--1.3.4;
   - Sections 1.4 and 1.5.
7. Confirm evidence IDs through `C1-081` and all terminology/status changes from 1.3.1.
8. Confirm all five required citation keys exist and `\thesisbibliographytrue` remains active.
9. Record the session-start `sources/` file count and deterministic SHA-256.

If 1.3.1 is incomplete, stop rather than combining tasks.

## Step 1: integrate the approved draft exactly

Preserve:

```latex
\subsection{持续分割场景和评价维度不完备}
\label{subsec:intro-challenge-benchmark}
```

Insert immediately after the label and before the title of 1.3.3:

```latex
持续医学图像分割首先面临场景定义不统一的问题。通用持续学习通常依据输入分布、标签空间和任务身份区分域增量、类增量和任务增量等设定\cite{wang2024continualsurvey}，但医学分割还涉及器官、模态、中心和标注协议的共同变化。Kumari 等的综述表明，同一医学数据序列可能因输出空间、测试时上下文和阶段划分不同而被赋予不同场景名称\cite{kumari2025medicalcl}。若这些条件没有明确说明，方法之间即使使用相似术语，也未必在解决同一问题。

跨中心域变化、新增分割结构和跨器官任务具有不同的学习目标。域变化通常保持分割语义不变，要求模型在顺序中心或设备间适应；新增结构会扩展输出空间，并可能伴随旧类别在当前阶段缺少标注；跨器官任务则可能同时改变图像区域、目标结构和输出头。第四章基准将这些情况分别组织为 Domain-CL、Class-CL 和 Organ-CL\cite{wang2026benchmark}，其目的在于形成可复现的医学分割场景，而不是宣布三种名称能够穷尽所有持续医学影像问题。

标注协议会进一步改变场景难度。持续语义分割中，若当前阶段只标注新增类别，旧类和未来类像素可能被并入背景，从而形成背景语义漂移\cite{yuan2024continualseg}；若每个阶段都对全部既有结构提供完整掩膜，这一问题则不以相同形式出现。因此，任务划分除了说明数据和类别如何变化，还需要说明当前标签覆盖哪些结构、测试时是否统一预测全部已见类别，以及是否提供任务或域身份。

场景定义不完备会直接影响评价结论。仅报告训练结束后的平均分割性能，无法区分模型是保持了旧任务、学会了当前任务，还是依赖某个阶段的高分掩盖了其他阶段的退化。仅报告遗忘量也不足以判断新任务是否被有效学习。Lifelong nnU-Net 的统一比较表明，方法行为会随任务序列、网络和评价设置发生变化\cite{gonzalez2023lifelong}，因而需要保存以训练阶段为行、测试任务为列的完整性能矩阵。

基于该矩阵，评价至少需要覆盖知识保持、当前任务可塑性和前向泛化。知识保持考察已学习任务在后续更新后的变化，当前任务可塑性考察模型在新阶段能够达到的学习水平，前向泛化则考察模型在尚未参与优化的任务或域上的直接表现\cite{wang2026benchmark}。前向泛化与前向迁移并非同一概念：前者强调未适应任务上的现有能力，后者通常比较已有知识是否改善后续任务的学习过程。二者若不区分，会使评价指标与研究目标错位。

资源和访问信息同样是评价的一部分。完整联合训练、有限回放、无回放、任务特定参数扩展和固定容量模型具有不同的数据与存储条件；在不报告历史样本数量、参数增长、计算开销和任务身份假设时，相同的最终性能不能被解释为相同难度下的结果\cite{wang2024continualsurvey,wang2026benchmark}。因此，持续分割基准不仅要统一数据序列，还要把资源约束和训练协议纳入比较范围。

由此，持续医学图像分割需要解决两个相互依赖的基础问题：建立能够区分域、类别、器官及其组合变化的明确场景，并形成同时衡量稳定性、可塑性、前向泛化和资源效率的评价体系。场景不清会使指标失去对应对象，评价维度不足又会掩盖场景中的真实取舍。这构成第四章场景定义与综合评测研究所针对的关键挑战。
```

Verify:

- all content through 1.3.1 is byte-for-byte unchanged;
- 1.3.2 title/label remain unique;
- 1.3.3--1.3.4, 1.4, and 1.5 remain body-empty;
- only the five approved citation keys are used;
- `Organ-CL` is explicitly limited to the Chapter 4 benchmark naming;
- forward transfer and forward generalization are not conflated;
- no benchmark result number or algorithm claim is introduced.

## Step 2: bibliography verification

Do not add entries. Verify the five keys exist, resolve in `.bbl`, and introduce no duplicate key/DOI/title. Preserve `\thesisbibliographytrue`.

## Step 3: append evidence records

```csv
C1-082,1,1.3.2,持续学习场景名称取决于输入分布标签空间任务身份和评价协议,DOI:10.1109/TPAMI.2024.3367329;DOI:10.1016/j.media.2025.103730,Scenario taxonomies,wang2024continualsurvey;kumari2025medicalcl,author_synthesis,confirmed,drafted,用于说明相同数据序列可能因协议不同被归入不同场景
C1-083,1,1.3.2,Domain-CL Class-CL和Organ-CL是第四章基准组织医学持续分割的三个命名场景,arXiv:2605.06160,Abstract and scenario definitions,wang2026benchmark,benchmark,confirmed,drafted,不得表述为领域统一且穷尽的标准分类
C1-084,1,1.3.2,背景语义漂移是否出现取决于当前阶段对旧类和未来类的标注协议,DOI:10.1109/TPAMI.2024.3446949,Problem definition and protocols,yuan2024continualseg,author_analysis,confirmed,drafted,完整标注域增量场景不机械套用该结论
C1-085,1,1.3.2,任意静态数据切分不足以定义可解释的持续医学分割场景,author scope definition,Section challenge analysis,kumari2025medicalcl;wang2026benchmark,author_definition,confirmed,drafted,需要交代顺序变化输出空间和测试条件
C1-086,1,1.3.2,最终平均性能或遗忘单一指标不能同时反映知识保持和新任务学习,DOI:10.1038/s41598-023-34484-2;arXiv:2605.06160,Comparative evaluation and benchmark framework,gonzalez2023lifelong;wang2026benchmark,author_synthesis,confirmed,drafted,用于提出多维评价要求
C1-087,1,1.3.2,阶段任务性能矩阵能够分别支撑稳定性可塑性和前向泛化评价,arXiv:2605.06160,Evaluation framework,wang2026benchmark,benchmark,confirmed,drafted,具体公式留待第四章
C1-088,1,1.3.2,前向泛化指未适应任务上的直接表现而前向迁移关注已有知识对后续学习过程的影响,author terminology distinction,Section definition,wang2024continualsurvey;wang2026benchmark,author_definition,confirmed,drafted,遵守本论文术语边界
C1-089,1,1.3.2,历史访问参数增长计算开销和任务身份条件影响持续分割结果的可比性,DOI:10.1109/TPAMI.2024.3367329;arXiv:2605.06160,Resource-efficiency framework and benchmark design,wang2024continualsurvey;wang2026benchmark,author_synthesis,confirmed,drafted,不能忽略资源条件直接排序
C1-090,1,1.3.2,持续医学分割基准需联合解决场景定义与稳定性可塑性泛化资源多维评价,author synthesis based on section sources,Section synthesis,kumari2025medicalcl;yuan2024continualseg;gonzalez2023lifelong;wang2026benchmark,author_analysis,confirmed,drafted,用于形成第四章问题入口而非算法贡献
```

Validate exact 11-column CSV structure, unique IDs `C1-082`--`C1-090`, unchanged existing rows, and valid bibliography keys.

## Step 4: terminology and status

### Add terminology rows

```csv
scenario completeness,场景完备性,第一章与第四章,场景完整性（避免混用）,场景定义是否明确覆盖变化对象顺序标签和测试条件
stage-task performance matrix,阶段—任务性能矩阵,第一章与第四章,准确率矩阵（任务指标不一定为准确率）,以训练阶段为行测试任务为列记录基础性能
current-task plasticity,当前任务可塑性,第一章与第四至六章,新任务性能（仅作观测量时使用）,模型在当前阶段吸收新知识的能力
resource-aware evaluation,资源约束评价,第一章与第四至六章,资源效率评价（范围较窄）,在数据存储参数计算通信等条件下解释模型表现
protocol-aware comparison,协议感知比较,第一章与第四至六章,公平比较（范围更宽）,比较时显式核对任务身份历史访问输出空间和资源条件
```

Validate 5 columns and unique English keys.

### Status

Set:

- `1.3` → `in_progress`
- `1.3.1` → `drafted_and_verified`
- `1.3.2` → `drafted_and_verified`, artifact `chapters/ch01_introduction.tex`
- `1.3.3` → `queued`
- `1.3.4` → `not_started`

Update concise `STATE.md`: 1.3.1 and 1.3.2 verified; next target 1.3.3; later prose absent.

## Step 5: fast verification

Run:

```bash
bash scripts/verify_fast_section.sh --quiet chapters/ch01_introduction.tex
```

Verify citations, references, labels, files, placeholders, BibTeX duplicates, CSV schemas/uniqueness, baseline hashes, empty later sections, `git diff --check`, unchanged `sources/` fingerprint, and no new layout warning.

No routine manual PDF inspection is required for this pure-text subsection. Inspect only if the build exposes a new anomaly attributable to this task.

## Step 6: concise report

Update `handoff/LATEST_CODEX_REPORT.md` in the content commit with preflight, exact integration, preserved hashes, bibliography reuse, evidence/terminology/status changes, fast verification result, `sources/` result, unresolved issues, and next target 1.3.3. Do not create a deployment-receipt commit.

## Step 7: commit and sync

Use one content commit, for example:

```bash
git commit -m "Draft Chapter 1 Section 1.3.2"
git push origin main
```

After remote verification and a clean worktree:

```bash
bash scripts/sync_latex_to_overleaf.sh --skip-local-build "Sync Chapter 1 Section 1.3.2"
```

Report GitHub and Overleaf SHAs in the terminal. No force-push and no second report-only commit.

## Definition of done

- 1.3.2 integrated exactly;
- prior prose unchanged;
- later subsections empty;
- no new bibliography records;
- `C1-082`--`C1-090` unique;
- terminology/status valid;
- fast verification succeeds;
- `sources/` unchanged;
- GitHub and Overleaf synchronized or exact failure reported;
- clean worktree;
- 1.3.3 remains undrafted.

Do not continue beyond Section 1.3.2.
