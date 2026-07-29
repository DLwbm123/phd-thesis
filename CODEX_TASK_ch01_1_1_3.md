# Codex Task: integrate Chapter 1, Section 1.1.3

Read and obey `AGENTS.md`, `THESIS_CONTRACT.md`, `AUTHORSHIP_PROTOCOL.md`, `AUTHOR_VOICE.md`, `STATE.md`, `PROJECT_CONFIG.md`, and `chapter_cards/ch01.md` before editing.

## Goal

Integrate the GPT Pro-approved draft for Section 1.1.3 “数据分布与医学任务的持续演化” into the thesis repository, add only the verified references, evidence records, and terminology entries supplied below, compile and inspect the complete thesis, run all required audits, push the verified work to `origin/main`, and synchronize the compilable LaTeX subset to Overleaf.

This subsection must complete the conceptual chain of Section 1.1:

1. Section 1.1.1 established the functions and data dependence of medical image classification, segmentation, and registration.
2. Section 1.1.2 distinguished limitations on annotation acquisition, historical-data access, and cross-center raw-data sharing.
3. Section 1.1.3 must now explain how the data-generating distribution and the medical task itself may change over time, and why this creates distinct requirements for knowledge retention, new-task learning, and cross-task generalization.

The subsection is background and motivation. It must not become a detailed method review, a formal benchmark specification, or an early version of Sections 1.2, 1.3, or Chapters 4--6.

## Strict scientific boundaries

- Do not state or imply that all clinical data streams are continuously changing.
- Do not equate any static domain difference, multi-center dataset, or external-validation gap with continual learning.
- A domain difference becomes a domain-incremental continual-learning setting only when domains are encountered sequentially, the model is updated across stages, and earlier-domain capability remains part of the objective.
- Do not call poor first-time performance on an unseen external institution “catastrophic forgetting.” Forgetting requires a previously acquired capability that declines after subsequent learning.
- Do not claim that task-incremental, domain-incremental, and class-incremental learning mechanically cover every medical imaging problem without additional assumptions.
- Do not present “organ-incremental learning” as a universally standardized category. When organs or targets are added, the scenario depends on the output space, model head, context assumptions, and evaluation protocol.
- Do not mechanically describe continual medical image registration as class-incremental learning. Its scenario must be defined through the changing image domains, registration objects, and input--output mapping.
- Do not assume that real medical data streams always have sharp task boundaries or that task/context identity is always available.
- Do not describe continual learning as autonomous online clinical deployment, regulatory approval, or permission to update a deployed diagnostic model without validation.
- Do not claim that replay-free learning is universally required by privacy law or that all institutions must delete historical patient data.
- Do not describe ZScribbleSeg, weak supervision, or annotation-efficient learning as continual learning.
- Do not claim that federated learning or federated continual learning provides a formal privacy guarantee.
- Do not introduce the detailed algorithms, equations, experimental numbers, or claimed contributions of the four thesis works.
- Do not begin the literature review in Section 1.2 or add prose under its subsections.
- Do not copy, translate, paraphrase, or import prose, citations, figures, bibliography combinations, metadata, or personal information from `sources/reference_thesis/`.

## Strict file scope

Files that may be modified or added:

- `CODEX_TASK_ch01_1_1_3.md` — preserve this task file exactly if it is placed in the repository; add it as task provenance if untracked
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

Do not modify any file under `sources/`. Do not modify another chapter, a template/class file, figure, table, script, bibliography style, or the approved prose of Sections 1.1.1 and 1.1.2. Build products and ordinary LaTeX auxiliary files may be regenerated locally but must not be committed if excluded by `.gitignore`.

Do not rewrite the approved academic prose except for a strictly necessary LaTeX syntax correction or replacement of a citation key when an equivalent verified bibliography record already exists under a different key. If a scientific, factual, stylistic, or layout concern is found, report it rather than silently rewriting the prose.

