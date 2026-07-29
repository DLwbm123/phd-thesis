# Codex Task: integrate Chapter 1, Section 1.2.1

Read and obey `AGENTS.md`, `THESIS_CONTRACT.md`, `AUTHORSHIP_PROTOCOL.md`, `AUTHOR_VOICE.md`, `STATE.md`, `PROJECT_CONFIG.md`, and `chapter_cards/ch01.md` before editing.

## Goal

Integrate the GPT Pro-approved draft for Section 1.2.1 “标注高效与弱监督医学图像分割研究现状” into the thesis repository. Add only the verified references, evidence records, and terminology updates supplied below; compile and inspect the complete thesis; run all required audits; push the verified work to `origin/main`; and synchronize the compilable LaTeX subset to Overleaf.

This task is the first of three sequential tasks for Section 1.2. It must stop after 1.2.1 is completed and verified. Do not draft 1.2.2 or 1.2.3.

## Evidence policy

The literature organization below was prepared using the user-provided surveys and the Introduction/Related Work of the author’s ZScribbleSeg study. Surveys are used to establish terminology and locate research lines; the actual academic claims in the approved prose are tied primarily to original papers.

Source priority:

1. original papers and verified publisher/DOI metadata;
2. the author’s ZScribbleSeg article as the source for its own motivation, mechanism, and scope;
3. surveys only for broad taxonomy or synthesis;
4. no content from `sources/reference_thesis/`.

Do not copy, translate, or closely paraphrase any source sentence. The approved Chinese text below is an original synthesis and must be integrated exactly.

## Strict scientific boundaries

- Do not describe weak supervision, annotation-efficient learning, scribble supervision, or ZScribbleSeg as continual learning.
- Do not treat image-level labels, points, boxes, scribbles, and partial-slice annotations as equivalent supervision.
- Do not claim that a weak annotation preserves all information contained in a dense mask.
- Do not claim that pseudo-label generation always improves segmentation; state its dependence on prediction quality and error control.
- Do not claim that one method or annotation form is universally best across organs, modalities, and pathological targets.
- Do not introduce experimental numbers from ZScribbleSeg or another method in this research-status subsection.
- Do not describe ZScribbleSeg as a clinical deployment, a universal framework for every annotation form, or a continual-learning method.
- Do not turn the subsection into a method chapter. Only give the level of mechanism detail required to identify research lines and the unresolved problem.
- Do not draft Section 1.2.2, Section 1.2.3, Section 1.3, or any later section.
- Do not modify, translate, paraphrase, or import prose, figures, tables, bibliography combinations, metadata, or personal information from `sources/reference_thesis/`.
- Do not modify any file under `sources/`.

## Strict file scope

Files that may be modified or added:

- `CODEX_TASK_ch01_1_2_1.md` — preserve this task file exactly if placed in the repository; add it as task provenance if untracked
- `chapters/ch01_introduction.tex`
- `bibliography/references.bib`
- `config/build_flags.tex` — only if required to keep `\thesisbibliographytrue`; no change is expected
- `evidence/claims.csv`
- `qa/terminology.csv`
- `qa/chapter_status.csv`
- `qa/style_audit_report.md`
- `qa/reference_overlap_report.md`
- `STATE.md`
- `handoff/LATEST_CODEX_REPORT.md`

Do not modify another chapter, template/class file, figure, table, script, bibliography style, or any file under `sources/`. Ordinary LaTeX build products may be regenerated locally but must not be committed if excluded by `.gitignore`.

Do not rewrite the approved academic prose except for a strictly necessary LaTeX syntax correction or replacement of a citation key when an equivalent verified bibliography record already exists under a different key. Report any concern instead of silently rewriting.

## Step 0: repository and baseline preflight

Before editing:

1. Run:

   ```bash
   git status --short
   git branch --show-current
   git fetch origin
   ```

