# Codex Task: integrate Chapter 1, Section 1.3.1

Read and obey `AGENTS.md`, `WORKFLOW_MODES.md`, `THESIS_CONTRACT.md`, `AUTHORSHIP_PROTOCOL.md`, `AUTHOR_VOICE.md`, `STATE.md`, `PROJECT_CONFIG.md`, and `chapter_cards/ch01.md` before editing.

## Workflow mode

Use **Mode A: fast subsection integration** in `WORKFLOW_MODES.md`.

This is a pure-text subsection task. Run one complete build and the changed-text style/reference-overlap checks through:

```bash
bash scripts/verify_fast_section.sh --quiet chapters/ch01_introduction.tex
```

Do not duplicate this with a second routine full build unless the script fails and a diagnostic build is required. Do not run a full-repository style audit, full PDF visual inspection, or rebuild `handoff/CONTEXT_PACKET_FOR_GPT.md` in this task. Those actions are reserved for the Chapter 1 milestone unless a newly introduced layout or build problem requires inspection.

After the verified content commit is pushed, synchronize Overleaf with the verified build fingerprint:

```bash
bash scripts/sync_latex_to_overleaf.sh --skip-local-build "Sync Chapter 1 Section 1.3.1"
```

Report the Overleaf SHA in the final terminal response. Do not create a second report-only Git commit solely to store the deployment receipt.

## Goal

Integrate the GPT Pro-approved draft for Section 1.3.1 “稀疏标注下监督不足与结构信息缺失” into the thesis repository.

This subsection must synthesize the research status in 1.2.1 into a precise technical challenge. It should explain why sparse scribble labels create coupled deficiencies in supervision coverage, class/space representation, and structural information. It must motivate Chapter 3 without presenting the full ZScribbleSeg solution, formulas, experiments, or contribution list.

Stop after 1.3.1 is completed and verified. Do not draft 1.3.2, 1.3.3, 1.3.4, or Section 1.4.

## Evidence basis

Use the already verified sources and bibliography entries from Section 1.2.1:

- `tajbakhsh2020imperfect`
- `can2018scribble`
- `luo2022scribble`
- `han2024dmsps`
- `kervadec2019constrained`
- `zhang2026zscribbleseg`

No new bibliography entry is expected in this task. If any required key is absent, stop and report rather than inventing or importing a record.

The approved prose is an original synthesis of the author’s ZScribbleSeg Introduction/Related Work and the verified original literature. Do not copy, translate, or closely paraphrase a source sentence.

## Strict scientific boundaries

- Do not describe weak supervision, annotation-efficient learning, scribble supervision, or ZScribbleSeg as continual learning.
- Do not claim that all weak annotations provide the same information.
- Do not treat unannotated pixels as confirmed background.
- Do not claim that pseudo-labeling always improves segmentation.
- Do not state that every sparse-label method necessarily produces under-segmentation or fragmentation; use conditional wording.
- Do not claim that a fixed class proportion, spatial prior, or shape prior is valid for every organ, modality, or lesion.
- Do not introduce ZScribbleSeg formulas, module implementation details, quantitative results, ablations, or contribution bullets.
- Do not draft a solution section. State the properties that a solution must satisfy.
- Do not modify any file under `sources/`.
- Do not import prose, figures, tables, citation combinations, metadata, or personal information from `sources/reference_thesis/`.

## Strict file scope

Files that may be modified or added:

- `CODEX_TASK_ch01_1_3_1.md`
- `chapters/ch01_introduction.tex`
- `evidence/claims.csv`
- `qa/terminology.csv`
- `qa/chapter_status.csv`
- `qa/style_audit_report.md`
- `qa/reference_overlap_report.md`
- `STATE.md`
- `handoff/LATEST_CODEX_REPORT.md`

`bibliography/references.bib` and `config/build_flags.tex` are read-only verification targets in this task. No bibliography or build-flag change is expected.

Do not modify another chapter, template/class file, figure, table, script, bibliography style, or any file under `sources/`.

Do not rewrite approved prose outside 1.3.1. Except for a strictly necessary LaTeX syntax correction or reuse of an existing equivalent citation key, integrate the approved text exactly.

## Step 0: repository and baseline preflight

1. Run:

   ```bash
   git status --short
   git branch --show-current
   git fetch origin
   ```

