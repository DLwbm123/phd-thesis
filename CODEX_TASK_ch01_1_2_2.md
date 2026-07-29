# Codex Task: integrate Chapter 1, Section 1.2.2

Read and obey `AGENTS.md`, `THESIS_CONTRACT.md`, `AUTHORSHIP_PROTOCOL.md`, `AUTHOR_VOICE.md`, `STATE.md`, `PROJECT_CONFIG.md`, and `chapter_cards/ch01.md` before editing.

## Goal

Integrate the GPT Pro-approved draft for Section 1.2.2 “医学影像持续学习研究现状” into the thesis repository. Add only the verified references, evidence records, and terminology updates supplied below; compile and inspect the complete thesis; run all required audits; push the verified work to `origin/main`; and synchronize the compilable LaTeX subset to Overleaf.

This is the second of three sequential Section 1.2 tasks. It assumes that `CODEX_TASK_ch01_1_2_1.md` has already been completed and verified. Stop after 1.2.2. Do not draft 1.2.3 or Section 1.3.

## Evidence policy

The user-provided surveys by De Lange et al., Wang et al., Kumari et al., and Yuan and Zhao establish the general taxonomy, medical scenario map, and continual-segmentation distinctions. The approved prose nevertheless uses original studies as the primary evidence for concrete mechanisms and medical findings.

Do not copy, translate, or closely paraphrase survey or paper text. Do not import any text or citation combination from a reference thesis.

## Strict scientific boundaries

- Do not present all multi-center or multi-dataset experiments as continual learning. A sequential update process and retention objective must be present.
- Do not treat task-incremental, domain-incremental, class-incremental, instance-incremental, organ-incremental, and modality-incremental settings as interchangeable.
- `Domain-CL`, `Class-CL`, and `Organ-CL` are the named scenarios of the author’s benchmark study; `Organ-CL` must not be presented as a universally standardized field-wide category.
- Do not call first-time failure on an unseen domain catastrophic forgetting.
- Do not reduce continual learning evaluation to final average accuracy or forgetting alone.
- Do not use “forward transfer” and “forward generalization” as synonyms. Preserve the terminology of this thesis.
- Do not describe the continual segmentation benchmark as a single anti-forgetting algorithm.
- Do not mechanically classify continual medical image registration as class-incremental learning.
- Do not claim that replay is universally prohibited in medicine; distinguish full replay, limited replay, and no replay.
- Do not describe ZScribbleSeg or weak supervision as continual learning.
- Do not claim clinical deployment, regulatory approval, or automatic online updating.
- Do not draft 1.2.3, Section 1.3, or later sections.
- Do not modify any file under `sources/` or import material from `sources/reference_thesis/`.

## Strict file scope

Files that may be modified or added:

- `CODEX_TASK_ch01_1_2_2.md`
- `chapters/ch01_introduction.tex`
- `bibliography/references.bib`
- `config/build_flags.tex` — only if needed to preserve `\thesisbibliographytrue`
- `evidence/claims.csv`
- `qa/terminology.csv`
- `qa/chapter_status.csv`
- `qa/style_audit_report.md`
- `qa/reference_overlap_report.md`
- `STATE.md`
- `handoff/LATEST_CODEX_REPORT.md`

Do not modify another chapter, template/class file, figure, table, script, bibliography style, or any file under `sources/`. Do not rewrite approved prose outside 1.2.2.

## Step 0: repository and baseline preflight

1. Run:

   ```bash
   git status --short
   git branch --show-current
   git fetch origin
   ```

2. The worktree must be clean except that this task file may be the only untracked file.
3. Confirm `main`, no divergence, and fast-forward only when needed.
4. Record the exact baseline SHA.
5. Confirm:
   - Sections 1.1.1--1.1.3 are verified;
   - 1.2.1 is present and `drafted_and_verified`;
   - the 1.2.2 title and label exist and its body is empty;
   - 1.2.3 and Section 1.3 are body-empty.
