# Codex Task: integrate Chapter 1, Section 1.1.2

Read and obey `AGENTS.md`, `THESIS_CONTRACT.md`, `AUTHORSHIP_PROTOCOL.md`, `AUTHOR_VOICE.md`, `STATE.md`, `PROJECT_CONFIG.md`, and `chapter_cards/ch01.md` before editing.

## Goal

Integrate the GPT Pro-approved draft for Section 1.1.2 “医学影像训练信息的多维受限性” into the thesis repository, add only the verified references, evidence records, and terminology entries supplied below, compile and inspect the complete thesis, run all required audits, push the verified work to `origin/main`, and synchronize the compilable LaTeX subset to Overleaf.

The section must establish three distinct but composable constraints:

1. annotation acquisition is limited;
2. access to historical training data is limited;
3. raw data sharing across medical centers is limited.

It must also preserve the boundary between information accessibility and the temporal evolution of data/tasks, which is reserved for Section 1.1.3.

## Strict scientific boundaries

- Do not describe ZScribbleSeg or annotation-efficient learning as continual learning.
- Do not claim that all medical institutions must delete historical images.
- In this thesis, “historical data are inaccessible” means that a specific later training stage cannot fully call the earlier raw samples; it is not a universal legal claim.
- Do not equate replay-free learning with task or distribution evolution.
- Do not claim that federated learning, parameter aggregation, or “data staying local” provides a formal privacy guarantee.
- Do not claim that raw medical data are universally impossible or illegal to share. Use the approved conditional wording about governance, authorization, ownership, infrastructure, and security constraints.
- Do not introduce detailed thesis methods, equations, experimental results, or chapter contributions in this background subsection.
- Do not expand Section 1.1.3 here. This task may only establish the conceptual distinction and transition to it.
- Do not add statutes, regulatory interpretations, numerical claims, or clinical deployment claims.
- Do not copy, translate, paraphrase, or import prose, citations, figures, or metadata from `sources/reference_thesis/`.

## Strict file scope

Files that may be modified or added:

- `CODEX_TASK_ch01_1_1_2.md` — preserve this task file exactly if it is placed in the repository; add it as task provenance if untracked
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

Do not modify any file under `sources/`. Do not modify another chapter, template file, class file, figure, table, script, or bibliography style. Build products and ordinary LaTeX auxiliary files may be regenerated locally but must not be committed if excluded by `.gitignore`.

Do not rewrite the approved academic prose except for a strictly necessary LaTeX syntax correction or replacement of a citation key when an equivalent verified bibliography record already exists under a different key. If a scientific, factual, or stylistic concern is found, report it rather than silently rewriting the prose.

## Step 0: repository and baseline preflight

Before editing:

1. Run `git status --short`.
2. The worktree must be clean except that this task file may be the only untracked file.
3. Run `git fetch origin`.
4. Confirm that the current branch is `main`.
5. Confirm that local `HEAD` is not behind or divergent from `origin/main`.
   - If `origin/main` is ahead and the worktree is otherwise clean, use `git pull --ff-only origin main`.
   - If the histories diverge or unrelated local modifications exist, stop and report the exact state. Do not overwrite or force-push.
6. Confirm in `chapters/ch01_introduction.tex` that:
   - Section 1.1.1 is present and must remain unchanged;
   - the title and label for 1.1.2 already exist;
   - the body between `\label{subsec:intro-information-constraints}` and the next subsection is empty;
   - the next subsection is 1.1.3 “数据分布与医学任务的持续演化”.
7. Confirm that `bibliography/references.bib` currently contains the six verified references from 1.1.1 and that `config/build_flags.tex` has `\thesisbibliographytrue`.
8. Record a read-only snapshot or hash of `sources/` so the final report can confirm that it was not modified.

## Step 1: integrate the approved draft exactly

In `chapters/ch01_introduction.tex`, preserve the existing subsection title and label:

```latex
\subsection{医学影像训练信息的多维受限性}
\label{subsec:intro-information-constraints}
```

