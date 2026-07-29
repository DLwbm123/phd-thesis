# Codex Task: integrate Chapter 1, Section 1.1.1

Read and obey `AGENTS.md`, `THESIS_CONTRACT.md`, `AUTHORSHIP_PROTOCOL.md`, `AUTHOR_VOICE.md`, `STATE.md`, and `chapter_cards/ch01.md` before editing.

## Goal

Integrate the GPT Pro-approved draft for Section 1.1.1 “医学影像智能分析及其临床价值” into the thesis repository, add only the verified references and evidence records supplied below, compile the complete thesis, and run all required audits.

## Strict scope

Files that may be modified:

- `chapters/ch01_introduction.tex`
- `bibliography/references.bib`
- `config/build_flags.tex`
- `evidence/claims.csv`
- `qa/terminology.csv`
- `qa/chapter_status.csv`
- `STATE.md`
- `handoff/LATEST_CODEX_REPORT.md`

Do not modify any file under `sources/`. Do not import prose, citations, figures, or metadata from `sources/reference_thesis/`. Do not rewrite the approved academic prose except for a strictly necessary LaTeX syntax correction. If a scientific or stylistic concern is found, report it instead of silently rewriting it.

## Step 1: integrate the approved draft

In `chapters/ch01_introduction.tex`, replace the comment

```latex
% 当前写作起点：1.1.1
```

with the following text, preserving the existing subsection title and label:

```latex
医学影像将人体内部的解剖结构、组织形态及部分生理活动转换为可记录和比较的空间信息。X 射线、计算机断层成像、磁共振成像、超声成像和数字病理等技术具有不同的成像机理与信息尺度，但其临床解释通常都涉及对异常征象的识别、对器官或病灶范围的测量，以及对不同时间点、不同模态或不同个体影像的比较。医学影像智能分析因而不只是对图像给出一个类别标签，而是利用计算模型提取、组织和量化与诊疗任务相关的影像信息，为筛查、诊断、治疗规划和疗效随访提供可复核的分析结果。现有深度学习研究已覆盖分类、检测、分割、配准等多类医学影像任务\cite{litjens2017survey}。

医学图像分类主要建立图像内容与疾病类别、异常状态或风险水平之间的映射。根据任务粒度不同，模型可以处理整幅图像、局部候选区域或多幅影像组成的检查序列，输出离散类别或连续评分。这类结果可用于病例筛选、检查分诊和辅助鉴别，但其作用依赖于明确的适用人群、输入条件与决策阈值。以皮肤病变识别为例，Esteva 等利用临床图像和疾病标签训练卷积神经网络，说明端到端特征学习能够处理细粒度的医学图像分类问题\cite{esteva2017dermatologist}。此类研究展示了图像级预测的可行性，也表明分类模型的有效性与训练样本覆盖的疾病谱和成像条件密切相关。

医学图像分割需要为每个像素或体素赋予解剖结构、病灶或背景标签，其输出保留了目标在图像空间中的位置、边界和形态。与单一的图像级判断相比，分割结果能够进一步支持器官体积、病灶负荷、形状变化和空间邻接关系的定量分析，并可作为手术规划、放射治疗勾画和纵向随访中的基础信息。U-Net 通过编码路径获取上下文信息，并利用对称解码路径恢复空间定位，形成了医学图像分割中具有代表性的端到端建模方式\cite{ronneberger2015unet}。分割算法的临床价值并不只取决于平均重叠指标，还取决于边界误差、细小结构遗漏以及输出结果是否满足具体测量和规划需求。

医学图像配准则在两幅或多幅图像之间估计空间变换，使相同或对应的解剖位置建立一致关系。该任务可用于同一患者不同时间点影像的纵向比较、多模态信息融合、群体模板映射以及图像引导干预。传统配准方法往往针对每一对图像独立优化相似性度量与形变正则项；学习式方法将图像对到形变场的映射参数化为神经网络，在完成训练后可直接预测新的配准结果。VoxelMorph 是这一思路的代表性工作之一\cite{balakrishnan2019voxelmorph}。配准结果通常不直接给出疾病结论，但它为跨时间和跨模态分析提供统一坐标，是多阶段医学图像处理流程中的关键环节。

分类、分割和配准分别形成图像级判断、空间级描述和图像间对应关系，三者在临床分析中具有互补性。例如，配准可以将不同检查对齐到可比较的空间，分割可以量化局部结构及其变化，分类或风险预测再结合这些信息形成病例层面的判断。深度学习将许多依赖人工设计特征和逐例优化的流程转化为由数据学习的参数化映射，使模型能够在统一计算框架下处理高维医学图像。其价值主要体现在提供可重复的定量结果、减少部分重复性处理步骤，并扩大复杂影像信息被系统利用的范围；算法输出仍需结合临床资料、任务目标和人工复核进行解释，而不能等同于独立的临床诊断。

上述能力建立在训练数据能够充分描述目标任务的前提上。监督学习模型从图像及其标签中估计输入与输出之间的关系，样本规模、标注质量、疾病构成和采集条件会共同限定模型可以学习到的规律。医学影像数据的整理与专家标注本身具有较高成本，训练集也常难以同时满足规模、代表性和质量要求\cite{willemink2020preparing}。Zech 等对多医疗机构胸部 X 射线数据的研究进一步表明，模型在原训练机构内部的表现不能直接代表其在外部机构的表现，网络还可能利用与医院或采集流程相关的混杂信息\cite{zech2018variable}。因此，医学影像智能分析的临床价值不仅取决于模型在固定测试集上的预测性能，还取决于其在真实训练信息条件下获得可靠能力的方式。下一节将从标注、历史数据访问和医疗机构三个维度讨论这些训练信息限制。
```