6. Save byte-for-byte hashes of Section 1.1, 1.2.1, the empty 1.2.3 body, and the empty Section 1.3 body.
7. Confirm that all bibliography entries and claims from the completed 1.2.1 task are present, including `C1-030` through `C1-042`.
8. Record the actual active bibliography count; the expected sequential baseline is 22 entries if all nine 1.2.1 records were newly added.
9. Confirm `\thesisbibliographytrue`.
10. Record the `sources/` file count and deterministic SHA-256.

If 1.2.1 is not complete and verified, stop. Do not silently execute two tasks at once.

## Step 1: integrate the approved draft exactly

Preserve:

```latex
\subsection{医学影像持续学习研究现状}
\label{subsec:intro-continual-learning}
```

Insert immediately after the label and before the title of 1.2.3:

```latex
持续学习研究关注模型在数据或任务顺序到达时如何累积知识，并在有限或无法访问旧训练样本的条件下维持已获得能力。De Lange 等将回放、正则化和参数隔离概括为主要技术路线，并强调稳定性—可塑性权衡\cite{delange2022continual}；Wang 等进一步把持续学习目标扩展为资源约束下的稳定性、可塑性以及任务内和任务间泛化\cite{wang2024continualsurvey}。这些综述为方法分类提供了共同框架，但其多数定义和实验首先建立在分类任务上，迁移到医学图像分割与配准时仍需结合输出结构和评价协议重新界定。

医学影像中的顺序变化可来源于样本批次、类别、任务、医疗中心、设备、协议、模态或器官目标。Kumari 等将已有医学研究整理为实例增量、类增量、任务增量、域增量和混合场景，并指出任务身份、阶段边界和标注可用性会改变问题难度\cite{kumari2025medicalcl}。这种分类反映了医学应用的多样性，也暴露出文献命名尚不完全统一：相同的数据序列可能因输出头、测试时上下文和累计预测要求不同而被归入不同场景。因此，研究现状不能只按方法名称比较，还需同时核对任务序列和测试协议。

通用持续学习方法可以按保存何种历史信息来理解。回放方法保存旧样本、特征或生成数据，以近似历史分布；正则化方法约束重要参数或旧模型输出的变化；参数隔离和动态结构方法为不同任务保留独立或部分独立的模型容量；优化与表示方法则通过梯度投影、平坦解或预训练表征减少任务干扰\cite{wang2024continualsurvey}。这些路线在存储、计算、参数增长和历史数据依赖上具有不同代价，不存在脱离具体资源条件的统一优劣顺序。

若从代表性原始方法看，iCaRL 通过类别样本记忆和表示学习支持类别集合扩展\cite{rebuffi2017icarl}；弹性权重巩固根据参数对旧任务的重要性限制后续更新\cite{kirkpatrick2017ewc}；Learning without Forgetting 则利用旧模型在当前数据上的输出进行知识蒸馏\cite{li2018lwf}。三者分别体现经验回放、参数正则和函数正则的基本思想。它们为医学持续学习提供了可复用机制，但原始设定以分类为主，不能仅凭方法类别推断其在高分辨率体数据和密集预测任务中的效果。

早期持续医学图像分割研究主要关注设备和采集协议变化。Karani 等将不同扫描仪和协议视为顺序到达的相关域，在共享卷积特征的同时保留域特定批归一化参数\cite{karani2018lifelong}。该设计减少新域适配对旧域的直接干扰，但需要为域保留特定状态，并依赖域身份或相应参数选择。它说明域增量医学分割不仅涉及通用特征保持，还涉及成像统计的显式建模。

此后，正则化方法开始结合医学结构信息。S3R 根据分割形状和语义估计参数重要性，对跨中心持续分割中的选择性参数变化进行约束\cite{zhang2023s3r}。与只使用分类损失敏感度的通用正则化相比，这类方法把密集预测输出的结构属性纳入知识保持。然而，参数保护强度仍需在新中心适应和旧中心保持之间调节，统一约束不一定适合差异程度不同的任务序列。

标准化框架研究进一步表明，分类领域的结论不能直接套用于医学分割。Lifelong nnU-Net 在统一分割管线中比较回放、EWC、LwF、Riemannian Walk 和 MiB，并在三个持续分割用例中跟踪旧任务和新任务性能\cite{gonzalez2023lifelong}。该研究在其测试条件下观察到，所比较方法没有持续获得正向后向迁移，回放的遗忘相对较少，而任务特定输出头的影响有限。这些结论属于指定网络、数据序列和方法集合，不能扩展为所有医学分割场景的一般排序。

持续语义分割还具有分类任务中不完全相同的监督变化。MiB 指出，当当前阶段只标注新增类别时，旧类别像素可能被并入背景，导致背景语义随阶段改变，并据此调整损失与蒸馏\cite{cermelli2020mib}。PLOP 进一步利用多尺度特征蒸馏和背景伪标签维持旧类别信息\cite{douillard2021plop}。Yuan 和 Zhao 将这一现象概括为持续语义分割中的背景语义漂移，并将已有方法按数据回放和无旧数据路线整理\cite{yuan2024continualseg}。对于医学分割，该问题是否出现取决于标签协议；在所有结构都被完整标注的域增量场景中，不能机械套用类别增量背景漂移的结论。

当分割目标随阶段扩展时，研究开始使用器官特定组件和伪标签保护既有结构。Zhang 等在腹部多器官与肿瘤分割中采用器官特定输出头，并利用旧模型产生的伪标签辅助顺序学习\cite{zhang2023continualorgan}。这类设定可表现为新增解剖类别，也可因任务身份和输出组织方式被视为新任务。因此，“新增器官”本身不足以唯一决定增量类型，必须同时说明共享输出空间、测试时上下文和累计预测要求。

现有研究在场景和评价方面仍缺少统一口径。Wang 等构建 Domain-CL、Class-CL 和 Organ-CL 三类持续医学图像分割场景，并同时评价总体性能、遗忘、可塑性、前向泛化、参数效率和回放负担\cite{wang2026benchmark}。该工作属于场景定义和系统性实证研究，而不是提出单一抗遗忘算法。其结果表明，不同技术路线在稳定性、可塑性和资源开销之间呈现不同取舍，也说明仅以最终平均性能或遗忘量不足以刻画持续分割方法。

持续学习还被用于医学图像配准。SAMCL 面向顺序到达的三维配准任务，将有限经验回放与元持续学习结合，并通过锐度感知优化改善跨任务泛化\cite{wang2024samcl}。配准模型输出的是图像间空间变换，而非离散类别，因此其任务变化应由解剖区域、模态组合和配准映射共同定义。该研究表明，知识保持之外，模型能否利用已有任务形成对后续乃至未见配准任务有效的初始化，同样是持续医学影像学习的重要目标。

总体而言，医学影像持续学习已从通用抗遗忘方法的直接迁移，发展到面向跨中心域变化、类别或器官扩展、密集预测语义变化以及顺序配准的专门设计。现有方法分别利用回放、参数或函数正则、任务特定结构、伪标签、梯度约束和元学习，但其结论常受场景定义、历史数据访问、任务身份、网络容量和评价维度影响。如何建立覆盖不同医学分割演化方式的清晰场景，并在知识保持、新知识学习、前向泛化和资源效率之间进行综合评价，仍是持续医学影像研究需要解决的问题。
```