2. The worktree must be clean except that `CODEX_TASK_ch01_1_2_1.md` may be the only untracked file.
3. Confirm that the branch is `main`.
4. Confirm that local `HEAD` is not behind or divergent from `origin/main`.
   - If the remote is ahead and the worktree is otherwise clean, use `git pull --ff-only origin main`.
   - If histories diverge or unrelated modifications exist, stop and report the exact state. Do not overwrite, reset, rebase, or force-push.
5. Record the exact baseline commit SHA.
6. Confirm in `chapters/ch01_introduction.tex` that:
   - Sections 1.1.1, 1.1.2, and 1.1.3 are present and must remain unchanged;
   - `\raggedbottom` is present and must remain unchanged;
   - the title and label of 1.2.1 already exist;
   - the body between `\label{subsec:intro-weak-supervision}` and the next subsection is empty;
   - 1.2.2 and 1.2.3 contain titles and labels only;
   - Section 1.3 contains titles and labels only.
7. Save byte-for-byte hashes of:
   - the complete Section 1.1 body;
   - the empty 1.2.2 body;
   - the empty 1.2.3 body;
   - the empty Section 1.3 body.
8. Confirm that `bibliography/references.bib` currently contains the 13 verified entries used by Section 1.1, unless the repository has a newer verified baseline. Record the actual count rather than guessing.
9. Confirm that `config/build_flags.tex` contains `\thesisbibliographytrue`.
10. Confirm that `evidence/claims.csv` contains unique claim IDs and currently ends the Chapter 1 sequence at `C1-029`.
11. Confirm that `qa/chapter_status.csv` records Section 1.2 as `queued`.
12. Record a deterministic read-only snapshot of `sources/`, including file count and SHA-256, for final comparison.

## Step 1: integrate the approved draft exactly

Preserve the existing title and label:

```latex
\subsection{标注高效与弱监督医学图像分割研究现状}
\label{subsec:intro-weak-supervision}
```

Insert the following text immediately after the label and before the title of Section 1.2.2.