2. The worktree must be clean except that `CODEX_TASK_ch01_1_3_1.md` may be the only untracked file.
3. Confirm the current branch is `main`.
4. Confirm local `HEAD` is not behind or divergent from `origin/main`.
   - Use `git pull --ff-only origin main` only when the remote is ahead and the worktree is otherwise clean.
   - Stop on divergence, conflict, or unrelated modification. Do not reset, rebase, overwrite, or force-push.
5. Record the exact baseline commit SHA.
6. Confirm:
   - Sections 1.1 and 1.2 are present and `drafted_and_verified`;
   - the title and label for 1.3.1 already exist;
   - the body between `\label{subsec:intro-challenge-scribble}` and the 1.3.2 subsection command is empty;
   - 1.3.2, 1.3.3, 1.3.4, 1.4, and 1.5 contain no body text.
7. Save byte-for-byte hashes of:
   - all text before the 1.3.1 label;
   - the empty bodies of 1.3.2--1.3.4;
   - the empty bodies of Sections 1.4 and 1.5.
8. Confirm that `qa/chapter_status.csv` records 1.2 as `drafted_and_verified` and 1.3 as `queued`.
9. Confirm that `evidence/claims.csv` ends the Chapter 1 sequence at `C1-074`.
10. Confirm all six required citation keys exist in `bibliography/references.bib`, with no duplicate key, DOI, or normalized title.
11. Confirm `config/build_flags.tex` contains `\thesisbibliographytrue`.
12. Record the session-start `sources/` file count and deterministic SHA-256 fingerprint.

## Step 1: integrate the approved draft exactly

Preserve the existing title and label:

```latex
\subsection{稀疏标注下监督不足与结构信息缺失}
\label{subsec:intro-challenge-scribble}
```

Insert the following approved text immediately after that label and before the title of 1.3.2:

```latex
稀疏标注下的首要困难不是训练图像数量不足，而是单幅图像中的监督信息在空间、类别和结构三个层面均不完整。涂鸦能够指出部分像素所属的类别，却不直接描述目标的完整区域、边界位置及其与周围组织的关系\cite{tajbakhsh2020imperfect,zhang2026zscribbleseg}。因此，同一组涂鸦可能与多种候选分割同时相容，模型还需依据图像内容和附加约束判断未标注区域。

仅在涂鸦像素上计算部分交叉熵，可以避免将未知区域错误设为背景，但监督作用被限制在少量离散位置\cite{can2018scribble}。网络即使在这些位置取得较低损失，也不能保证未标注区域的类别、目标范围和边界均被正确恢复。随着涂鸦覆盖率下降或空间分布趋于集中，训练目标对错误区域扩张和目标遗漏的约束进一步减弱，形成监督覆盖不足。

标签传播和伪标签学习试图把模型预测转化为附加监督，但也形成了由当前模型决定后续训练目标的闭环。双分支预测和软伪标签能够降低单一硬预测带来的不稳定性\cite{luo2022scribble,han2024dmsps}，却不能消除初始预测偏差。当错误区域被赋予较高置信度，或多个分支共享相似偏差时，噪声可能随迭代被重复利用。因而，扩大监督范围与控制标签噪声并不是两个可以分别处理的问题。

涂鸦的类别分布还可能偏离完整图像中的真实类别构成。背景和大结构通常更容易获得较多标注像素，细小器官、狭窄边界或离散病灶则可能只被少量涂鸦覆盖。若训练过程直接把已标注像素的类别比例视为完整区域的代表，模型可能偏向占据更多监督像素的类别，并在目标类别上产生范围收缩或欠分割\cite{zhang2026zscribbleseg}。这一偏差取决于标注像素比例、空间随机性和目标形态，不能仅通过增加总涂鸦数量加以概括。

结构信息缺失进一步增加了医学目标恢复的难度。区域大小约束、空间关系和形状正则可以限定预测的整体范围\cite{kervadec2019constrained}，但先验过强或与当前病理不符时也可能压制真实变化。对于边界模糊、形态不规则或多灶分布的目标，局部外观相似性不足以唯一确定连通关系；模型可能出现边界缺失、孤立区域和结构碎片化\cite{zhang2026zscribbleseg}。因此，结构约束既要补充稀疏监督，又要保留不同病例之间的真实形态差异。

由此，稀疏标注医学图像分割需要同时解决三个相互耦合的问题：在不增加密集标注的条件下扩大可靠监督覆盖，校正标注在类别和空间上的代表性偏差，并恢复未被涂鸦直接描述的边界与全局结构。任何只强化其中一个方面的设计，都可能通过伪标签噪声、过度约束或类别偏置影响另外两个方面。这构成第三章研究所针对的核心技术挑战。
```