After insertion verify:

- Section 1.1 and 1.2.1 are byte-for-byte unchanged.
- 1.2.3 and Section 1.3 remain body-empty.
- 1.2.2 title and label remain unique.
- No statement treats the benchmark as an algorithm.
- No statement treats Organ-CL as a universal standard.
- No statement equates first-time external-domain failure with forgetting.
- No statement equates forward transfer with forward generalization.

## Step 2: add verified bibliography entries

Check key, DOI, normalized title, and equivalent records before adding. Add or reuse only entries cited above:

```bibtex
@article{wang2024continualsurvey,
  author  = {Wang, Liyuan and Zhang, Xingxing and Su, Hang and Zhu, Jun},
  title   = {A Comprehensive Survey of Continual Learning: Theory, Method and Application},
  journal = {IEEE Transactions on Pattern Analysis and Machine Intelligence},
  volume  = {46},
  number  = {8},
  pages   = {5362--5383},
  year    = {2024},
  doi     = {10.1109/TPAMI.2024.3367329}
}

@article{kumari2025medicalcl,
  author  = {Kumari, Pratibha and Chauhan, Joohi and Bozorgpour, Afshin and Huang, Boqiang and Azad, Reza and Merhof, Dorit},
  title   = {Continual Learning in Medical Image Analysis: A Comprehensive Review of Recent Advancements and Future Prospects},
  journal = {Medical Image Analysis},
  volume  = {106},
  pages   = {103730},
  year    = {2025},
  doi     = {10.1016/j.media.2025.103730}
}

@article{yuan2024continualseg,
  author  = {Yuan, Bo and Zhao, Danpei},
  title   = {A Survey on Continual Semantic Segmentation: Theory, Challenge, Method and Application},
  journal = {IEEE Transactions on Pattern Analysis and Machine Intelligence},
  volume  = {46},
  number  = {12},
  pages   = {10891--10910},
  year    = {2024},
  doi     = {10.1109/TPAMI.2024.3446949}
}

@inproceedings{rebuffi2017icarl,
  author    = {Rebuffi, Sylvestre-Alvise and Kolesnikov, Alexander and Sperl, Georg and Lampert, Christoph H.},
  title     = {{iCaRL}: Incremental Classifier and Representation Learning},
  booktitle = {Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition},
  pages     = {2001--2010},
  year      = {2017}
}

@article{kirkpatrick2017ewc,
  author  = {Kirkpatrick, James and Pascanu, Razvan and Rabinowitz, Neil and Veness, Joel and Desjardins, Guillaume and Rusu, Andrei A. and Milan, Kieran and Quan, John and Ramalho, Tiago and Grabska-Barwinska, Agnieszka and Hassabis, Demis and Clopath, Claudia and Kumaran, Dharshan and Hadsell, Raia},
  title   = {Overcoming Catastrophic Forgetting in Neural Networks},
  journal = {Proceedings of the National Academy of Sciences},
  volume  = {114},
  number  = {13},
  pages   = {3521--3526},
  year    = {2017},
  doi     = {10.1073/pnas.1611835114}
}

@article{li2018lwf,
  author  = {Li, Zhizhong and Hoiem, Derek},
  title   = {Learning without Forgetting},
  journal = {IEEE Transactions on Pattern Analysis and Machine Intelligence},
  volume  = {40},
  number  = {12},
  pages   = {2935--2947},
  year    = {2018},
  doi     = {10.1109/TPAMI.2017.2773081}
}

@inproceedings{karani2018lifelong,
  author    = {Karani, Neerav and Chaitanya, Krishna and Baumgartner, Christian F. and Konukoglu, Ender},
  title     = {A Lifelong Learning Approach to Brain {MR} Segmentation Across Scanners and Protocols},
  booktitle = {Medical Image Computing and Computer Assisted Intervention -- MICCAI 2018},
  series    = {Lecture Notes in Computer Science},
  volume    = {11070},
  pages     = {476--484},
  publisher = {Springer},
  year      = {2018},
  doi       = {10.1007/978-3-030-00928-1_54}
}

@article{zhang2023s3r,
  author  = {Zhang, Jingyang and Gu, Ran and Xue, Peng and Liu, Mianxin and Zheng, Hao and Zheng, Yefeng and Ma, Lei and Wang, Guotai and Gu, Lixu},
  title   = {{$S^3R$}: Shape and Semantics-Based Selective Regularization for Explainable Continual Segmentation Across Multiple Sites},
  journal = {IEEE Transactions on Medical Imaging},
  volume  = {42},
  number  = {9},
  pages   = {2539--2551},
  year    = {2023},
  doi     = {10.1109/TMI.2023.3260974}
}

@article{gonzalez2023lifelong,
  author  = {Gonz{\'a}lez, Camila and Ranem, Amin and Pinto dos Santos, Daniel and Othman, Ahmed and Mukhopadhyay, Anirban},
  title   = {Lifelong {nnU-Net}: A Framework for Standardized Medical Continual Learning},
  journal = {Scientific Reports},
  volume  = {13},
  pages   = {9381},
  year    = {2023},
  doi     = {10.1038/s41598-023-34484-2}
}

@inproceedings{cermelli2020mib,
  author    = {Cermelli, Fabio and Mancini, Massimiliano and Rota Bulo, Samuel and Ricci, Elisa and Caputo, Barbara},
  title     = {Modeling the Background for Incremental Learning in Semantic Segmentation},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
  pages     = {9233--9242},
  year      = {2020}
}

@inproceedings{douillard2021plop,
  author    = {Douillard, Arthur and Chen, Yifu and Dapogny, Arnaud and Cord, Matthieu},
  title     = {{PLOP}: Learning without Forgetting for Continual Semantic Segmentation},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
  pages     = {4040--4050},
  year      = {2021}
}

@inproceedings{zhang2023continualorgan,
  author    = {Zhang, Yixiao and Li, Xinyi and Chen, Huimiao and Yuille, Alan L. and Liu, Yaoyao and Zhou, Zongwei},
  title     = {Continual Learning for Abdominal Multi-organ and Tumor Segmentation},
  booktitle = {Medical Image Computing and Computer Assisted Intervention -- MICCAI 2023},
  series    = {Lecture Notes in Computer Science},
  volume    = {14221},
  pages     = {35--45},
  publisher = {Springer},
  year      = {2023},
  doi       = {10.1007/978-3-031-43895-0_4}
}

@article{wang2026benchmark,
  author        = {Wang, Bomin and Zhou, Hangqi and Gao, Yibo and Zhuang, Xiahai},
  title         = {Beyond Forgetting in Continual Medical Image Segmentation: A Comprehensive Benchmark Study},
  journal       = {arXiv preprint arXiv:2605.06160},
  year          = {2026},
  eprint        = {2605.06160},
  archiveprefix = {arXiv},
  primaryclass  = {cs.CV}
}

@inproceedings{wang2024samcl,
  author    = {Wang, Bomin and Luo, Xinzhe and Zhuang, Xiahai},
  title     = {Toward Universal Medical Image Registration via Sharpness-Aware Meta-Continual Learning},
  booktitle = {Medical Image Computing and Computer Assisted Intervention -- MICCAI 2024},
  series    = {Lecture Notes in Computer Science},
  pages     = {739--748},
  publisher = {Springer},
  year      = {2024},
  doi       = {10.1007/978-3-031-72069-7_69}
}
```