Insert the following approved text immediately after that label and before:

```latex
\subsection{数据分布与医学任务的持续演化}
```

Approved text:

```latex
上一节说明，医学影像智能分析的能力取决于训练数据能否覆盖目标任务。进一步看，决定模型可学习内容的并非医疗系统中客观存在的数据总量，而是特定训练阶段能够被实际调用的图像、标签及其访问方式。本文将这些要素统称为训练信息。其中，标签决定监督信号的粒度，历史样本访问决定旧信息能否在后续优化中被重新利用，跨机构共享条件决定分散数据能否形成共同的学习过程。因而，即使影像总量较大，只要上述任一环节受限，模型可利用的信息仍可能少于潜在数据资源\cite{willemink2020preparing,rieke2020future}。

标注获取受限首先表现为专业监督不足。分类任务可以使用检查级或病例级标签，但这类标签通常不能直接给出异常的空间位置和边界；分割任务需要逐像素或逐体素描述器官与病灶，配准研究也可能借助人工标志点或结构分割进行监督与评估。当标签粒度由图像级细化到空间级时，标注过程需要更细致的专业判断，复杂边界、小目标和多类别结构还会增加一致性控制的难度。Tajbakhsh 等将医学图像分割中的不完备数据概括为标注稀缺和弱标注两类，弱标注又可表现为稀疏标签、噪声标签或仅有图像级标签\cite{tajbakhsh2020imperfect}。这说明影像已经完成采集，并不意味着与目标任务匹配的监督信息已经具备。

在这一条件下，图像级标签、点、框、涂鸦或部分切片标注可以降低监督获取负担，但它们不是密集标签的等价替代\cite{tajbakhsh2020imperfect}。未标注区域的类别、目标边界和结构关系仍需由模型根据有限监督、图像内容与先验约束进行推断；若已有标签包含偏差或错误，这些信息还可能作为训练噪声影响优化。标注高效学习的关键因此不是简单减少标签数量，而是明确现有标注保留了哪些任务信息、缺失了哪些信息，并针对缺失部分建立可验证的学习约束。该问题属于弱监督与标注高效学习范畴，不应被解释为持续学习中的知识保持问题。

历史数据访问受限是第二个维度。传统离线训练通常假设所有样本能够在同一阶段被反复读取、随机组合并共同优化；当数据按时间或任务分批进入训练流程时，早期样本在后续阶段未必仍能被完整调用。这里的“不可访问”并不表示所有医疗机构都必须删除历史影像，而是指在特定训练任务中，旧数据可能受治理授权、存储配置、项目边界或实验协议约束，只能保留少量代表样本，甚至不能保留原始样本\cite{rieke2020future}。持续学习研究因而把历史数据能否保存以及可用记忆规模视为关键设定变量：联合训练依赖完整历史数据，回放方法依赖有限的旧样本或替代信息，无回放方法则在不重新读取旧样本的条件下更新模型\cite{delange2022continual}。

历史访问限制与任务变化需要区分。前者描述旧样本在当前优化中是否可用，后者描述当前需要学习的数据分布或目标是否发生变化。即使新旧数据来自相同分布，历史样本不可重访也会排除完整联合训练；反之，即使历史数据可访问，新的设备、模态、类别或任务仍可能要求模型调整已有表征。明确这一区分，可以避免把“无回放”直接等同于“持续演化”，也便于区分有限回放与无回放方法的适用边界。

跨医疗中心数据共享受限构成第三个维度。医学影像由不同机构采集、保存和管理，各中心承担的数据控制责任、患者授权、伦理审批、基础设施和数据所有权安排并不完全相同。将多中心原始影像复制到同一位置因而并非单纯的文件传输问题；即使技术上可以传输，也需满足相应的治理与安全条件。Rieke 等指出，医疗数据常被分隔在不同的数据孤岛中，隐私与数据治理要求会限制集中访问\cite{rieke2020future}。在此背景下，联邦学习通过在数据所在机构执行局部训练并聚合模型更新，为不集中原始数据的协同建模提供了一种技术路径；Sheller 等在多机构脑肿瘤影像上验证了这类协同训练的可行性\cite{sheller2020federated}。

然而，“数据不出中心”只限定了原始数据的流动方式，并不自动构成形式化隐私保证。模型参数或梯度仍可能携带与本地训练数据相关的信息，协作方身份、通信内容、攻击能力和附加保护机制会共同影响实际风险\cite{rieke2020future,sheller2020federated}。联邦训练还改变了数据检查、随机混合、统一验证和故障排查的条件，并需处理中心间样本量与数据分布差异。因此，本文讨论联邦学习时，主要关注原始数据难以集中条件下的协同优化与跨中心历史知识保护，不把参数聚合本身表述为已经消除隐私泄露。

三个维度可以独立出现，也可以相互叠加。单个中心可能积累了大量影像，却只有少量精细标注；历史样本可能继续保存在本地，但不能在后续任务中重新调用；多中心数据总量可能足够，却因物理和管理上的分离而无法构成统一训练集。因此，医学影像学习方法的设定不能只用样本数量描述，还应同时说明监督形式、历史样本访问范围以及跨中心通信和聚合方式。弱监督、持续学习和联邦学习分别改变模型可利用信息集合的不同部分，它们可以组合，但不能在未说明假设的情况下相互替代。

上述限制回答的是模型在各训练阶段能够获得、保留和共享哪些信息。真实医学场景还存在另一类变化：患者人群、疾病构成、成像设备、采集协议和任务目标可能随时间改变。信息可访问性与数据或任务演化相关但并不相同，前者限定模型可用的证据，后者改变模型需要适应的目标。下一节将讨论数据分布与医学任务的持续演化，以及由此产生的知识保持、新知识学习和跨任务泛化要求。
```