## Step 0: repository and baseline preflight

Before editing:

1. Run:

   ```bash
   git status --short
   git branch --show-current
   git fetch origin
   ```

2. The worktree must be clean except that `CODEX_TASK_ch01_1_1_3.md` may be the only untracked file.
3. Confirm that the current branch is `main`.
4. Confirm that local `HEAD` is not behind or divergent from `origin/main`.
   - If `origin/main` is ahead and the worktree is otherwise clean, use `git pull --ff-only origin main`.
   - If the histories diverge or unrelated local modifications exist, stop and report the exact state. Do not overwrite, reset, rebase, or force-push.
5. Record the exact baseline commit SHA.
6. Confirm in `chapters/ch01_introduction.tex` that:
   - Section 1.1.1 is present and has status `drafted_and_verified`;
   - Section 1.1.2 is present and has status `drafted_and_verified`;
   - `\raggedbottom` is already present and must not be removed without explicit authorization;
   - the title and label for 1.1.3 already exist;
   - the body between `\label{subsec:intro-evolving-tasks}` and `\section{国内外研究现状}` is empty;
   - Section 1.2 and its subsection titles are present but contain no body text.
7. Save byte-for-byte hashes of the approved bodies of Sections 1.1.1 and 1.1.2 so that the final report can prove they were unchanged.
8. Confirm that `bibliography/references.bib` currently contains ten verified records:
   - six records used by 1.1.1;
   - four additional records used by 1.1.2.
9. Confirm that `config/build_flags.tex` contains:

   ```latex
   \thesisbibliographytrue
   ```

10. Confirm that `evidence/claims.csv` currently ends its Chapter 1 sequence at `C1-016`.
11. Confirm that `qa/chapter_status.csv` records:
    - 1.1.1 → `drafted_and_verified`;
    - 1.1.2 → `drafted_and_verified`;
    - 1.1.3 → `queued`.
12. Record a read-only snapshot or deterministic hash of `sources/`, including the file count, so the final report can prove that no source file was changed.

## Step 1: integrate the approved draft exactly

In `chapters/ch01_introduction.tex`, preserve the existing subsection title and label:

```latex
\subsection{数据分布与医学任务的持续演化}
\label{subsec:intro-evolving-tasks}
```

Insert the following approved text immediately after that label and before:

```latex
\section{国内外研究现状}
```

Approved text:

```latex
上一节讨论的是模型在特定训练阶段能够获得哪些图像、标签和历史信息，本节进一步关注这些信息所描述的数据分布与任务目标是否保持不变。传统离线学习通常在预先汇集的训练集上完成一次优化，并默认后续应用面对与既定任务相对稳定的输入--输出关系。医学影像数据却可能按时间、机构或项目批次持续到达，患者构成、疾病谱、成像条件和分析目标也可能随之改变。当模型需要在顺序数据上更新并把新信息纳入已有能力时，训练对象由固定数据集转变为非平稳数据流，持续学习由此成为区别于一次性离线训练的问题设定\cite{hadsell2020embracing,vandeven2022three}。这种演化改变模型需要适应的目标，而上一节所述信息限制决定模型在适应过程中能够使用哪些证据，二者相关但不等同。

数据分布演化首先可以表现为输入域变化，而任务输出的语义保持不变。不同患者人群、医疗中心、设备、扫描序列、重建算法和采集协议会改变医学图像的外观与统计特征。Dewey 等在磁共振成像研究中指出，硬件、软件或扫描协议变化可能影响定量结果，并在纵向多发性硬化症数据上观察到协议变化对脑萎缩计算的影响\cite{dewey2019deepharmony}。Zech 等的多机构胸部 X 射线实验也表明，原机构内部的模型表现不能直接代表其在外部机构的表现\cite{zech2018variable}。这些结果说明，即使标签集合和临床问题没有变化，输入分布改变仍可能削弱固定模型的适用性。

域差异本身并不自动构成持续学习问题。若来自多个中心或设备的数据在同一训练阶段同时可用，问题仍可在静态多域条件下处理；只有当不同域按顺序出现，模型在接收新域数据并持续更新后还需维持旧域能力时，才形成域增量学习。因此，判断一个医学影像问题是否属于持续学习，不能只看数据是否来自不同中心或设备，还需说明数据的到达顺序、每一阶段的访问范围以及模型是否发生连续更新。

医学任务的演化还可能改变输出空间或输入--输出映射。新的疾病类别会扩展分类标签集合，新增器官或病灶目标会改变分割对象，新的模态组合或解剖区域也会改变配准模型需要估计的对应关系。监督式持续学习通常区分任务增量、域增量和类增量三类基本场景：任务增量学习面向可区分任务的顺序学习，域增量学习保持输出语义而改变上下文或输入分布，类增量学习则要求模型逐步扩展统一判别的类别集合\cite{vandeven2022three}。在医学图像分割中，新增器官究竟被视为新类别还是新任务，取决于输出头是否共享、测试时是否提供上下文身份以及不同阶段是否要求统一预测；对于输出为形变场的医学图像配准，也需根据输入域和映射目标定义场景，而不宜机械套用类增量设定。

真实演化过程未必由边界清晰且互不重叠的任务组成。患者构成和疾病比例可以逐渐变化，既有设备或中心可能再次出现，域、类别、器官、模态和任务目标等因素还可能同时改变。van de Ven 等指出，持续学习的数据流可以包含上下文的渐变、重访以及多维变化的混合情形\cite{vandeven2022three}。因此，任务序列应描述具有实际含义的数据生成变化，而不能仅把静态数据集任意切分后即视为临床持续演化；实验设定至少需要交代阶段划分、边界是否可见、标签空间如何变化以及测试时能否获得上下文身份。

顺序更新带来的核心困难之一是灾难性遗忘。深度模型在新任务或新分布上继续优化时，共享参数的改变可能降低其在先前任务上的性能\cite{delange2022continual,vandeven2022three}。遗忘是相对于更新过程定义的概念：模型需要先在旧任务上形成能力，随后该能力在学习新信息后发生下降。若模型从未学习某个外部中心的数据，并在首次测试时表现较差，这属于跨域泛化不足，而不是灾难性遗忘。区分两者可以避免把静态外部验证结果与顺序学习中的知识损失混为同一现象。

持续学习的目标也不能简化为只保持旧任务性能。模型需要在保留既有能力的同时有效吸收当前任务信息，这对应稳定性与可塑性的共同要求。过强地限制参数变化可能保护旧知识，却压低新任务的学习幅度；只依据当前数据自由更新又可能破坏先前形成的表示。这一稳定性--可塑性权衡贯穿持续学习方法设计\cite{hadsell2020embracing,delange2022continual}。不同医学任务之间既可能共享解剖或表征信息，也可能产生优化冲突，因此合理目标不是使模型在后续阶段保持不变，而是在明确资源条件下协调知识保护与任务适应。

相应地，持续医学影像学习需要多维评价。旧任务性能及其随阶段的变化反映知识保持，当前任务达到的性能反映新知识学习；已有知识能否促进后续任务学习涉及前向迁移，模型在尚未参与优化的任务或域上的表现则涉及前向泛化。仅报告最终平均性能可能掩盖不同阶段的退化，仅报告遗忘也无法判断模型是否真正学会了新任务。评价还应同时说明历史样本访问、存储开销、参数增长和通信条件，因为在完整联合训练、有限回放和无回放设定下，相同数值对应的问题难度并不一致\cite{vandeven2022three,delange2022continual}。

数据与任务演化可以同上一节的训练信息限制叠加。在集中式环境中，完整历史数据、有限回放和无回放对应不同的知识保护条件；在跨医疗中心环境中，原始数据不能集中与客户端任务顺序演化还会共同形成联邦持续学习设定\cite{delange2022continual,rieke2020future}。这些组合不改变前述概念边界：有限回放描述历史数据访问条件，联邦学习描述跨中心协同方式，二者都不能单独定义数据或任务是否发生持续演化，也不自动提供形式化隐私保证。

由此，医学影像学习需要同时面对静态任务中的监督不足，以及动态任务中的知识保持、新知识学习和跨任务泛化。前者形成标注高效与弱监督医学图像分割问题，后者进一步形成集中式和联邦式持续医学影像学习问题。下一节将分别梳理上述研究方向的国内外进展，并在此基础上归纳现有方法尚未解决的关键技术挑战。
```