Do not add uncited papers or copy a survey bibliography wholesale. Preserve `\thesisbibliographytrue`.

## Step 3: append evidence records

```csv
C1-043,1,1.2.2,持续学习研究要求顺序累积知识并协调稳定性和可塑性,DOI:10.1109/TPAMI.2021.3057446,Abstract introduction and scope,delange2022continual,literature,confirmed,drafted,该综述重点为任务增量分类
C1-044,1,1.2.2,持续学习总体目标还包括任务内任务间泛化和资源效率,DOI:10.1109/TPAMI.2024.3367329,Abstract and conceptual framework,wang2024continualsurvey,literature,confirmed,drafted,用于扩展评价视角
C1-045,1,1.2.2,医学影像持续学习文献包含实例类任务域及混合增量场景,DOI:10.1016/j.media.2025.103730,Scenario taxonomy,kumari2025medicalcl,literature,confirmed,drafted,不将分类视为互斥且穷尽
C1-046,1,1.2.2,回放正则化参数隔离优化和表示方法保存不同形式的历史信息,DOI:10.1109/TPAMI.2024.3367329,Method taxonomy,wang2024continualsurvey,literature,confirmed,drafted,用于研究路线概括
C1-047,1,1.2.2,iCaRL使用类别样本记忆与表示学习支持类别增量分类,primary paper,Method and evaluation,rebuffi2017icarl,method,confirmed,drafted,不直接扩展为分割效果结论
C1-048,1,1.2.2,EWC依据参数对旧任务的重要性限制后续参数变化,DOI:10.1073/pnas.1611835114,Method formulation,kirkpatrick2017ewc,method,confirmed,drafted,作为参数正则代表
C1-049,1,1.2.2,LwF通过旧模型在当前数据上的输出实施知识蒸馏,DOI:10.1109/TPAMI.2017.2773081,Method formulation,li2018lwf,method,confirmed,drafted,作为函数正则代表
C1-050,1,1.2.2,脑MR持续分割可使用共享卷积参数和域特定批归一化适应新扫描仪与协议,DOI:10.1007/978-3-030-00928-1_54,Abstract and method,karani2018lifelong,method,confirmed,drafted,依赖域特定状态
C1-051,1,1.2.2,S3R利用形状和语义信息估计跨中心持续分割中的参数重要性,DOI:10.1109/TMI.2023.3260974,Abstract and method,zhang2023s3r,method,confirmed,drafted,用于说明医学结构正则
C1-052,1,1.2.2,Lifelong nnU-Net在统一管线中比较多种持续分割策略并报告方法差异,DOI:10.1038/s41598-023-34484-2,Abstract experiments and discussion,gonzalez2023lifelong,primary_experiment,confirmed,drafted,结论严格限定于该框架和三个用例
C1-053,1,1.2.2,类别增量语义分割中旧类像素可能被并入背景形成背景语义变化,primary paper,Abstract and formulation,cermelli2020mib,method,confirmed,drafted,不扩展至完整标注域增量场景
C1-054,1,1.2.2,PLOP通过多尺度特征蒸馏和背景伪标签保护旧类别信息,primary paper,Abstract and method,douillard2021plop,method,confirmed,drafted,作为持续语义分割代表方法
C1-055,1,1.2.2,持续语义分割具有灾难性遗忘与背景语义漂移等密集预测特有问题,DOI:10.1109/TPAMI.2024.3446949,Abstract and challenge taxonomy,yuan2024continualseg,literature,confirmed,drafted,背景漂移需结合标签协议判断
C1-056,1,1.2.2,腹部多器官与肿瘤持续分割可结合器官特定输出头和旧模型伪标签,DOI:10.1007/978-3-031-43895-0_4,Abstract and method,zhang2023continualorgan,method,confirmed,drafted,新增器官的场景类型仍取决于协议
C1-057,1,1.2.2,持续医学分割基准定义Domain-CL Class-CL Organ-CL并开展多维评价,arXiv:2605.06160,Abstract,wang2026benchmark,benchmark,confirmed,drafted,Organ-CL为该研究命名场景而非领域统一标准
C1-058,1,1.2.2,持续医学分割评价可同时考虑总体性能遗忘可塑性前向泛化参数效率和回放负担,arXiv:2605.06160,Abstract and evaluation framework,wang2026benchmark,benchmark,confirmed,drafted,具体指标公式留待第四章
C1-059,1,1.2.2,SAMCL结合有限经验回放元持续学习和锐度感知优化处理顺序三维配准任务,DOI:10.1007/978-3-031-72069-7_69,Abstract and method,wang2024samcl,method,confirmed,drafted,配准任务不机械归为类增量
```