```latex
医学图像分割中的标注高效学习，旨在减少对完整像素级或体素级标注的依赖，同时保留完成目标分割所需的监督信息。按照标注所提供的空间范围，已有研究使用图像级标签、点、边界框、涂鸦以及部分切片标注等不同形式\cite{tajbakhsh2020imperfect}。这些标注的获取负担和信息粒度并不相同：图像级标签主要说明目标是否存在，点和涂鸦提供局部类别位置，边界框限定大致区域，而密集掩膜进一步描述完整边界和内部结构。因此，弱监督医学图像分割的核心并非简单减少标注数量，而是从不完备监督中恢复未被直接标出的空间信息。

涂鸦监督首先在自然图像语义分割中形成了标签传播的基本路线。ScribbleSup 将涂鸦标记、图像外观和网络预测纳入图模型，在传播标签至未标注像素的同时更新分割网络\cite{lin2016scribblesup}。这类方法表明，稀疏的类别位置可以与图像相似性结合形成更完整的训练目标，但传播结果依赖局部外观、边界可分性和涂鸦覆盖范围。医学图像中目标对比度、病灶形态和成像噪声的变化，使这种依赖更加需要针对具体任务进行检验。

面向医学图像的早期工作进一步研究了仅利用涂鸦训练像素级网络的可行性。Can 等比较了不同训练策略，并在心脏和前列腺分割中直接利用涂鸦像素提供监督\cite{can2018scribble}。选择性损失或部分交叉熵只在已标注位置计算分类误差，能够避免把未知像素错误地当作背景，但未标注区域只能通过共享表征和网络归纳偏置受到间接影响。当涂鸦稀疏、类别覆盖不均或目标边界复杂时，仅扩大网络容量并不能补足缺失的空间监督。

一类研究通过正则项直接约束未标注区域，而不先生成完整硬标签。Tang 等将成对关系和条件随机场等结构约束写入弱监督分割损失，使图像信息参与未标注像素的优化\cite{tang2018regularized}。Kervadec 等进一步将目标区域大小等全局不等式约束转化为可微惩罚项，用领域知识限定网络输出\cite{kervadec2019constrained}。这类方法避免把单次预测直接固定为伪真值，但其有效性取决于约束是否与具体器官、病灶和数据分布相符；过强或不准确的先验同样可能限制模型学习。

另一类研究通过多分支预测或教师模型构造伪标签，以增加被监督的像素。Luo 等采用双分支网络，并动态混合两个分支的预测作为辅助监督\cite{luo2022scribble}。DMSPS 使用动态混合的软伪标签缓解硬伪标签的过度置信问题，并依据低不确定性预测扩展稀疏涂鸦\cite{han2024dmsps}。伪标签能够扩大监督覆盖，但其信息来自当前模型或相关分支；若早期预测存在系统性偏差，错误仍可能在后续训练中被强化。因此，监督扩展需要同时控制置信度、分支相关性和噪声累积。

针对体数据和结构信息，已有方法还从切片关联、边界和特征表示等角度补充监督。Scribble2D5 将相邻切片信息、标签传播和边界预测结合，用于涂鸦监督的体数据分割\cite{chen2022scribble2d5}。Zhou 等利用超像素引导涂鸦传播，并通过类别级对比正则增强类内一致性和类间区分\cite{zhou2023scribblewalking}。这些方法说明，稀疏标签之外的图像结构和表示关系可以提供附加约束；但超像素质量、切片连续性和特征紧致性并非在所有医学目标上都同样可靠。

总体来看，已有涂鸦监督方法主要沿着选择性监督、标签传播与伪标签、一致性学习以及结构先验四条路线利用未标注区域。不同路线分别扩大监督范围、约束预测变化或补充边界和形状信息，但多数方法默认既有涂鸦本身已经足以代表目标类别。事实上，相同标注像素数在不同空间分布、类别比例和目标形态下可能提供不同的信息量；若监督位置集中于局部区域或不同类别的标注比例偏差较大，后续传播和正则化仍可能建立在不平衡的初始证据上。

ZScribbleSeg 将研究重点进一步前移至涂鸦形式本身，分析标注像素比例和空间随机性对有效监督的影响，并据此构造监督增强\cite{zhang2026zscribbleseg}。该工作通过混合和遮挡增加监督覆盖与分布变化，并利用全局一致性约束增强前后预测的对应关系。这一设计并非生成一种固定的完整伪标签，而是重组已有稀疏监督，使模型在不增加密集标注的条件下接触更广的监督位置。

对于涂鸦难以直接提供的类别比例和全局结构，ZScribbleSeg 进一步估计类别混合比例，并将其用于空间先验和形状正则化\cite{zhang2026zscribbleseg}。类别混合比例用于刻画完整图像中不同类别的潜在占比，空间先验用于从未标注区域中识别与各类别相符的像素，形状正则化则用于减少碎片化预测。该方法的作用范围是涂鸦监督医学图像分割，其贡献不构成持续学习中的知识保持机制，也不意味着一种先验可以不经验证地迁移至所有器官和病灶。

现有研究已经从稀疏损失、伪标签、表示一致性和结构正则等角度提高了涂鸦监督的可用性，但仍存在相互关联的限制：监督覆盖不足会增加模型对自身预测的依赖，伪标签误差可能随训练累积，类别标注比例偏差可能导致欠分割，而不完整的边界和形状信息容易产生结构碎片。由此，如何在不引入密集标注的前提下扩大有效监督、校正类别与空间偏差并保持结构完整性，构成后续需要解决的关键问题。
```

After insertion, verify:

- Section 1.1 is byte-for-byte unchanged.
- 1.2.2 and 1.2.3 remain body-empty.
- Section 1.3 remains body-empty.
- The 1.2.1 title and label remain unique.
- The approved prose contains only these citation keys:
  - existing: `tajbakhsh2020imperfect`;
  - new: `lin2016scribblesup`, `can2018scribble`, `tang2018regularized`, `kervadec2019constrained`, `luo2022scribble`, `han2024dmsps`, `chen2022scribble2d5`, `zhou2023scribblewalking`, `zhang2026zscribbleseg`.
- No method result number, clinical-deployment claim, or continual-learning characterization of ZScribbleSeg has been added.

## Step 2: add verified bibliography entries