After insertion, verify all of the following:

- Sections 1.1.1 and 1.1.2 are byte-for-byte unchanged relative to the preflight hashes.
- `\raggedbottom` remains present and unchanged.
- The 1.1.3 subsection title and label remain unique.
- No body text is added under Section 1.2 or any of its subsections.
- The approved text contains exactly these six distinct citation keys:
  - existing: `zech2018variable`, `delange2022continual`, `rieke2020future`;
  - new: `hadsell2020embracing`, `vandeven2022three`, `dewey2019deepharmony`.
- The em-dash and Chinese punctuation remain Unicode text, while LaTeX mathematical or compound-word dashes remain valid (`--` where supplied).
- No prose is silently “improved,” shortened, expanded, or rearranged.

## Step 2: add the verified bibliography entries

The following metadata was verified by GPT Pro against primary publisher or index records:

- Hadsell et al., official ScienceDirect record, DOI `10.1016/j.tics.2020.09.004`, volume 24(12), pages 1028--1040.
- van de Ven et al., official Nature Machine Intelligence record, DOI `10.1038/s42256-022-00568-3`, volume 4, pages 1185--1197.
- Dewey et al., PubMed/PMC and publisher metadata, PMID `31301354`, DOI `10.1016/j.mri.2019.05.041`, volume 64, pages 160--170.

Before adding each entry, check `bibliography/references.bib` for:

1. duplicate key;
2. duplicate DOI, case-insensitively;
3. duplicate normalized title;
4. an equivalent verified record under a different key.

Add the following entries only when no equivalent record exists. Preserve all ten existing verified records. If an equivalent record exists under another key, reuse it and change only the corresponding `\cite{}` key in the approved text.

```bibtex
@article{hadsell2020embracing,
  author  = {Hadsell, Raia and Rao, Dushyant and Rusu, Andrei A. and Pascanu, Razvan},
  title   = {Embracing Change: Continual Learning in Deep Neural Networks},
  journal = {Trends in Cognitive Sciences},
  volume  = {24},
  number  = {12},
  pages   = {1028--1040},
  year    = {2020},
  doi     = {10.1016/j.tics.2020.09.004}
}

@article{vandeven2022three,
  author  = {{van de Ven}, Gido M. and Tuytelaars, Tinne and Tolias, Andreas S.},
  title   = {Three Types of Incremental Learning},
  journal = {Nature Machine Intelligence},
  volume  = {4},
  pages   = {1185--1197},
  year    = {2022},
  doi     = {10.1038/s42256-022-00568-3}
}

@article{dewey2019deepharmony,
  author  = {Dewey, Blake E. and Zhao, Can and Reinhold, Jacob C. and Carass, Aaron and Fitzgerald, Kathryn C. and Sotirchos, Elias S. and Saidha, Shiv and Oh, Jiwon and Pham, Dzung L. and Calabresi, Peter A. and {van Zijl}, Peter C. M. and Prince, Jerry L.},
  title   = {{DeepHarmony}: A Deep Learning Approach to Contrast Harmonization across Scanner Changes},
  journal = {Magnetic Resonance Imaging},
  volume  = {64},
  pages   = {160--170},
  year    = {2019},
  doi     = {10.1016/j.mri.2019.05.041}
}
```