## Step 2: add verified bibliography entries

Check `bibliography/references.bib` for duplicate DOI, duplicate title, or an existing equivalent key. Add the following entries only when no equivalent record exists. Preserve existing verified entries.

```bibtex
@article{litjens2017survey,
  author  = {Litjens, Geert and Kooi, Thijs and Ehteshami Bejnordi, Babak and Setio, Arnaud Arindra Adiyoso and Ciompi, Francesco and Ghafoorian, Mohsen and van der Laak, Jeroen A. W. M. and van Ginneken, Bram and S{\'a}nchez, Clara I.},
  title   = {A Survey on Deep Learning in Medical Image Analysis},
  journal = {Medical Image Analysis},
  volume  = {42},
  pages   = {60--88},
  year    = {2017},
  doi     = {10.1016/j.media.2017.07.005}
}

@inproceedings{ronneberger2015unet,
  author    = {Ronneberger, Olaf and Fischer, Philipp and Brox, Thomas},
  title     = {{U-Net}: Convolutional Networks for Biomedical Image Segmentation},
  booktitle = {Medical Image Computing and Computer-Assisted Intervention -- MICCAI 2015},
  series    = {Lecture Notes in Computer Science},
  volume    = {9351},
  pages     = {234--241},
  publisher = {Springer},
  year      = {2015},
  doi       = {10.1007/978-3-319-24574-4_28}
}

@article{balakrishnan2019voxelmorph,
  author  = {Balakrishnan, Guha and Zhao, Amy and Sabuncu, Mert R. and Guttag, John and Dalca, Adrian V.},
  title   = {{VoxelMorph}: A Learning Framework for Deformable Medical Image Registration},
  journal = {IEEE Transactions on Medical Imaging},
  volume  = {38},
  number  = {8},
  pages   = {1788--1800},
  year    = {2019},
  doi     = {10.1109/TMI.2019.2897538}
}

@article{esteva2017dermatologist,
  author  = {Esteva, Andr{\'e} and Kuprel, Brett and Novoa, Roberto A. and Ko, Justin and Swetter, Susan M. and Blau, Helen M. and Thrun, Sebastian},
  title   = {Dermatologist-Level Classification of Skin Cancer with Deep Neural Networks},
  journal = {Nature},
  volume  = {542},
  number  = {7639},
  pages   = {115--118},
  year    = {2017},
  doi     = {10.1038/nature21056}
}

@article{willemink2020preparing,
  author  = {Willemink, Martin J. and Koszek, Wojciech A. and Hardell, Cailin and Wu, Jie and Fleischmann, Dominik and Harvey, Hugh and Folio, Les R. and Summers, Ronald M. and Rubin, Daniel L. and Lungren, Matthew P.},
  title   = {Preparing Medical Imaging Data for Machine Learning},
  journal = {Radiology},
  volume  = {295},
  number  = {1},
  pages   = {4--15},
  year    = {2020},
  doi     = {10.1148/radiol.2020192224}
}

@article{zech2018variable,
  author  = {Zech, John R. and Badgeley, Marcus A. and Liu, Manway and Costa, Anthony B. and Titano, Joseph J. and Oermann, Eric Karl},
  title   = {Variable Generalization Performance of a Deep Learning Model to Detect Pneumonia in Chest Radiographs: A Cross-Sectional Study},
  journal = {PLOS Medicine},
  volume  = {15},
  number  = {11},
  pages   = {e1002683},
  year    = {2018},
  doi     = {10.1371/journal.pmed.1002683}
}
```