After insertion, verify:

- all content before the 1.3.1 label is byte-for-byte unchanged;
- the 1.3.1 title and label remain unique;
- 1.3.2--1.3.4, 1.4, and 1.5 remain body-empty;
- the approved prose uses exactly the six listed citation keys and no new key;
- no method formula, experiment number, or continual-learning characterization of ZScribbleSeg has been added.

## Step 2: bibliography verification

Do not add a new bibliography record.

Verify:

- all six cited keys exist;
- all six resolve in the generated `.bbl`;
- no duplicate key, DOI, or normalized title exists;
- `config/build_flags.tex` remains `\thesisbibliographytrue`.

If a required key is missing, stop and report. Do not reconstruct it from memory or import a bibliography file from `sources/`.

## Step 3: append evidence records

Append the following rows to `evidence/claims.csv` after verifying that the IDs are absent:

```csv
C1-075,1,1.3.1,涂鸦监督在空间类别和结构层面均不等价于完整密集掩膜,DOI:10.1016/j.media.2020.101693;DOI:10.1016/j.media.2026.104074,Review taxonomy and ZScribbleSeg problem formulation,tajbakhsh2020imperfect;zhang2026zscribbleseg,author_synthesis,confirmed,drafted,用于界定稀疏监督缺失的三个层面
C1-076,1,1.3.1,部分交叉熵只在已有涂鸦位置提供直接监督,DOI:10.1007/978-3-030-00889-5_27,Training strategy,can2018scribble,method,confirmed,drafted,不把未标注像素视为已知背景
C1-077,1,1.3.1,同一组稀疏涂鸦可能与多种未标注区域预测同时相容,author analysis based on sparse supervision,Section challenge analysis,tajbakhsh2020imperfect;can2018scribble,author_analysis,confirmed,drafted,用于说明低涂鸦损失不保证完整分割正确
C1-078,1,1.3.1,伪标签扩大监督范围时可能继承并强化模型或分支的共同预测偏差,DOI:10.1007/978-3-031-16431-6_50;DOI:10.1016/j.media.2024.103274,Method assumptions and pseudo-label construction,luo2022scribble;han2024dmsps,author_analysis,confirmed,drafted,采用条件性表述而非断言所有伪标签均有害
C1-079,1,1.3.1,有效涂鸦监督受到标注像素比例空间随机性和类别覆盖差异影响,DOI:10.1016/j.media.2026.104074,Introduction and efficient-scribble analysis,zhang2026zscribbleseg,method,confirmed,drafted,用于说明标注分布代表性
C1-080,1,1.3.1,类别标注比例偏差和结构信息缺失可能表现为欠分割及碎片化预测,DOI:10.1016/j.media.2026.104074,Problem formulation and framework motivation,zhang2026zscribbleseg,author_analysis,confirmed,drafted,不扩展为所有弱监督方法必然现象
C1-081,1,1.3.1,稀疏标注挑战需要联合处理可靠监督扩展类别空间偏差和结构恢复,author synthesis based on section sources,Section synthesis,tajbakhsh2020imperfect;luo2022scribble;han2024dmsps;kervadec2019constrained;zhang2026zscribbleseg,author_analysis,confirmed,drafted,用于形成第三章问题入口且不提前展开具体解法
```

Preserve the existing header and exact 11-column schema. Validate with Python’s CSV parser:

- every row has exactly 11 columns;
- IDs `C1-075`--`C1-081` occur exactly once;
- no existing evidence row is changed;
- every citation key exists in the active bibliography.

Do not normalize or rewrite pre-existing mixed line endings merely to satisfy a different CSV implementation. Preserve existing rows and ensure Python standard-library parsing succeeds.

## Step 4: terminology and section status

### 4.1 Add terminology rows

Add the following non-duplicate rows to `qa/terminology.csv`:

```csv
supervision coverage,监督覆盖,第一章与第三章,监督范围（可作解释）,有直接或可靠间接训练信号约束的图像区域
annotation class-proportion bias,标注类别比例偏差,第一章与第三章,类别不平衡（范围不完全等同）,稀疏标注中的类别比例偏离完整图像类别构成
label-noise amplification,标签噪声放大,第一章与第三章,噪声累积（可作解释）,错误伪标签在后续迭代中被重复作为监督
under-segmentation,欠分割,第一章与第三章,分割不足（避免混用）,预测区域系统性遗漏目标的一部分
structural fragmentation,结构碎片化,第一章与第三章,预测碎片化（可作解释）,同一目标被预测为不合理的离散或断裂区域
```