Validate 11 columns, unique IDs `C1-043`--`C1-059`, unchanged existing rows, and valid citation keys.

## Step 4: terminology and status

### Add non-duplicate terminology rows

```csv
rehearsal-based continual learning,回放式持续学习,第一章与第四至六章,重放式持续学习（避免混用）,通过旧样本特征或生成信息近似历史分布
regularization-based continual learning,正则化持续学习,第一章与第四至六章,正则式持续学习（避免混用）,通过参数函数或表示约束保护已有知识
parameter isolation,参数隔离,第一章与第四至六章,参数分离（避免混用）,为不同任务保留独立或部分独立参数
background semantic drift,背景语义漂移,第一章与第四章,背景漂移（首次定义后可简称）,当前标注协议使背景包含旧类未来类与真实背景的语义变化
Domain-CL,域持续学习场景,第一章与第四章,域增量学习（两者按具体定义区分）,第四章基准中面向顺序跨中心域变化的场景名
Class-CL,类别持续学习场景,第一章与第四章,类增量学习（两者按具体定义区分）,第四章基准中面向顺序新增分割结构的场景名
Organ-CL,器官持续学习场景,第一章与第四章,器官增量学习（避免视为统一标准术语）,第四章基准中面向跨器官分割任务的场景名
replay burden,回放负担,第一章与第四至六章,回放开销（可作解释）,由保存或生成历史信息带来的存储计算与治理成本
global performance,总体性能,第一章与第四至六章,全局性能（在联邦语境中含义不同）,对已学习任务整体能力的汇总评价
```