After insertion, verify that:

- Section 1.1.1 is byte-for-byte unchanged relative to the baseline;
- both subsection titles and labels remain unique;
- no text was added to 1.1.3;
- the approved text contains exactly the five expected citation keys:
  - existing: `willemink2020preparing`
  - new: `tajbakhsh2020imperfect`, `delange2022continual`, `rieke2020future`, `sheller2020federated`.

## Step 2: add the verified bibliography entries

The metadata below was verified by GPT Pro against the DOI publisher record and, where available, PubMed/PMC or DBLP metadata:

- Tajbakhsh et al.: DOI `10.1016/j.media.2020.101693`, PMID `32289663`
- De Lange et al.: DOI `10.1109/TPAMI.2021.3057446`, final volume 44(7), pages 3366--3385
- Rieke et al.: DOI `10.1038/s41746-020-00323-1`, PMID `33015372`
- Sheller et al.: DOI `10.1038/s41598-020-69250-1`, PMCID `PMC7387485`

Before adding each entry, check `bibliography/references.bib` for:

1. duplicate key;
2. duplicate DOI, case-insensitively;
3. duplicate normalized title;
4. an equivalent verified record under a different key.

Add the following entries only when no equivalent record exists. Preserve all existing verified records. If an equivalent record exists under another key, reuse it and change only the corresponding `\cite{}` key in the approved text.