Before adding an entry, check duplicate key, case-insensitive DOI, normalized title, and an equivalent verified record under another key. Reuse an equivalent record when present and change only the citation key in the approved prose.

Add only entries actually cited by the approved prose:

```bibtex
@inproceedings{lin2016scribblesup,
  author    = {Lin, Di and Dai, Jifeng and Jia, Jiaya and He, Kaiming and Sun, Jian},
  title     = {{ScribbleSup}: Scribble-Supervised Convolutional Networks for Semantic Segmentation},
  booktitle = {Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition},
  pages     = {3159--3167},
  year      = {2016},
  doi       = {10.1109/CVPR.2016.344}
}

@inproceedings{can2018scribble,
  author    = {Can, Yigit B. and Chaitanya, Krishna and Mustafa, Basil and Koch, Lisa M. and Konukoglu, Ender and Baumgartner, Christian F.},
  title     = {Learning to Segment Medical Images with Scribble-Supervision Alone},
  booktitle = {Deep Learning in Medical Image Analysis and Multimodal Learning for Clinical Decision Support},
  series    = {Lecture Notes in Computer Science},
  volume    = {11045},
  pages     = {236--244},
  publisher = {Springer},
  year      = {2018},
  doi       = {10.1007/978-3-030-00889-5_27}
}

@inproceedings{tang2018regularized,
  author    = {Tang, Meng and Perazzi, Federico and Djelouah, Abdelaziz and {Ben Ayed}, Ismail and Schroers, Christopher and Boykov, Yuri},
  title     = {On Regularized Losses for Weakly-Supervised {CNN} Segmentation},
  booktitle = {Computer Vision -- ECCV 2018},
  series    = {Lecture Notes in Computer Science},
  pages     = {524--540},
  publisher = {Springer},
  year      = {2018},
  doi       = {10.1007/978-3-030-01270-0_31}
}

@article{kervadec2019constrained,
  author  = {Kervadec, Hoel and Dolz, Jose and Tang, Meng and Granger, Eric and Boykov, Yuri and {Ben Ayed}, Ismail},
  title   = {Constrained-{CNN} Losses for Weakly Supervised Segmentation},
  journal = {Medical Image Analysis},
  volume  = {54},
  pages   = {88--99},
  year    = {2019},
  doi     = {10.1016/j.media.2019.02.009}
}

@inproceedings{luo2022scribble,
  author    = {Luo, Xiangde and Hu, Minhao and Liao, Wenjun and Zhai, Shuwei and Song, Tao and Wang, Guotai and Zhang, Shaoting},
  title     = {Scribble-Supervised Medical Image Segmentation via Dual-Branch Network and Dynamically Mixed Pseudo Labels Supervision},
  booktitle = {Medical Image Computing and Computer Assisted Intervention -- MICCAI 2022},
  series    = {Lecture Notes in Computer Science},
  pages     = {528--538},
  publisher = {Springer},
  year      = {2022},
  doi       = {10.1007/978-3-031-16431-6_50}
}

@article{han2024dmsps,
  author  = {Han, Meng and Luo, Xiangde and Xie, Xiangjiang and Liao, Wenjun and Zhang, Shichuan and Song, Tao and Wang, Guotai and Zhang, Shaoting},
  title   = {{DMSPS}: Dynamically Mixed Soft Pseudo-Label Supervision for Scribble-Supervised Medical Image Segmentation},
  journal = {Medical Image Analysis},
  volume  = {97},
  pages   = {103274},
  year    = {2024},
  doi     = {10.1016/j.media.2024.103274}
}

@inproceedings{chen2022scribble2d5,
  author    = {Chen, Qiuhui and Hong, Yi},
  title     = {{Scribble2D5}: Weakly-Supervised Volumetric Image Segmentation via Scribble Annotations},
  booktitle = {Medical Image Computing and Computer Assisted Intervention -- MICCAI 2022},
  series    = {Lecture Notes in Computer Science},
  pages     = {234--243},
  publisher = {Springer},
  year      = {2022},
  doi       = {10.1007/978-3-031-16452-1_23}
}

@inproceedings{zhou2023scribblewalking,
  author    = {Zhou, Meng and Xu, Zhe and Zhou, Kang and Tong, Raymond Kai-Yu},
  title     = {Weakly Supervised Medical Image Segmentation via Superpixel-Guided Scribble Walking and Class-Wise Contrastive Regularization},
  booktitle = {Medical Image Computing and Computer Assisted Intervention -- MICCAI 2023},
  series    = {Lecture Notes in Computer Science},
  volume    = {14221},
  pages     = {137--147},
  publisher = {Springer},
  year      = {2023},
  doi       = {10.1007/978-3-031-43895-0_13}
}

@article{zhang2026zscribbleseg,
  author  = {Zhang, Ke and Wang, Bomin and Zhou, Hangqi and Zhuang, Xiahai},
  title   = {{ZScribbleSeg}: A Comprehensive Segmentation Framework with Modeling of Efficient Annotation and Maximization of Scribble Supervision},
  journal = {Medical Image Analysis},
  volume  = {112},
  pages   = {104074},
  year    = {2026},
  doi     = {10.1016/j.media.2026.104074}
}
```