Update existing scopes:

- `experience replay` → `第一章与第四至五章`
- `limited replay` → `第一章与第五章`
- `sharpness-aware minimization` → `第一章与第五章`
- `meta-continual learning` → `第一章与第五章`

Do not duplicate or rename existing `forward transfer` and `forward generalization`.

### Chapter status

Set:

- `1.2` → `in_progress`
- `1.2.1` → `drafted_and_verified`
- `1.2.2` → `drafted_and_verified`, artifact `chapters/ch01_introduction.tex`
- `1.2.3` → `queued`

Update `STATE.md`: 1.2.1 and 1.2.2 verified; next target 1.2.3; no 1.2.3 prose drafted.

## Step 5: build and audits

Run the full build, style audit, and reference-overlap audit using the same commands as prior tasks. Check:

- all active citations resolve;
- no duplicate BibTeX key/DOI/title;
- no undefined references, duplicate labels, missing files, or placeholders;
- CSV schemas and unique IDs/keys;
- byte-identical Section 1.1 and 1.2.1;
- body-empty 1.2.3 and Section 1.3;
- no benchmark-as-algorithm mischaracterization;
- no forward-transfer/forward-generalization conflation;
- unchanged `sources/`;
- visual inspection of all 1.2.2 and updated bibliography pages;
- PDF page count, size, SHA-256, and warning comparison.