Confirm that `config/build_flags.tex` remains:

```latex
\thesisbibliographytrue
```

Do not add any reference that is not cited by the approved text. Do not import a bibliography collection from any source project or reference thesis.

## Step 3: append evidence records

Append the following rows to `evidence/claims.csv` after checking that the claim IDs do not already exist:

```csv
C1-017,1,1.1.3,持续学习区别于固定数据集离线训练之处在于模型从顺序到达的非平稳数据流中增量学习,DOI:10.1016/j.tics.2020.09.004;DOI:10.1038/s42256-022-00568-3,Highlights abstract and scenario definition,hadsell2020embracing;vandeven2022three,literature,confirmed,drafted,用于界定持续学习而不延伸到临床在线部署
C1-018,1,1.1.3,磁共振扫描硬件软件或协议变化可能影响定量结果并干扰纵向脑萎缩计算,DOI:10.1016/j.mri.2019.05.041,Abstract and longitudinal analysis,dewey2019deepharmony,primary_experiment,confirmed,drafted,结论限于该磁共振协议变化与多发性硬化症纵向研究
C1-019,1,1.1.3,多机构胸部X射线研究中原机构内部模型表现不能直接代表外部机构表现,DOI:10.1371/journal.pmed.1002683,Abstract and cross-institution evaluation,zech2018variable,primary_experiment,confirmed,drafted,用于说明静态跨机构域差异而不将其直接定义为遗忘
C1-020,1,1.1.3,静态域差异只有在域按顺序到达模型持续更新且旧域能力仍需保持时才构成域增量学习,author scope definition based on continual-learning scenarios,Section distinction,vandeven2022three,author_definition,confirmed,drafted,用于区分静态跨域问题与持续学习
C1-021,1,1.1.3,监督式持续学习可按待学习映射与上下文关系区分任务增量域增量和类增量场景,DOI:10.1038/s42256-022-00568-3,Abstract and scenario definitions,vandeven2022three,literature,confirmed,drafted,不声称三类场景可在无附加假设时覆盖所有医学任务
C1-022,1,1.1.3,医学分割中的新增器官属于新类别还是新任务取决于输出空间上下文身份和统一预测要求,author synthesis based on scenario definitions,Section medical-task interpretation,vandeven2022three,author_analysis,confirmed,drafted,不把器官增量表述为无条件标准类别
C1-023,1,1.1.3,持续学习数据流可以包含上下文渐变重访以及多维变化的混合情形,DOI:10.1038/s42256-022-00568-3,Generalization to flexible settings,vandeven2022three,literature,confirmed,drafted,用于限制边界清晰离散任务假设
C1-024,1,1.1.3,任意切分静态数据集不足以证明任务序列具有临床持续演化含义,author scope definition,Section benchmark boundary,vandeven2022three,author_definition,confirmed,drafted,任务阶段应对应可解释的数据生成或目标变化
C1-025,1,1.1.3,灾难性遗忘是模型学习新任务或新分布后先前已获得能力发生下降,DOI:10.1109/TPAMI.2021.3057446;DOI:10.1038/s42256-022-00568-3,Survey definition and main text,delange2022continual;vandeven2022three,literature,confirmed,drafted,定义依赖先学习后下降的顺序过程
C1-026,1,1.1.3,模型首次面对未学习外部域时表现较差属于泛化不足而不是灾难性遗忘,author scope definition,Section distinction,zech2018variable;delange2022continual,author_definition,confirmed,drafted,用于区分外部验证与顺序更新后的知识损失
C1-027,1,1.1.3,持续学习需协调旧知识保持与新任务学习形成稳定性可塑性权衡,DOI:10.1016/j.tics.2020.09.004;DOI:10.1109/TPAMI.2021.3057446,Review discussion and survey taxonomy,hadsell2020embracing;delange2022continual,literature,confirmed,drafted,不将目标简化为参数完全不变
C1-028,1,1.1.3,持续医学影像学习评价应同时考虑知识保持当前任务学习前向迁移前向泛化及资源条件,author synthesis based on continual-learning requirements,Section evaluation synthesis,vandeven2022three;delange2022continual,author_analysis,confirmed,drafted,具体指标定义和公式留待后续章节
C1-029,1,1.1.3,数据任务演化可与有限回放无回放及跨中心协同条件叠加但这些条件不能单独定义演化,author synthesis based on access and collaboration settings,Section synthesis,delange2022continual;rieke2020future,author_analysis,confirmed,drafted,用于形成集中式与联邦式持续学习的共同背景且不声称形式化隐私
```