```bibtex
@article{tajbakhsh2020imperfect,
  author  = {Tajbakhsh, Nima and Jeyaseelan, Laura and Li, Qian and Chiang, Jeffrey N. and Wu, Zhihao and Ding, Xiaowei},
  title   = {Embracing Imperfect Datasets: A Review of Deep Learning Solutions for Medical Image Segmentation},
  journal = {Medical Image Analysis},
  volume  = {63},
  pages   = {101693},
  year    = {2020},
  doi     = {10.1016/j.media.2020.101693}
}

@article{delange2022continual,
  author  = {{De Lange}, Matthias and Aljundi, Rahaf and Masana, Marc and Parisot, Sarah and Jia, Xu and Leonardis, Ale{\v{s}} and Slabaugh, Gregory G. and Tuytelaars, Tinne},
  title   = {A Continual Learning Survey: Defying Forgetting in Classification Tasks},
  journal = {IEEE Transactions on Pattern Analysis and Machine Intelligence},
  volume  = {44},
  number  = {7},
  pages   = {3366--3385},
  year    = {2022},
  doi     = {10.1109/TPAMI.2021.3057446}
}

@article{rieke2020future,
  author  = {Rieke, Nicola and Hancox, Jonny and Li, Wenqi and Milletar{\`i}, Fausto and Roth, Holger R. and Albarqouni, Shadi and Bakas, Spyridon and Galtier, Mathieu N. and Landman, Bennett A. and Maier-Hein, Klaus and Ourselin, S{\'e}bastien and Sheller, Micah and Summers, Ronald M. and Trask, Andrew and Xu, Daguang and Baust, Maximilian and Cardoso, M. Jorge},
  title   = {The Future of Digital Health with Federated Learning},
  journal = {npj Digital Medicine},
  volume  = {3},
  number  = {1},
  pages   = {119},
  year    = {2020},
  doi     = {10.1038/s41746-020-00323-1}
}

@article{sheller2020federated,
  author  = {Sheller, Micah J. and Edwards, Brandon and Reina, G. Anthony and Martin, Jason and Pati, Sarthak and Kotrotsou, Aikaterini and Milchenko, Mikhail and Xu, Weilin and Marcus, Daniel and Colen, Rivka R. and Bakas, Spyridon},
  title   = {Federated Learning in Medicine: Facilitating Multi-Institutional Collaborations without Sharing Patient Data},
  journal = {Scientific Reports},
  volume  = {10},
  number  = {1},
  pages   = {12598},
  year    = {2020},
  doi     = {10.1038/s41598-020-69250-1}
}
```

Confirm that `config/build_flags.tex` remains set to:

```latex
\thesisbibliographytrue
```

Do not add any reference that is not cited by the approved text.

## Step 3: append evidence records

Append the following rows to `evidence/claims.csv` after checking that the claim IDs do not already exist.

```csv
C1-008,1,1.1.2,医学影像训练信息包括特定训练阶段可实际调用的图像标签历史样本及跨机构协作条件,author synthesis based on cited section sources,Section definition,willemink2020preparing;rieke2020future,author_analysis,confirmed,drafted,用于界定训练信息而非仅指客观存在的数据量
C1-009,1,1.1.2,医学图像分割中的不完备数据可区分为标注稀缺与弱标注且弱标注可表现为稀疏噪声或图像级标签,DOI:10.1016/j.media.2020.101693,Abstract and dataset limitation taxonomy,tajbakhsh2020imperfect,literature,confirmed,drafted,仅用于概括监督信息形式
C1-010,1,1.1.2,图像级点框涂鸦和部分切片等弱标注可降低标注负担但不等价于密集空间监督,DOI:10.1016/j.media.2020.101693,Review taxonomy and weak annotation discussion,tajbakhsh2020imperfect,author_analysis,confirmed,drafted,不声称所有弱标注形式具有相同信息量
C1-011,1,1.1.2,联合训练有限回放和无回放方法对应不同的历史数据访问与记忆条件,DOI:10.1109/TPAMI.2021.3057446,Survey scope method taxonomy and memory comparison,delange2022continual,literature,confirmed,drafted,该综述重点为分类任务故正文只用于概念设定
C1-012,1,1.1.2,本节所称历史数据不可访问是训练阶段不能完整调用旧样本而非声称机构必须删除全部历史影像,author scope definition,Section scope statement,delange2022continual;rieke2020future,author_definition,confirmed,drafted,用于限制论断范围并避免法律化绝对表述
C1-013,1,1.1.2,医疗数据常位于相互隔离的数据孤岛且隐私与治理条件会限制集中访问,DOI:10.1038/s41746-020-00323-1,Abstract and data reliance sections,rieke2020future,literature,confirmed,drafted,不扩展为原始数据绝对不能共享
C1-014,1,1.1.2,联邦学习可通过局部训练和更新聚合支持不交换原始患者数据的多机构医学影像协同训练,DOI:10.1038/s41598-020-69250-1,Abstract and experimental design,sheller2020federated,primary_experiment,confirmed,drafted,验证范围限于该多机构脑肿瘤影像研究
C1-015,1,1.1.2,数据不出中心不等于形式化隐私保证且共享参数或梯度仍可能暴露训练数据相关信息,DOI:10.1038/s41746-020-00323-1;DOI:10.1038/s41598-020-69250-1,Technical considerations and security privacy discussion,rieke2020future;sheller2020federated,literature,confirmed,drafted,用于明确本文不声称联邦聚合提供形式化隐私
C1-016,1,1.1.2,标注历史访问和机构共享三类限制可独立存在或叠加且方法设定应明确监督回放和通信条件,author synthesis based on section sources,Section synthesis,tajbakhsh2020imperfect;delange2022continual;rieke2020future;sheller2020federated,author_analysis,confirmed,drafted,用于形成全文统一问题背景
```

