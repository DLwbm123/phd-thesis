# Codex Task: integrate Chapter 2, Section 2.1.1

Read and obey `AGENTS.md`, `WORKFLOW_MODES.md`, `THESIS_CONTRACT.md`,
`AUTHORSHIP_PROTOCOL.md`, `AUTHOR_VOICE.md`, `STATE.md`,
`PROJECT_CONFIG.md`, `SOURCE_MAP.md`, `chapter_cards/ch02.md`,
`qa/terminology.csv`, and `qa/notation.csv` before editing.

## Workflow mode

Use **Mode A: fast subsection integration** in `WORKFLOW_MODES.md`.

This task adds display equations, so the ordinary fast verification must be
followed by targeted visual inspection of the PDF pages containing Section
2.1.1 and any bibliography page changed by the new reference.

Run:

```bash
bash scripts/verify_fast_section.sh --quiet chapters/ch02_foundations.tex
```

Do not duplicate this command with another routine full build unless it fails
and a diagnostic build is required. Do not run the Chapter 2 milestone audit or
rebuild `handoff/CONTEXT_PACKET_FOR_GPT.md`.

After the verified content commit is pushed, synchronize the compilable LaTeX
subset with:

```bash
bash scripts/sync_latex_to_overleaf.sh --skip-local-build "Sync Chapter 2 Section 2.1.1"
```

Report the GitHub content SHA and Overleaf deployment SHA in the final terminal
response. Do not create a second GitHub commit only to record the deployment
receipt.

## Goal

Integrate the GPT Pro-approved section introduction for 2.1 and the approved
draft for Section 2.1.1 “医学图像分割”.

The subsection must provide the shared technical foundation for later chapters:

- define semantic medical image segmentation as a dense prediction problem;
- distinguish two-dimensional and three-dimensional image domains;
- define model outputs and a supervised cross-entropy objective;
- define region-overlap and boundary-distance evaluation metrics;
- explain why metric interpretation depends on target properties, physical
  spacing, class aggregation, and empty-class handling.

It must not become a literature-review subsection and must not introduce the
ZScribbleSeg method, weak supervision, continual learning, or experimental
claims.

Stop after 2.1.1 is integrated and verified. Do not draft 2.1.2 or any later
Chapter 2 subsection.

## Evidence basis

Before editing, read the relevant parts of:

- `sources/zscribble/Zscribble_MEDIA_arxiv/main_clean_new.tex`
- `sources/benchmark/Benchmark_pa/main.tex`

These source files may be used only to confirm the task type, dimensionality,
notation compatibility, and metrics used by the author's later chapters. They
are not text to translate or copy.

Reuse the verified bibliography entries:

- `litjens2017survey`
- `ronneberger2015unet`

Add or reuse the single verified metric reference supplied below:

- `taha2015metrics`

The approved prose is an original technical synthesis. Do not copy, translate,
or closely paraphrase any source sentence. Do not use any content from
`sources/reference_thesis/`.

## Strict scientific boundaries

- Use “医学影像” for the field and “医学图像” for concrete images and
  algorithmic tasks.
- Treat the main task in this thesis as semantic segmentation. Do not silently
  convert it to instance segmentation or object detection.
- Do not claim that every segmentation task is binary or that all classes are
  mutually exclusive without stating the current formulation.
- Do not treat a two-dimensional slice and a three-dimensional volume as
  interchangeable. Physical voxel spacing must be distinguished from array
  indices when distance metrics are interpreted.
- Do not treat unlabeled pixels as background; weak supervision belongs to
  Section 2.2.
- Do not equate the cross-entropy training objective with the final evaluation
  metric.
- Do not claim that Dice, IoU, HD95, or ASSD alone is sufficient for every
  segmentation problem.
- Do not introduce ZScribbleSeg modules, losses, experiments, or innovations.
- Do not discuss continual learning, federated learning, replay, or task
  evolution.
- Do not modify any file under `sources/`.
- Do not import prose, figures, tables, references, metadata, or personal
  information from `sources/reference_thesis/`.

## Strict file scope

Files that may be modified or added:

- `CODEX_TASK_ch02_2_1_1.md`
- `chapters/ch02_foundations.tex`
- `bibliography/references.bib`
- `evidence/claims.csv`
- `qa/terminology.csv`
- `qa/notation.csv`
- `qa/chapter_status.csv`
- `qa/style_audit_report.md`
- `qa/reference_overlap_report.md`
- `STATE.md`
- `handoff/LATEST_CODEX_REPORT.md`

`config/build_flags.tex` is a read-only verification target and must remain
`\thesisbibliographytrue`.

Do not modify Chapter 1, another Chapter 2 subsection, another chapter,
template/class files, build scripts, figures, tables, or any file under
`sources/`.

Except for a strictly necessary LaTeX syntax correction or reuse of an
equivalent existing citation key, integrate the approved text exactly.

## Step 0: repository and baseline preflight

1. Run:

   ```bash
   git status --short
   git branch --show-current
   git fetch origin
   ```

2. The worktree must be clean except that `CODEX_TASK_ch02_2_1_1.md` may be
   the only untracked file.
3. Confirm the branch is `main`, local `HEAD` is not divergent from
   `origin/main`, and only use `git pull --ff-only origin main` when required.
   Stop on divergence, conflicts, or unrelated modifications. Never reset,
   rebase, overwrite, or force-push.
4. Record the exact baseline SHA.
5. Confirm:
   - Chapter 1 is `drafted_and_verified`;
   - Chapter 2 is `queued`;
   - `chapters/ch02_foundations.tex` contains the expected skeleton;
   - the body between `\subsection{医学图像分割}` and
     `\subsection{医学图像配准}` is empty;
   - 2.1.2, 2.1.3, and all later Chapter 2 subsections contain no body text.
6. Confirm that the Section 2.1 and 2.1.1 labels supplied below do not already
   exist. If an equivalent label exists, preserve it and report the key change
   rather than creating a duplicate.
7. Save byte-for-byte hashes of:
   - all Chapter 1 content;
   - the Chapter 2 skeleton before the Section 2.1 command;
   - the empty bodies of 2.1.2, 2.1.3, and all later Chapter 2 subsections.
8. Confirm `evidence/claims.csv` contains no `C2-` claim and that
   `C2-001` is the next Chapter 2 ID.
9. Confirm `qa/notation.csv` uses the seven-column schema and contains the
   existing `theta` row exactly once.
10. Confirm `litjens2017survey` and `ronneberger2015unet` exist in the active
    bibliography.
11. Check for an existing equivalent of `taha2015metrics` by key, DOI, and
    normalized title.
12. Confirm `config/build_flags.tex` contains `\thesisbibliographytrue`.
13. Record the session-start file count and deterministic SHA-256 fingerprint
    for all files under `sources/`.

## Step 1: add the Section 2.1 label and introduction

Preserve:

```latex
\section{医学影像智能分析任务基础}
```

Immediately after the section command, add:

```latex
\label{sec:foundations-tasks}

医学影像智能分析的基本任务可以按照输出空间区分为分割、配准和分类。分割在图像网格上预测结构标签，配准估计图像之间的空间变换，分类则在图像、检查或病例层面输出类别或类别概率\cite{litjens2017survey}。三类任务可以共享特征提取思想，但其预测对象、监督单位和评价尺度不同，因而需要分别定义数学映射和性能指标。本节建立后续章节共同使用的任务记号，不展开弱监督、持续学习或联邦学习机制。
```

Do not alter the titles or order of the three subsections.

## Step 2: integrate the approved 2.1.1 draft exactly

Preserve:

```latex
\subsection{医学图像分割}
```

Immediately after that command, add:

```latex
\label{subsec:foundations-segmentation}

医学图像分割旨在为图像域中的每个像素或体素赋予解剖结构、病灶或背景标签，从而得到与输入图像空间对应的标签图\cite{litjens2017survey,ronneberger2015unet}。本文后续研究主要采用语义分割设定，即同一类别的所有位置共享类别语义，而不额外区分同类目标的实例身份。根据标签空间大小，语义分割可以表现为前景与背景的二值分割，也可以表现为多个解剖结构或病理区域的多类分割。

设图像域为 $\Omega\subset\mathbb{Z}^{d}$，其中 $d=2$ 表示二维图像，$d=3$ 表示三维体数据。输入医学图像记为 $\mathbf{I}:\Omega\rightarrow\mathbb{R}^{C}$，$C$ 为图像通道数；参考标签图记为 $\mathbf{Y}:\Omega\rightarrow\{0,\ldots,K-1\}$，$K$ 为类别数。参数为 $\theta$ 的分割模型 $f_{\theta}$ 在每个位置 $\mathbf{u}\in\Omega$ 输出类别概率向量 $\mathbf{p}_{\theta}(\mathbf{u})$，满足 $\sum_{k=0}^{K-1}p_{\theta,k}(\mathbf{u})=1$。多类预测由最大概率类别确定：
\begin{equation}
\mathbf{p}_{\theta}(\mathbf{u})=f_{\theta}(\mathbf{I})(\mathbf{u}),\qquad
\widehat{\mathbf{Y}}(\mathbf{u})
=\operatorname*{arg\,max}_{0\leq k<K}p_{\theta,k}(\mathbf{u}).
\label{eq:foundations-seg-prediction}
\end{equation}
对于二值分割，也可以只输出前景概率，并通过给定阈值得到前景区域。

二维分割通常以单幅图像或切片为计算单位，三维分割则在体素网格上联合建模空间信息。二者的数组表示可以采用相同的离散域记号，但距离和体积的物理含义取决于像素或体素间距。尤其在各向异性的三维数据中，相邻切片之间的物理距离可能明显大于层内像素间距，因此以毫米为单位的边界距离不能直接由未校正的数组索引代替。

在完整监督条件下，可以把每个空间位置视为一个多类分类单元。令 $Y_k(\mathbf{u})$ 为参考标签在位置 $\mathbf{u}$ 属于类别 $k$ 的独热编码，则平均交叉熵写为
\begin{equation}
\mathcal{L}_{\mathrm{CE}}(\theta)
=-\frac{1}{|\Omega|}
\sum_{\mathbf{u}\in\Omega}\sum_{k=0}^{K-1}
Y_k(\mathbf{u})\log p_{\theta,k}(\mathbf{u}).
\label{eq:foundations-seg-ce}
\end{equation}
该目标直接约束位置级类别概率，但分割训练还可以根据类别不平衡、边界关注或区域重叠需求采用其他损失。训练损失用于构造优化信号，评价指标用于描述预测结果的性质，两者即使形式相近也不应被视为同一概念。

区域重叠是分割评价的基础。对类别 $k$，令预测区域和参考区域分别为
$P_k=\{\mathbf{u}\in\Omega:\widehat{\mathbf{Y}}(\mathbf{u})=k\}$ 和
$G_k=\{\mathbf{u}\in\Omega:\mathbf{Y}(\mathbf{u})=k\}$。Dice 相似系数和交并比分别定义为\cite{taha2015metrics}
\begin{equation}
\mathrm{DSC}_k=\frac{2|P_k\cap G_k|}{|P_k|+|G_k|},\qquad
\mathrm{IoU}_k=\frac{|P_k\cap G_k|}{|P_k\cup G_k|}.
\label{eq:foundations-seg-overlap}
\end{equation}
二者均衡量区域重叠，但数值尺度不同。若预测区域和参考区域同时为空，分母可能为零，因而实现中必须明确空类别的计分与汇总规则。

重叠指标不能完整描述边界误差。令 $\partial P_k$ 和 $\partial G_k$ 表示两个区域的边界点集，点到集合的距离定义为
$d(\mathbf{a},B)=\min_{\mathbf{b}\in B}\|\mathbf{a}-\mathbf{b}\|_2$，$Q_q$ 表示分位数算子，则 95\% 豪斯多夫距离和平均对称表面距离可以写为\cite{taha2015metrics}
\begin{align}
\mathrm{HD95}_k
&=\max\left\{
Q_{0.95}\!\left(\{d(\mathbf{a},\partial G_k):\mathbf{a}\in\partial P_k\}\right),
Q_{0.95}\!\left(\{d(\mathbf{b},\partial P_k):\mathbf{b}\in\partial G_k\}\right)
\right\}, \\
\mathrm{ASSD}_k
&=\frac{
\sum_{\mathbf{a}\in\partial P_k}d(\mathbf{a},\partial G_k)
+\sum_{\mathbf{b}\in\partial G_k}d(\mathbf{b},\partial P_k)}
{|\partial P_k|+|\partial G_k|}.
\label{eq:foundations-seg-boundary}
\end{align}
距离指标应在物理坐标中计算，并注明单位、分位数定义和空边界处理方式。

不同指标对目标大小、边界离群点和局部结构错误的敏感性不同\cite{taha2015metrics}。DSC 和 IoU 适合描述总体重叠，却可能弱化局部边界偏差；HD95 强调较大边界误差，但其数值受分位数和空间分辨率影响；ASSD 描述平均边界偏差，却可能掩盖少量严重错误。多类任务还需说明采用逐类平均、按样本平均还是全数据聚合。因而，医学图像分割评价通常需要根据目标结构、任务用途和数据尺度组合区域与边界指标，而不是只报告单一数值。

分割在一个既定坐标系中描述区域和边界。若需要比较不同时间、不同模态或不同个体的图像，首先还需建立图像之间的空间对应关系。下一小节据此介绍医学图像配准的基本表述。
```