## Step 6: report

Replace `handoff/LATEST_CODEX_REPORT.md` with a complete report covering preflight, exact prose integration, preserved hashes, references, evidence, terminology, status, compile/audits, visual inspection, source snapshot, unresolved issues, GitHub and Overleaf SHAs, and confirmation that 1.2.3 remains undrafted.

## Step 7: commit and synchronize

Use a content commit such as:

```bash
git commit -m "Draft Chapter 1 Section 1.2.2"
git push origin main
```

After verified push and clean worktree:

```bash
bash scripts/sync_latex_to_overleaf.sh "Sync Chapter 1 Section 1.2.2"
```

Record deployment in `handoff/LATEST_CODEX_REPORT.md` and `STATE.md`; push a report-only commit if needed. Do not sync Overleaf again for GitHub-only report changes. No force-push.

## Definition of done

- 1.2.2 integrated exactly;
- Sections 1.1 and 1.2.1 unchanged;
- 1.2.3 and Section 1.3 body-empty;
- verified references added or reused without duplicates;
- `C1-043`--`C1-059` present once;
- terminology and scopes valid;
- 1.2.2 verified and 1.2.3 queued;
- full build, audits, CSV checks, and visual inspection completed;
- `sources/` unchanged;
- GitHub and Overleaf synchronized or exact failure reported;
- clean worktree;
- no 1.2.3 prose drafted.

Do not continue beyond Section 1.2.2.