Confirm that `config/build_flags.tex` remains `\thesisbibliographytrue`.

## Step 3: append evidence records

Append the following rows to `evidence/claims.csv` after checking that each ID is absent:

```csv
C1-030,1,1.2.1,弱监督医学图像分割使用图像级点框涂鸦和部分切片等不同信息粒度的标注,DOI:10.1016/j.media.2020.101693,Review taxonomy,tajbakhsh2020imperfect,literature,confirmed,drafted,用于界定标注形式差异而不主张彼此等价
C1-031,1,1.2.1,ScribbleSup通过图模型联合进行涂鸦标签传播和网络参数学习,DOI:10.1109/CVPR.2016.344,Abstract and method overview,lin2016scribblesup,method,confirmed,drafted,自然图像语义分割原始工作
C1-032,1,1.2.1,医学图像分割网络可以仅利用涂鸦像素上的监督进行训练,DOI:10.1007/978-3-030-00889-5_27,Abstract and training strategies,can2018scribble,primary_experiment,confirmed,drafted,结论限于该心脏与前列腺分割研究
C1-033,1,1.2.1,结构正则项可直接写入弱监督分割损失以利用未标注区域信息,DOI:10.1007/978-3-030-01270-0_31,Method formulation,tang2018regularized,method,confirmed,drafted,不声称所有结构约束均适用于医学目标
C1-034,1,1.2.1,全局不等式约束可通过可微惩罚项限制弱监督医学分割输出,DOI:10.1016/j.media.2019.02.009,Abstract and formulation,kervadec2019constrained,method,confirmed,drafted,目标大小仅为原文示例之一
C1-035,1,1.2.1,双分支预测可动态混合形成涂鸦监督医学分割的辅助伪标签,DOI:10.1007/978-3-031-16431-6_50,Abstract and method overview,luo2022scribble,method,confirmed,drafted,用于归纳伪标签扩展路线
C1-036,1,1.2.1,DMSPS使用动态混合软伪标签并按低不确定性预测扩展涂鸦,DOI:10.1016/j.media.2024.103274,Abstract,han2024dmsps,method,confirmed,drafted,不写入实验数值
C1-037,1,1.2.1,Scribble2D5结合相邻切片信息标签传播和边界预测处理体数据涂鸦监督,DOI:10.1007/978-3-031-16452-1_23,Abstract and method overview,chen2022scribble2d5,method,confirmed,drafted,用于说明体数据结构利用
C1-038,1,1.2.1,超像素引导涂鸦传播和类别级对比正则可联合利用图像结构与表示关系,DOI:10.1007/978-3-031-43895-0_13,Abstract and method overview,zhou2023scribblewalking,method,confirmed,drafted,不扩展为所有超像素方法结论
C1-039,1,1.2.1,伪标签扩大监督范围的同时可能继承并强化模型早期预测误差,author synthesis based on pseudo-label methods,Section synthesis,luo2022scribble;han2024dmsps,author_analysis,confirmed,drafted,采用审慎表述
C1-040,1,1.2.1,有效涂鸦监督与标注像素比例空间覆盖和随机性有关,DOI:10.1016/j.media.2026.104074,Abstract introduction and efficient-scribble analysis,zhang2026zscribbleseg,method,confirmed,drafted,属于ZScribbleSeg对标注形式的研究范围
C1-041,1,1.2.1,ZScribbleSeg通过监督增强全局一致性类别混合比例空间先验和形状正则利用稀疏监督,DOI:10.1016/j.media.2026.104074,Abstract and framework overview,zhang2026zscribbleseg,method,confirmed,drafted,仅概括机制不写公式或结果
C1-042,1,1.2.1,涂鸦监督现有不足集中于监督覆盖伪标签噪声类别比例偏差及边界形状缺失,author synthesis based on section sources,Section synthesis,tajbakhsh2020imperfect;luo2022scribble;han2024dmsps;zhang2026zscribbleseg,author_analysis,confirmed,drafted,用于过渡至1.3.1且不解释为持续学习
```