Preserve the existing CSV header and 11-column schema. Validate every row with a CSV parser. If a field would require a comma, quote that field rather than changing the scientific meaning.

## Step 4: terminology and writing status

Add the following non-duplicate rows to `qa/terminology.csv`:

```csv
training information,训练信息,全文,训练数据（两者范围不完全等同）,指特定训练阶段可实际调用的图像标签及其访问和共享条件
weak annotation,弱标注,第一至三章,弱监督（方法范式与标签形式不可混用）,指稀疏噪声图像级等不完整监督形式
historical data access,历史数据访问,第一章与第四至六章,历史数据可用性（首次定义后可作解释）,指后续训练阶段能否重新调用旧样本
limited replay,有限回放,第一章与第五章,受限回放（避免混用）,允许访问有限历史样本或其受控替代信息
data silo,数据孤岛,第一章与第六章,信息孤岛（避免混用）,指数据由不同机构独立保存和治理
federated learning,联邦学习,第一章与第六章,分布式学习（不可等同）,数据不出中心不代表参数交换本身提供形式化隐私保证
```

Update `qa/chapter_status.csv`:

- `1.1.2` → `drafted_and_verified`, artifact `chapters/ch01_introduction.tex`
- `1.1.3` → `queued`
- do not change the status of another section unless required to preserve the CSV schema.

Update `STATE.md` so that it accurately records:

- 1.1.2 has been integrated, referenced, compiled, audited, and visually checked;
- the current/next subsection is 1.1.3 “数据分布与医学任务的持续演化”;
- the exact build and audit outcome;
- any non-fatal layout warning or unresolved scientific/source issue;
- the GitHub and Overleaf synchronization state after Step 7.

Do not add an approved voice example to `AUTHOR_VOICE.md`; that file is updated only after the author personally revises and confirms a section.

## Step 5: compile and verify

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

If `sources/reference_thesis/` contains reference thesis `.tex` files, run:

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
3. All ten expected bibliography records are present after this task unless an equivalent record was reused:
   - six existing records from 1.1.1;
   - four verified records from this task.
4. Every citation used in 1.1.1 and 1.1.2 resolves in the active `.bib` and generated `.bbl`.
5. No undefined citation or cross-reference is introduced.
6. No duplicate bibliography key, DOI, or normalized title exists.
7. No duplicate LaTeX label is introduced.
8. No required input or figure is missing.
9. No new `TODO`, `TBD`, or `??` appears in active thesis inputs.
10. `git diff --check` passes.
11. `evidence/claims.csv` remains parseable with exactly 11 columns per row and contains unique claim IDs.
12. `qa/terminology.csv` remains parseable with exactly 5 columns per row.
13. Section 1.1.1 remains unchanged.
14. The 1.1.2 title and label remain unchanged.
15. No body text is added to 1.1.3.
16. The style audit result is reported rather than silently fixed through unauthorized rewriting.
17. The reference-overlap audit result is reported and no superficial paraphrasing is used to conceal overlap.
18. The `sources/` snapshot or hash is unchanged.
19. Render and visually inspect every PDF page containing 1.1.2 and the updated bibliography pages for:
    - Chinese character rendering;
    - citation rendering;
    - paragraph breaks;
    - overfull or clipped text;
    - unusual blank areas;
    - heading placement;
    - overlap or missing content.