Preserve the existing CSV header and the exact 11-column schema. Validate every row with a real CSV parser. Confirm:

- claim IDs `C1-017` through `C1-029` each occur exactly once;
- every row has exactly 11 columns;
- no existing claim is changed;
- semicolon-separated DOI or citation lists remain within one CSV field;
- commas, if introduced by a necessary correction, are handled by CSV quoting rather than by changing the scientific meaning.

## Step 4: terminology and writing status

### 4.1 Add terminology rows

Add the following non-duplicate rows to `qa/terminology.csv`:

```csv
data distribution evolution,数据分布演化,第一章与第四至六章,数据漂移（范围不完全等同）,指数据生成分布随顺序阶段发生变化
task evolution,任务演化,第一章与第四至六章,任务变化（可作一般解释）,指输出空间输入输出映射或任务目标随阶段变化
non-stationary data stream,非平稳数据流,第一章与第四至六章,动态数据流（可作解释但非首选）,指数据分布或任务关系随时间或阶段变化的数据流
domain shift,域偏移,第一章与第四至六章,领域偏移（避免混用）,静态域差异不自动等同于持续学习
task-incremental learning,任务增量学习,第一章与第四至六章,任务递增学习（避免混用）,可区分任务按顺序到达且测试阶段上下文身份假设必须明确
domain-incremental learning,域增量学习,第一章与第四至六章,领域增量学习（避免混用）,输出语义保持而输入域或上下文按顺序变化
class-incremental learning,类增量学习,第一章与第四至六章,类别增量学习（避免混用）,标签空间随阶段扩展且通常要求统一判别
context identity,上下文身份,第一章与第四至六章,任务标签（两者不总等同）,指模型在训练或测试时是否获知样本所属域或任务上下文
```

### 4.2 Update existing terminology scopes without changing preferred wording

The approved 1.1.3 text now uses several terms already registered only for Chapters 4--6. Update only the `scope` field of the existing rows as follows:

- `continual learning` → `第一章与第四至六章`
- `catastrophic forgetting` → `第一章与第四至六章`
- `stability-plasticity trade-off` → `第一章与第四至六章`
- `forward transfer` → `第一章与第四至六章`
- `forward generalization` → `第一章与第四至六章`

Do not create duplicate rows and do not change their preferred Chinese terms, avoid-fields, or notes unless a CSV syntax correction is strictly required.

Validate `qa/terminology.csv` with a CSV parser and confirm every row has exactly 5 columns.

### 4.3 Update chapter status

Update `qa/chapter_status.csv`:

- `1.1.3` → `drafted_and_verified`, artifact `chapters/ch01_introduction.tex`
- `1.2` → `queued`
- do not change the status of another section unless required to preserve the CSV schema.

Update `STATE.md` so that it accurately records:

- Sections 1.1.1, 1.1.2, and 1.1.3 are integrated and verified;
- Section 1.1 “研究背景及意义” is complete at the current draft stage;
- the next writing target is 1.2.1 “标注高效与弱监督医学图像分割研究现状” under Section 1.2;
- the exact build, citation, audit, and visual-inspection outcome;
- any non-fatal layout, bibliography, template, or source warning;
- the GitHub and Overleaf synchronization state after Step 7.