Validate with a CSV parser:

- every row has exactly 11 columns;
- claim IDs `C1-030` through `C1-042` each occur exactly once;
- no existing row is changed;
- all citation keys exist in the active bibliography.

## Step 4: terminology and section status

### 4.1 Add terminology rows

Add the following non-duplicate rows to `qa/terminology.csv`:

```csv
partial cross-entropy,部分交叉熵,第一章与第三章,局部交叉熵（避免混用）,只在有标注像素上计算监督误差
label propagation,标签传播,第一章与第三章,标注传播（避免混用）,依据图像或特征关系将稀疏标签扩展至未标注区域
pseudo label,伪标签,第一章与第三章,伪真值（避免作为首选）,由模型或辅助过程产生的训练目标
soft pseudo-label,软伪标签,第一章与第三章,软标签（范围更宽）,保留类别概率而非仅使用硬类别的伪标签
consistency regularization,一致性正则化,第一章与第三章,一致性损失（仅指具体损失时使用）,约束相关输入变换或预测分支的输出保持对应
annotation expansion,标注扩展,第一章与第三章,标签扩充（避免混用）,依据可靠预测增加可用于监督的位置
efficient scribble,高效涂鸦,第一章与第三章,高效标注（范围更宽）,指在有限标注努力下提高监督覆盖与空间随机性的涂鸦形式
```

### 4.2 Update existing terminology scopes

Update only the `scope` field of these existing rows:

- `annotation-efficient learning` → `第一章与第三章`
- `weakly supervised segmentation` → `第一章与第三章`
- `scribble supervision` → `第一章与第三章`
- `supervision augmentation` → `第一章与第三章`
- `global consistency` → `第一章与第三章`
- `class mixture ratio` → `第一章与第三章`
- `spatial prior` → `第一章与第三章`
- `shape regularization` → `第一章与第三章`

Do not change preferred wording, avoid-fields, or notes. Validate the file with a CSV parser and confirm exactly 5 columns per row and unique English keys.

### 4.3 Update `qa/chapter_status.csv`

Insert subsection rows if absent and set:

- `1.2` → `in_progress`, artifact `chapters/ch01_introduction.tex`
- `1.2.1` → `drafted_and_verified`, artifact `chapters/ch01_introduction.tex`
- `1.2.2` → `queued`
- `1.2.3` → `not_started`

Preserve the existing header and schema.

### 4.4 Update `STATE.md`

Record accurately:

- Section 1.1 remains complete and unchanged;
- 1.2.1 has been integrated, referenced, compiled, audited, and visually checked;
- Section 1.2 is in progress;
- the next target is 1.2.2 “医学影像持续学习研究现状”;
- no 1.2.2 or 1.2.3 prose was drafted;
- exact build, audit, PDF, GitHub, and Overleaf results;
- all non-fatal warnings and unresolved source issues.

Do not add an approved voice example to `AUTHOR_VOICE.md`.

## Step 5: compile, audit, and verify

Run:

```bash
latexmk -xelatex -interaction=nonstopmode -file-line-error main.tex
```

Then:

```bash
python scripts/style_audit.py \
  --input chapters/ch01_introduction.tex \
  --patterns qa/style_red_flags.csv \
  --output qa/style_audit_report.md
```

If reference-thesis `.tex` files exist:

```bash
python scripts/reference_overlap_audit.py \
  --thesis chapters/ch01_introduction.tex \
  --reference sources/reference_thesis \
  --min-chars 28 \
  --output qa/reference_overlap_report.md
```

Check and report:

1. full build exit code;
2. actual BibTeX execution;
3. citation resolution for all active Chapter 1 citations;
4. no duplicate bibliography key, DOI, or normalized title;
5. no undefined citation/reference;
6. no duplicate label;
7. no missing input, figure, class, or bibliography file;
8. no new `TODO`, `TBD`, or `??`;
9. `git diff --check`;
10. claims CSV integrity and unique IDs;
11. terminology CSV integrity and unique keys;
12. Section 1.1 byte-for-byte unchanged;
13. 1.2.2, 1.2.3, and Section 1.3 remain body-empty;
14. no continual-learning characterization of ZScribbleSeg;
15. style-audit result;
16. reference-overlap result;
17. unchanged `sources/` file count and hash;
18. PDF visual inspection of every page containing 1.2.1 and every updated bibliography page;
19. final PDF page count, byte size, and SHA-256;
20. distinction between pre-existing warnings and task-introduced warnings.

Do not alter approved prose to hide a harmless page break or box warning.

## Step 6: handoff report

Replace `handoff/LATEST_CODEX_REPORT.md` with a complete report containing:

- task name and timestamp;
- baseline commit and repository preflight;
- exact modified files;
- confirmation of exact prose integration;
- hashes proving Section 1.1 and untouched empty sections were preserved;
- bibliography entries added or reused and duplicate checks;
- evidence and terminology changes;
- status and state changes;
- compile command and full result;
- citation/reference/label/input/placeholder/CSV checks;
- style and overlap audits;
- visual inspection pages and result;
- before/after `sources/` snapshot;
- unresolved scientific, source, bibliography, style, or layout issues;
- GitHub content commit;
- Overleaf deployment commit or exact non-bypassed failure;
- confirmation that the next target is 1.2.2 and that it was not drafted.

## Step 7: commit, push, and synchronize

Do not force-push.

After all checks:

```bash
git diff --check
git status --short
```

Stage only permitted files. Create a content commit, for example:

```bash
git commit -m "Draft Chapter 1 Section 1.2.1"
git push origin main
```

Verify the content commit on `origin/main`. Only after the push succeeds and the worktree is clean, run:

```bash
bash scripts/sync_latex_to_overleaf.sh "Sync Chapter 1 Section 1.2.1"
```

Record the exact Overleaf SHA. If recording deployment creates a GitHub-only report change:

```bash
git add handoff/LATEST_CODEX_REPORT.md STATE.md
git commit -m "Record Chapter 1.2.1 deployment"
git push origin main
```

Do not re-run Overleaf synchronization for a report-only commit.

At the end:

```bash
git status --short
git rev-parse HEAD
git rev-parse origin/main
```

The worktree must be clean and local `HEAD` must match `origin/main`.

## Definition of done

Complete only when:

- 1.2.1 approved prose is integrated exactly;
- Section 1.1 is unchanged;
- 1.2.2, 1.2.3, and Section 1.3 remain body-empty;
- all verified cited references are added or reused without duplicates;
- `C1-030` through `C1-042` occur exactly once;
- terminology additions and scope updates are valid;
- 1.2.1 is `drafted_and_verified`;
- full compilation and all audits pass or exact non-bypassed failures are reported;
- PDF pages are visually inspected;
- `sources/` is unchanged;
- verified content is pushed to GitHub and the LaTeX subset is synchronized to Overleaf;
- the next target is 1.2.2 and no 1.2.2 prose has been drafted.

Do not continue beyond Section 1.2.1 in this task.