After the first real citations are present, change `\thesisbibliographyfalse` to `\thesisbibliographytrue` in `config/build_flags.tex` if it is still false.

## Step 3: append evidence records

Append the following rows to `evidence/claims.csv` after checking that the claim IDs do not already exist:

```csv
C1-001,1,1.1.1,深度学习已用于医学影像分类检测分割配准等多类任务,DOI:10.1016/j.media.2017.07.005,Abstract and task survey,litjens2017survey,literature,confirmed,drafted,用于建立任务范围
C1-002,1,1.1.1,端到端卷积神经网络可用于细粒度皮肤病变分类,DOI:10.1038/nature21056,Abstract and experimental design,esteva2017dermatologist,primary_experiment,confirmed,drafted,仅作为图像分类代表性实例
C1-003,1,1.1.1,U-Net 通过编码路径提取上下文并通过对称解码路径恢复定位,DOI:10.1007/978-3-319-24574-4_28,Abstract and architecture description,ronneberger2015unet,method,confirmed,drafted,不扩展为所有分割模型结论
C1-004,1,1.1.1,VoxelMorph 将图像对到形变场的映射参数化为神经网络,DOI:10.1109/TMI.2019.2897538,Abstract and formulation,balakrishnan2019voxelmorph,method,confirmed,drafted,作为学习式配准代表
C1-005,1,1.1.1,医学影像机器学习依赖规模充分经过整理且具有代表性的训练数据和专家标注,DOI:10.1148/radiol.2020192224,Abstract,willemink2020preparing,literature,confirmed,drafted,用于引出训练信息限制
C1-006,1,1.1.1,医疗机构外部数据上的模型表现可能低于原机构内部测试且模型可能利用机构相关混杂信息,DOI:10.1371/journal.pmed.1002683,Abstract and author summary,zech2018variable,primary_experiment,confirmed,drafted,结论限于该多机构胸片研究并采用审慎表述
C1-007,1,1.1.1,分类分割和配准分别提供图像级判断空间级描述和图像间对应关系,author synthesis based on cited task definitions,Section synthesis,litjens2017survey;ronneberger2015unet;balakrishnan2019voxelmorph,author_analysis,confirmed,drafted,属于任务功能层面的综合概括
```

Preserve the existing CSV header and quoting conventions. If commas require quoting, quote fields rather than changing the wording.

## Step 4: terminology and status

In `qa/terminology.csv`, add non-duplicate entries for:

```csv
medical image classification,医学图像分类,全文,医学影像分类（具体任务中避免混用）,领域总称可写医学影像智能分析
medical image segmentation,医学图像分割,全文,医学影像分割（具体任务中避免混用）,用于具体图像和算法任务
medical image registration,医学图像配准,全文,医学影像配准（具体任务中避免混用）,用于具体图像和算法任务
```

Update `qa/chapter_status.csv`:

- `1.1.1` → `drafted_and_verified`, artifact `chapters/ch01_introduction.tex`
- `1.1.2` → `queued`

Update `STATE.md` so that:

- Section 1.1.1 is recorded as integrated and compiled;
- the current/next section is 1.1.2 “医学影像训练信息的多维受限性”;
- the compilation and audit outcome is recorded accurately.

## Step 5: verification

Run the repository’s normal complete build. Then run:

```bash
python scripts/style_audit.py \
  --input chapters/ch01_introduction.tex \
  --patterns qa/style_red_flags.csv \
  --output qa/style_audit_report.md
```

If `sources/reference_thesis/` contains the reference thesis `.tex` files, run:

```bash
python scripts/reference_overlap_audit.py \
  --thesis chapters/ch01_introduction.tex \
  --reference sources/reference_thesis \
  --min-chars 28 \
  --output qa/reference_overlap_report.md
```

Check all of the following:

- full thesis compiles;
- all six citation keys resolve;
- no new undefined citation/reference;
- no duplicate bibliography DOI/title/key;
- no duplicate label;
- no missing file;
- no new TODO/TBD/??;
- style audit result is reported, not automatically rewritten;
- reference overlap result is reported, not concealed through superficial paraphrasing.

## Step 6: report

Write `handoff/LATEST_CODEX_REPORT.md` with:

1. modified files;
2. exact bibliography entries added or reused;
3. compile command and result;
4. citation/reference status;
5. style audit result;
6. reference-overlap audit result;
7. unresolved source or scientific issues;
8. confirmation that the next section is 1.1.2.

Do not continue drafting Section 1.1.2 in this task.