Do not add an approved voice example to `AUTHOR_VOICE.md`. That file is updated only after the author personally revises and confirms representative prose.

## Step 5: compile, audit, and verify

Run the complete build:

```bash
latexmk -xelatex -interaction=nonstopmode -file-line-error main.tex
```

Then run the style audit:

```bash
python scripts/style_audit.py \
  --input chapters/ch01_introduction.tex \
  --patterns qa/style_red_flags.csv \
  --output qa/style_audit_report.md
```

If `sources/reference_thesis/` contains reference-thesis `.tex` files, run:

```bash
python scripts/reference_overlap_audit.py \
  --thesis chapters/ch01_introduction.tex \
  --reference sources/reference_thesis \
  --min-chars 28 \
  --output qa/reference_overlap_report.md
```

Perform and report all of the following checks:

1. The full thesis compiles with exit code 0.
2. BibTeX actually runs or the existing bibliography is correctly reused by `latexmk`.
3. The active bibliography contains thirteen verified records after this task unless an equivalent record was reused:
   - ten existing records from 1.1.1 and 1.1.2;
   - three verified records from this task.
4. Every citation used in Sections 1.1.1--1.1.3 resolves in the active `.bib` and generated `.bbl`.
5. No undefined citation or cross-reference is introduced.
6. No duplicate bibliography key, DOI, or normalized title exists.
7. No duplicate LaTeX label is introduced.
8. No required input, class file, bibliography file, or figure is missing.
9. No new `TODO`, `TBD`, or `??` appears in active thesis inputs.
10. `git diff --check` passes.
11. `evidence/claims.csv` remains parseable with exactly 11 columns per row and unique claim IDs.
12. `qa/terminology.csv` remains parseable with exactly 5 columns per row and unique English-term keys.
13. Sections 1.1.1 and 1.1.2 remain byte-for-byte unchanged.
14. `\raggedbottom` remains unchanged.
15. The 1.1.3 title and label remain unchanged and unique.
16. No body text is added to Section 1.2.
17. The prose does not equate static domain shift with continual learning.
18. The prose does not call first-time external-domain failure catastrophic forgetting.
19. The prose does not present organ-incremental learning as a universally fixed category.
20. The prose does not present replay-free learning as a universal legal requirement.
21. The prose does not present federated learning as a formal privacy guarantee.
22. The style-audit result is reported rather than silently fixed through unauthorized rewriting.
23. The reference-overlap result is reported and no superficial paraphrasing is used to conceal overlap.
24. The `sources/` snapshot, file count, and hash are unchanged.
25. Render and visually inspect every PDF page containing 1.1.3 and every updated bibliography page for:
    - Chinese character rendering;
    - citation rendering and ordering;
    - paragraph breaks;
    - overfull or clipped text;
    - unusual blank areas;
    - heading placement;
    - overlap or missing content;
    - continuity from 1.1.2 into 1.1.3 and from 1.1.3 to the empty Section 1.2.
26. Record the final PDF page count, byte size, and SHA-256 in the handoff report.
27. Compare the final page count and layout warnings with the 1.1.2 baseline and distinguish pre-existing warnings from warnings introduced by this task.

A non-fatal warning may be reported without unauthorized template changes. Do not change approved prose merely to hide a harmless page break, underfull box, or pre-existing template warning.

## Step 6: write the Codex handoff report

Replace `handoff/LATEST_CODEX_REPORT.md` with a complete report containing:

1. task name and execution timestamp;
2. baseline Git commit and repository preflight result;
3. exact modified and added files;
4. confirmation that the approved 1.1.3 prose was integrated without unauthorized rewriting;
5. hashes proving that Sections 1.1.1 and 1.1.2 were unchanged;
6. exact bibliography entries added or reused and duplicate checks performed;
7. evidence rows `C1-017` through `C1-029`;
8. terminology rows added and existing terminology scopes updated;
9. chapter-status and `STATE.md` updates;
10. compile command, exit code, PDF page count, size, and SHA-256;
11. citation, reference, label, input, placeholder, and CSV checks;
12. style-audit result;
13. reference-overlap audit result;
14. PDF visual-inspection result and exact pages inspected;
15. confirmation that `sources/` was not changed, including before/after file count and hash;
16. unresolved source, scientific, bibliography, style, template, or layout issues;
17. explicit confirmation that static domain shift was not equated with continual learning;
18. explicit confirmation that external-generalization failure was not called catastrophic forgetting;
19. explicit confirmation that weak supervision was not described as continual learning;
20. explicit confirmation that federated learning was not presented as a formal privacy guarantee;
21. the GitHub content commit SHA containing the verified LaTeX changes;
22. the Overleaf deployment commit SHA or the exact reason synchronization could not be completed;
23. confirmation that Section 1.1 is complete at the current draft stage;
24. confirmation that the next writing target is 1.2.1 and that no Section 1.2 prose was drafted in this task.

## Step 7: commit, push, and synchronize

Do not force-push either remote.

After all content, evidence, terminology, status, compilation, audits, visual checks, and the initial handoff report are complete:

```bash
git diff --check
git status --short
```

Stage only the permitted source, QA, task-provenance, status, and handoff files. Do not stage ignored build products or unrelated changes.

Create a content commit with a clear message, for example:

```bash
git commit -m "Draft Chapter 1 Section 1.1.3"
```

Push it:

```bash
git push origin main
```

Verify that `origin/main` contains the content commit. Only after that push succeeds and the worktree is clean, synchronize the compilable LaTeX subset:

```bash
bash scripts/sync_latex_to_overleaf.sh "Sync Chapter 1 Section 1.1.3"
```

Record the exact Overleaf commit SHA printed by the script.

Because the sync result is known only after the clean content commit, update `handoff/LATEST_CODEX_REPORT.md` and `STATE.md` with the GitHub and Overleaf SHAs after synchronization. If this creates a GitHub-only report change, make and push a second commit, for example:

```bash
git add handoff/LATEST_CODEX_REPORT.md STATE.md
git commit -m "Record Chapter 1.1.3 deployment"
git push origin main
```

Do not run the Overleaf sync again when the second commit changes only GitHub-only files such as `handoff/` or `STATE.md`.

At the end verify:

```bash
git status --short
git rev-parse HEAD
git rev-parse origin/main
```

The worktree must be clean and local `HEAD` must match `origin/main`. Report both final GitHub commit SHAs if two commits were used, and identify which content commit was deployed to Overleaf.

If GitHub push fails, do not synchronize Overleaf. If Overleaf synchronization fails, preserve the verified GitHub commit, report the exact error, and do not force-push or bypass the deployment checks.

## Definition of done

This task is complete only when:

- the approved 1.1.3 text is integrated exactly within its existing subsection;
- Sections 1.1.1 and 1.1.2 remain byte-for-byte unchanged;
- no prose is added to Section 1.2;
- three verified references are added or correctly reused without duplicates;
- claim IDs `C1-017` through `C1-029` are present exactly once;
- the eight new terminology entries are present exactly once;
- the five existing terminology scopes are updated without changing their preferred wording;
- 1.1.3 is `drafted_and_verified` and 1.2 is `queued`;
- the full thesis compiles and all citations resolve;
- style, overlap, structural, bibliography, CSV, and PDF visual checks are completed and reported;
- no file under `sources/` is changed;
- all scientific boundaries listed above are preserved;
- the verified content is pushed to `origin/main`;
- the LaTeX subset is synchronized to Overleaf and remotely verified, or an exact non-bypassed failure is reported;
- the worktree is clean;
- Section 1.1 is recorded as complete at the current draft stage;
- the next target is 1.2.1 and it is not drafted in this task.

Do not continue drafting Section 1.2 in this task.