20. Record the final PDF page count, byte size, and SHA-256 in the handoff report.

A non-fatal warning may be reported without unauthorized template changes. Do not change approved prose merely to hide a harmless page-break or underfull-box warning.

## Step 6: write the Codex handoff report

Replace `handoff/LATEST_CODEX_REPORT.md` with a complete report containing:

1. task name and execution timestamp;
2. baseline Git commit and repository preflight result;
3. exact modified and added files;
4. confirmation that the approved 1.1.2 prose was integrated without unauthorized rewriting;
5. exact bibliography entries added or reused and the duplicate checks performed;
6. evidence rows and terminology rows added;
7. chapter status and `STATE.md` updates;
8. compile command, exit code, PDF page count, size, and SHA-256;
9. citation, reference, label, input, and placeholder checks;
10. style audit result;
11. reference-overlap audit result;
12. PDF visual inspection result and pages inspected;
13. confirmation that `sources/` was not changed;
14. unresolved source, scientific, bibliography, style, or layout issues;
15. explicit confirmation that federated learning was not presented as a formal privacy guarantee;
16. explicit confirmation that annotation-efficient learning was not presented as continual learning;
17. the GitHub commit SHA containing the verified LaTeX changes;
18. the Overleaf deployment commit SHA or the exact reason synchronization could not be completed;
19. confirmation that the next subsection is 1.1.3 and that it was not drafted in this task.

## Step 7: commit, push, and synchronize

Do not force-push either remote.

After all content, evidence, status, compilation, audits, and the initial handoff report are complete:

```bash
git diff --check
git status --short
```

Stage only the permitted source, QA, task-provenance, status, and handoff files. Do not stage build products that are ignored or unrelated changes.

Create a content commit with a clear message, for example:

```bash
git commit -m "Draft Chapter 1 Section 1.1.2"
```

Push it:

```bash
git push origin main
```

Verify that the remote `origin/main` contains the content commit. Only after that push succeeds and the worktree is clean, synchronize the compilable LaTeX subset:

```bash
bash scripts/sync_latex_to_overleaf.sh "Sync Chapter 1 Section 1.1.2"
```

Record the exact Overleaf commit SHA printed by the script.

Because the sync result is only known after the clean content commit, update `handoff/LATEST_CODEX_REPORT.md` with the GitHub and Overleaf SHAs after synchronization. If this creates a report-only change, make and push a second GitHub commit, for example:

```bash
git add handoff/LATEST_CODEX_REPORT.md STATE.md
git commit -m "Record Chapter 1.1.2 deployment"
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

- the approved 1.1.2 text is integrated exactly within its existing subsection;
- Section 1.1.1 remains unchanged;
- four verified references are added or correctly reused without duplicates;
- claim IDs `C1-008` through `C1-016` are present exactly once;
- the six terminology entries are present exactly once;
- 1.1.2 is `drafted_and_verified` and 1.1.3 is `queued`;
- the full thesis compiles and all citations resolve;
- style, overlap, structural, CSV, and visual checks are completed and reported;
- no file under `sources/` is changed;
- the verified content is pushed to `origin/main`;
- the LaTeX subset is synchronized to Overleaf and remotely verified, or an exact non-bypassed failure is reported;
- the worktree is clean;
- no prose for Section 1.1.3 is drafted.

Do not continue drafting Section 1.1.3 in this task.