Verify that all equations compile and that no equation label is duplicated.

## Step 3: add or reuse the verified bibliography entry

Before adding, check key, case-insensitive DOI, normalized title, and equivalent
records under other keys.

Add only if no equivalent record exists:

```bibtex
@article{taha2015metrics,
  author  = {Taha, Abdel Aziz and Hanbury, Allan},
  title   = {Metrics for Evaluating 3D Medical Image Segmentation: Analysis, Selection, and Tool},
  journal = {BMC Medical Imaging},
  volume  = {15},
  pages   = {29},
  year    = {2015},
  doi     = {10.1186/s12880-015-0068-x}
}
```

Do not add another uncited entry. Preserve all existing bibliography records and
`\thesisbibliographytrue`.

## Step 4: append evidence records

Append after confirming the IDs are absent:

```csv
C2-001,2,2.1,医学影像智能分析的分割配准和分类任务具有不同输出空间监督单位和评价尺度,DOI:10.1016/j.media.2017.07.005,Task taxonomy and section synthesis,litjens2017survey,author_synthesis,confirmed,drafted,用于建立2.1统一任务入口
C2-002,2,2.1.1,医学图像语义分割在像素或体素网格上预测结构病灶或背景标签,DOI:10.1016/j.media.2017.07.005;DOI:10.1007/978-3-319-24574-4_28,Task definition and dense prediction formulation,litjens2017survey;ronneberger2015unet,literature,confirmed,drafted,本文主要范围为语义分割而非实例分割
C2-003,2,2.1.1,二维和三维分割可统一写在离散图像域上但距离解释必须考虑物理像素体素间距,DOI:10.1186/s12880-015-0068-x,Metric definitions and 3D evaluation conditions,taha2015metrics,author_synthesis,confirmed,drafted,各向异性数据不得直接以数组索引解释毫米距离
C2-004,2,2.1.1,分割模型在每个空间位置输出类别概率并通过最大概率得到多类标签图,author mathematical definition,Equation eq:foundations-seg-prediction,,author_definition,confirmed,drafted,二值情形允许单前景概率与阈值
C2-005,2,2.1.1,完整监督下平均交叉熵对所有有参考标签的空间位置计算类别概率损失,author mathematical definition,Equation eq:foundations-seg-ce,,author_definition,confirmed,drafted,训练损失不等同评价指标
C2-006,2,2.1.1,Dice相似系数和交并比分别基于预测区域与参考区域的交集和集合大小衡量重叠,DOI:10.1186/s12880-015-0068-x,Overlap metric definitions,taha2015metrics,metric,confirmed,drafted,空类别处理规则必须显式说明
C2-007,2,2.1.1,HD95和ASSD基于预测与参考边界之间的双向点集距离衡量边界误差,DOI:10.1186/s12880-015-0068-x,Distance metric definitions,taha2015metrics,metric,confirmed,drafted,距离应在物理坐标中计算
C2-008,2,2.1.1,区域重叠指标和边界距离指标对目标大小局部误差及离群点具有不同敏感性,DOI:10.1186/s12880-015-0068-x,Metric analysis and selection guidelines,taha2015metrics,literature,confirmed,drafted,不以单一指标覆盖全部任务需求
C2-009,2,2.1.1,多类医学图像分割评价需要说明逐类逐样本或全局聚合方式,author evaluation definition,Section metric interpretation,taha2015metrics,author_analysis,confirmed,drafted,用于保证不同实验结果可解释
```