Validate with a CSV parser:

- exactly 5 columns per row;
- unique English-term keys;
- no existing preferred Chinese term is changed.

### 4.2 Update `qa/chapter_status.csv`

Insert subsection rows if absent, and set:

- `1.3` → `in_progress`, artifact `chapters/ch01_introduction.tex`
- `1.3.1` → `drafted_and_verified`, artifact `chapters/ch01_introduction.tex`
- `1.3.2` → `queued`
- `1.3.3` → `not_started`
- `1.3.4` → `not_started`

Preserve all existing rows and the four-column schema.

### 4.3 Update `STATE.md`

Keep it concise. Record:

- Sections 1.1 and 1.2 remain complete and unchanged;
- 1.3.1 is integrated and verified;
- Section 1.3 is in progress;
- the next target is 1.3.2 “持续分割场景和评价维度不完备”;
- no later 1.3 subsection was drafted;
- the fast verification/build result and any new warning;
- `sources/` remained outside the diff.

Do not rebuild `handoff/CONTEXT_PACKET_FOR_GPT.md`.

## Step 5: fast verification

Run exactly:

```bash
bash scripts/verify_fast_section.sh --quiet chapters/ch01_introduction.tex
```

The script’s complete build and changed-text checks must succeed. Review its summary and additionally verify:

1. all active citations resolve;
2. no undefined citation/reference;
3. no duplicate label;
4. no missing input, class, figure, table, or bibliography file;
5. no new `TODO`, `TBD`, or `??`;
6. no duplicate BibTeX key, DOI, or normalized title;
7. `git diff --check` passes;
8. claims CSV has 11 columns and unique IDs;
9. terminology CSV has 5 columns and unique English keys;
10. all preserved baseline hashes match;
11. no body text was added outside 1.3.1;
12. `sources/` is absent from `git diff` and its session-end file count/fingerprint matches the session-start snapshot;
13. no new layout warning is introduced by this text-only change.

Do not perform routine manual PDF page inspection for this pure-text subsection. If the build reports a new overfull box, missing content, abnormal page break, or another layout anomaly attributable to this task, inspect only the affected pages and report the result.

## Step 6: concise handoff report

Replace `handoff/LATEST_CODEX_REPORT.md` with a concise report containing:

- task name and timestamp;
- baseline SHA and preflight result;
- exact changed files;
- confirmation that approved prose was integrated exactly;
- confirmation that Sections 1.1, 1.2, and later empty sections were preserved;
- bibliography reuse result;
- evidence and terminology additions;
- chapter-status and state changes;
- fast verification command and result;
- citation/reference/label/file/CSV status;
- changed-text style and reference-overlap result;
- `sources/` unchanged result;
- unresolved scientific, source, build, or layout issues;
- next target 1.3.2 and confirmation it was not drafted.

The content commit must include this handoff report. Do not create a later report-only commit merely to store the Overleaf SHA.

## Step 7: commit, push, and synchronize

After verification:

```bash
git diff --check
git status --short
```

Stage only permitted files and create one content commit, for example:

```bash
git commit -m "Draft Chapter 1 Section 1.3.1"
git push origin main
```

Verify the content commit exists on `origin/main` and the worktree is clean. Within 30 minutes of the verified build, run:

```bash
bash scripts/sync_latex_to_overleaf.sh --skip-local-build "Sync Chapter 1 Section 1.3.1"
```

Record the GitHub content SHA and Overleaf deployment SHA in the final terminal response. Do not make a second GitHub commit solely for the deployment receipt.

Final checks:

```bash
git status --short
git rev-parse HEAD
git rev-parse origin/main
```

Local `HEAD` must match `origin/main`; no force-push is allowed.

## Definition of done

This task is complete only when:

- the approved 1.3.1 prose is integrated exactly;
- Sections 1.1 and 1.2 are unchanged;
- 1.3.2--1.3.4, 1.4, and 1.5 remain body-empty;
- no new bibliography entry is introduced and all cited keys resolve;
- `C1-075`--`C1-081` occur exactly once;
- terminology additions are valid and unique;
- 1.3.1 is `drafted_and_verified` and 1.3.2 is `queued`;
- fast verification succeeds;
- `sources/` is unchanged;
- the verified content is pushed to GitHub;
- the LaTeX subset is synchronized to Overleaf or an exact non-bypassed failure is reported;
- the worktree is clean;
- 1.3.2 is not drafted.

Do not continue beyond Section 1.3.1.