Validate `evidence/claims.csv` with Python's CSV parser:

- exactly 11 columns in every row;
- IDs `C2-001`--`C2-009` occur exactly once;
- no existing row changes;
- every non-empty citation key exists in the active bibliography.

Preserve the existing mixed line endings rather than normalizing the whole
file.

## Step 5: terminology registration

Add the following non-duplicate rows to `qa/terminology.csv`:

```csv
semantic segmentation,语义分割,第二至四章,语义图像分割（避免混用）,为每个空间位置赋予类别语义且不区分同类实例身份
binary segmentation,二值分割,第二至四章,二分类分割（避免混用）,前景与背景两类的空间预测任务
multiclass segmentation,多类分割,第二至四章,多类别分割（统一用多类分割）,在同一标签空间中预测多个互斥结构类别
label map,标签图,第二至四章,标签掩膜（按语境使用）,与图像网格对应的离散类别标记
probability map,概率图,第二至四章,概率掩膜（避免混用）,模型在图像网格上输出的逐类概率
Dice similarity coefficient,Dice相似系数,第二至四章,Dice系数（首次定义后可简称）,衡量预测区域与参考区域重叠
intersection over union,交并比,第二至四章,Jaccard系数（首次可说明同义）,预测与参考区域交集占并集的比例
95th-percentile Hausdorff distance,95%豪斯多夫距离,第二至四章,HD95（首次定义后可用缩写）,双向边界距离的95%分位数最大值
average symmetric surface distance,平均对称表面距离,第二至四章,平均表面距离（范围可能不同）,两个边界点集双向最近距离的平均值
```

Validate exactly 5 columns and globally unique English keys. Do not alter
existing preferred Chinese terms.

## Step 6: notation registration

Update only the `first_definition` and `status` fields of the existing `theta`
row so that it records its first formal definition in 2.1.1:

```csv
theta,模型参数,跨章节,2.1.1,all,defined,各章可带上下标但含义需一致
```

Add the following non-duplicate rows to `qa/notation.csv`:

```csv
Omega,离散图像域,第二至六章,2.1.1,author_definition,defined,d取2或3分别表示二维或三维
I,输入医学图像,第二至四章,2.1.1,author_definition,defined,配准小节使用带F和M下标的图像记号
Y,参考标签图,第二至四章,2.1.1,author_definition,defined,空间位置取0至K减1的离散类别
K,类别数,第二至六章,2.1.1,author_definition,defined,按具体任务说明是否包含背景
f_theta,参数化预测模型,第二至六章,2.1.1,author_definition,defined,不同章节的输入输出空间由任务定义
p_theta_k,位置u属于类别k的预测概率,第二至四章,2.1.1,author_definition,defined,多类情形对k求和为1
Y_hat,预测标签图,第二至四章,2.1.1,author_definition,defined,由逐位置最大类别概率得到
L_CE,交叉熵损失,第二至六章,2.1.1,author_definition,defined,按任务可采用多类或二元形式
P_k,类别k的预测区域,第二至四章,2.1.1,author_definition,defined,由预测标签图定义
G_k,类别k的参考区域,第二至四章,2.1.1,author_definition,defined,由参考标签图定义
d_a_B,点a到集合B的最近欧氏距离,第二至五章,2.1.1,author_definition,defined,边界评价时应使用物理坐标
Q_q,q分位数算子,第二至五章,2.1.1,author_definition,defined,HD95中q取0.95
```

Validate the existing seven-column schema and globally unique symbols. Do not
change unrelated pending symbols.

## Step 7: status and state

Update `qa/chapter_status.csv`:

- `2` → `in_progress`, artifact `chapters/ch02_foundations.tex`;
- add `2.1,医学影像智能分析任务基础,in_progress,chapters/ch02_foundations.tex`
  if absent;
- add `2.1.1,医学图像分割,drafted_and_verified,chapters/ch02_foundations.tex`;
- add `2.1.2,医学图像配准,queued,`;
- add `2.1.3,医学图像分类,not_started,`;
- keep Section 2.2 and later sections in their pre-writing state.

Update `STATE.md` concisely:

- Chapter 1 remains complete and unchanged;
- Chapter 2 and Section 2.1 are in progress;
- 2.1.1 is integrated and verified;
- 2.1.2 is the next target;
- no 2.1.2 or later prose was drafted;
- record build, citation, targeted visual inspection, and deployment results;
- record that `sources/` remained unchanged.

Do not rebuild `handoff/CONTEXT_PACKET_FOR_GPT.md`.

## Step 8: verify and inspect

Run:

```bash
bash scripts/verify_fast_section.sh --quiet chapters/ch02_foundations.tex
```

Additionally verify:

1. all citations resolve;
2. no undefined reference or duplicate label;
3. no missing input, class, bibliography, figure, or table;
4. no new `TODO`, `TBD`, or `??`;
5. no duplicate BibTeX key, DOI, or normalized title;
6. all four equation labels are unique;
7. evidence, terminology, and notation CSV schemas and uniqueness;
8. all preserved hashes match;
9. no body text appears outside the Section 2.1 introduction and 2.1.1;
10. `git diff --check` passes;
11. `sources/` is outside the diff and its ending count/fingerprint matches the
    starting snapshot.

Because this task adds display equations, render and inspect every PDF page
containing the Section 2.1 introduction and 2.1.1, plus the bibliography page
containing `taha2015metrics`. Check equation wrapping, symbol rendering,
heading placement, Chinese text, blank space, clipping, and page breaks. Record
the exact pages inspected.

## Step 9: concise handoff report

Replace `handoff/LATEST_CODEX_REPORT.md` with a concise report containing:

- task, timestamp, and baseline SHA;
- exact changed files;
- exact prose/equation integration;
- preserved Chapter 1 and empty later Chapter 2 bodies;
- bibliography addition or reuse;
- evidence, terminology, notation, status, and state changes;
- verification command and result;
- PDF pages inspected and result;
- `sources/` integrity result;
- unresolved source, notation, build, or layout issues;
- next target 2.1.2 and confirmation it was not drafted.

## Step 10: commit and synchronize

After verification:

```bash
git diff --check
git status --short
git commit -m "Draft Chapter 2 Section 2.1.1"
git push origin main
```

Stage only permitted files. Verify the pushed content commit and a clean
worktree, then run within 30 minutes of the verified build:

```bash
bash scripts/sync_latex_to_overleaf.sh --skip-local-build "Sync Chapter 2 Section 2.1.1"
```

Report the GitHub and Overleaf SHAs. Do not force-push and do not create a
receipt-only commit.

## Definition of done

Complete only when:

- the Section 2.1 introduction and 2.1.1 are integrated exactly;
- Chapter 1 is unchanged;
- 2.1.2 and all later Chapter 2 bodies remain empty;
- `taha2015metrics` is added or reused without duplicates;
- `C2-001`--`C2-009` occur exactly once;
- terminology and notation records are valid;
- 2.1.1 is `drafted_and_verified`;
- fast verification and targeted PDF inspection succeed;
- `sources/` is unchanged;
- GitHub and Overleaf are synchronized or an exact failure is reported;
- the worktree is clean;
- 2.1.2 remains undrafted.

Do not continue beyond Section 2.1.1.
