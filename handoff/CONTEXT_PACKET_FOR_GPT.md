# GPT Pro 证据上下文包：2.1.2 医学图像配准

## 1. 当前任务

只起草第二章 2.1.2“医学图像配准”的正式正文；不得改动 2.1.1，不进入 2.1.3，也不得编造或补写第五章内容。本包提供的是已核查事实、术语、候选公式和边界，不能直接复制为正文。

## 2. 小节功能、边界与建议密度

- 功能：回答配准预测什么、如何以空间变换建模、如何由匹配项与正则项训练、以及如何评价；它不是持续配准研究现状或 SAMCL 方法章。
- 前接：2.1.1 在既定坐标系中描述区域与边界；本节建立不同图像间的空间对应。
- 后接：配准与分割输出空间结构；2.1.3 的分类在图像、检查或病例层面输出类别或风险。
- 建议顺序：任务定义与应用对象 → 坐标/变换方向 → 刚性、仿射与可变形模型 → 经典优化目标 → 学习式配准 → 评价与适用边界 → 过渡。
- 建议篇幅与密度：与 2.1.1 相当，约 5--7 个功能段和 4--6 个必要公式；不写方法排行榜、持续学习综述或实验描述。Dice 已在 2.1.1 定义，本节只交叉引用，不重复推导。

## 3. 当前 2.1 上下文（不得改写）

### 2.1 引言

> 医学影像智能分析的基本任务可以按照输出空间区分为分割、配准和分类。分割在图像网格上预测结构标签，配准估计图像之间的空间变换，分类则在图像、检查或病例层面输出类别或类别概率\cite{litjens2017survey}。三类任务可以共享特征提取思想，但其预测对象、监督单位和评价尺度不同，因而需要分别定义数学映射和性能指标。本节建立后续章节共同使用的任务记号，不展开弱监督、持续学习或联邦学习机制。

### 2.1.1 最后一段

> 分割在一个既定坐标系中描述区域和边界。若需要比较不同时间、不同模态或不同个体的图像，首先还需建立图像之间的空间对应关系。下一小节据此介绍医学图像配准的基本表述。

### 2.1.2 与 2.1.3 标题

```tex
\subsection{医学图像配准}
\label{subsec:foundations-registration}

\subsection{医学图像分类}
\label{subsec:foundations-classification}
```

## 4. 已核实术语与符号方案

| 术语/符号 | 建议中文或定义 | 使用边界与冲突检查 |
|---|---|---|
| medical image registration | 医学图像配准 | `qa/terminology.csv` 已登记；具体任务不写“医学影像配准”。 |
| fixed image / moving image | 固定图像 $I_F$ / 移动图像 $I_M$ | $I$ 已在 2.1.1 定义为输入图像；用下标区分，不与其冲突。 |
| $\Omega$ | 图像空间域 | 已登记为离散图像域；正文须说明数组索引与物理坐标不同。 |
| $\mathbf{x}$ | 固定图像域中的空间坐标 | 仅在本节局部使用；距离性指标优先在物理空间报告。 |
| $\phi:\Omega_F\!\to\!\Omega_M$ | 从固定坐标查询移动图像的空间变换 | 采用 backward-warp/重采样约定：$I_M\circ\phi$ 与 $I_F$ 比较；全节不得混用方向。该方向与 SAMCL 原文第 3 节一致。 |
| $\mathbf{u}$ | 位移场 | $\phi(\mathbf{x})=\mathbf{x}+\mathbf{u}(\mathbf{x})$；$\mathbf{u}$ 未在 `qa/notation.csv` 登记，正文获准写入时须登记。 |
| $W(I_M,\phi)$ | 重采样后的移动图像 | 可作为 $I_M\circ\phi$ 的实现记号；首次出现说明由插值实现。 |
| $g_\theta$、$\theta$ | 配准网络及其参数 | $\theta$ 已跨章节定义；$g_\theta(I_F,I_M)$ 输出 $\phi_\theta$。 |
| $D$、$R$、$\lambda$ | 相似性项、正则项及其权重 | 新局部记号；须首次定义并在实际正文集成时登记。 |
| $J_\phi$ | $\phi$ 的 Jacobian 矩阵 | 使用 $\det J_\phi$ 讨论局部体积变化或非正 Jacobian 比例；平滑不自动推出可逆或拓扑保持。 |

**方向约定必须固定：** $\mathbf{x}\in\Omega_F$ 是固定图像坐标，$\phi(\mathbf{x})\in\Omega_M$ 是移动图像采样位置，故注册后的移动图像为 $I_M(\phi(\mathbf{x}))$。该约定并不声称是唯一写法；其目的仅是避免本节同时使用 forward warp 与 backward warp。

## 5. 论断—证据表

| claim_id | 拟支持论断 | 类型 | 原始来源与定位 | 建议 citation key | 可直接用于正文 |
|---|---|---|---|---|---|
| C2-010 | 配准估计使固定图像与移动图像中对应结构对齐的空间变换；应用对象可包括纵向、跨模态、跨个体或模板对应。 | source_fact | Sotiras et al. 2013，Abstract：列出多模态融合、纵向研究和人群/图谱建模；SAMCL `Paper-0150.tex` 第 3 节第 149--158 行给出 fixed/moving 与 $\phi:\Omega_F\to\Omega_M$。 | `sotiras2013deformable`; `wang2024samcl` | 是；需以基础定义表述，不写 SAMCL。 |
| C2-011 | 输出是空间变换或位移场，而非离散类别；可写 $\phi(\mathbf{x})=\mathbf{x}+\mathbf{u}(\mathbf{x})$。 | author_definition | SAMCL 第 3 节第 149--150 行支持变换/网络映射；位移形式是作者的通用记号整理。 | `wang2024samcl` | 是，标明为统一记号。 |
| C2-012 | 刚性、仿射与可变形模型对应逐步增加的自由度；B 样条 FFD 是可变形模型实例。 | source_fact | Rueckert et al. 1999，Abstract：全局仿射与局部 B 样条 FFD；Sotiras et al. 2013，Abstract/Fig. 1：变形模型分类。 | `rueckert1999ffd`; `sotiras2013deformable` | 是。 |
| C2-013 | 经典优化可统一为图像匹配项加变换正则项；正则反映对形变平滑或几何性质的假设。 | source_fact + caution | Rueckert et al. 1999，Abstract：相似性与平滑代价结合；SAMCL 第 3 节第 151--158 行：$D+R$；第 317--319 行仅为 SAMCL 实验中的具体实例，不能泛化为唯一选择。 | `rueckert1999ffd`; `wang2024samcl` | 是，避免将任一正则说成必然物理真实。 |
| C2-014 | 同模态匹配可采用强度差或相关性；跨模态可采用互信息，但具体选择取决于成像关系和任务假设。 | source_fact + caution | Pluim et al. 2003，Abstract：互信息配准的预处理、插值、优化和几何变换因素；Rueckert et al. 1999，Abstract：归一化互信息实例。 | `pluim2003mi`; `rueckert1999ffd` | 是。 |
| C2-015 | 微分同胚约束是可变形配准的一类重要约束；可简述其与平滑、可逆和拓扑保持目标有关，但不得由“平滑”单独推出可逆。 | source_fact + caution | Avants et al. 2008，Abstract：在 topology-preserving diffeomorphic maps 空间进行优化；SAMCL 第 317--319 行仅说明其实验采用 stationary velocity field 的微分同胚变换。 | `avants2008syn` | 是；不展开 LDDMM。 |
| C2-016 | 学习式配准以参数化模型将图像对映射到形变场，替代对每个图像对单独迭代优化。 | source_fact | Balakrishnan et al. 2019，PubMed Abstract：CNN 将图像对映射到形变场，并指出传统逐对优化的代价。 | `balakrishnan2019voxelmorph` | 是。 |
| C2-017 | 不依赖真值形变的学习式配准并非没有训练信号：图像匹配目标和形变正则仍提供优化信号；有辅助分割时可作为额外监督。 | source_fact | Balakrishnan et al. 2019，PubMed Abstract：无监督设置最大化基于强度的匹配目标；第二种设置使用训练集辅助分割。 | `balakrishnan2019voxelmorph` | 是；不要写成“完全无监督”。 |
| C2-018 | 可微空间采样/重采样使基于配准后图像的损失能够对变换参数反向传播。 | source_fact | Jaderberg et al. 2015，NeurIPS 官方论文 Abstract/第 1 节：可微 spatial transformer 可用标准反向传播端到端训练。 | `jaderberg2015stn` | 是；将其作为一般计算机制，不称为医学配准创新。 |
| C2-019 | 配准评价可使用标志点 TRE、变换标签后的 Dice/区域重叠、图像相似性、形变规则性和运行时间；指标应随可用参考信息与任务变化。 | author_analysis grounded in sources | SAMCL 第 303--319 行：对应解剖标签用 Dice、对应标志点用毫米 TRE；Klein et al. 2009，Abstract/Fig. 2--3：标签重叠和边界距离用于评价。 | `wang2024samcl`; `klein2009evaluation` | 是；Dice 仅交叉引用 2.1.1。 |
| C2-020 | 图像相似性或整体标签重叠不是局部配准准确性的充分证据。 | source_fact | Rohlfing 2012，Abstract：单独或组合的图像相似性、组织重叠等 surrogate measures 不能作为准确配准的有效证据。 | `rohlfing2012surrogates` | 是，使用审慎限定。 |
| C2-021 | TRE 候选公式应以对应标志点在物理坐标中的欧氏距离定义，报告时说明点集、单位和聚合方式。 | author_definition; TODO-EVIDENCE | SAMCL 第 303--306 行仅确认 TRE 以毫米用于 NLST；本轮未为通用 TRE 数学式定位单一原始定义文献。 | `wang2024samcl` | 仅可在补充原始指标来源后直接用于正文。 |

## 6. 候选公式表（均未写入论文）

| 编号 | 功能与候选形式 | 符号/事实来源 | 性质 |
|---|---|---|---|
| F1 | 重采样：$I_M^{\phi}(\mathbf{x})=W(I_M,\phi)(\mathbf{x})=I_M(\phi(\mathbf{x}))$。 | 方向与 $m\circ\phi_\theta$ 来自 SAMCL 第 3 节第 149--158 行；$W$ 是作者的实现记号。 | 一般定义。 |
| F2 | 位移场：$\phi(\mathbf{x})=\mathbf{x}+\mathbf{u}(\mathbf{x})$。 | 常用作者统一记号；SAMCL 直接使用 $\phi$，未以该式定义位移场。 | 作者整理；首次写入正文须定义 $\mathbf{u}$。 |
| F3 | 经典能量：$\widehat\phi=\arg\min_\phi\;D(I_F,I_M\circ\phi)+\lambda R(\phi)$。 | SAMCL 第 3 节第 158 行为 $D+R$；Rueckert 1999 Abstract 支持相似性与平滑代价组合。 | 一般目标；不是 SAMCL 原始公式。 |
| F4 | 学习式目标：$\widehat\theta=\arg\min_\theta\;\mathbb{E}_{(I_F,I_M)\sim\mathcal D}[D(I_F,I_M\circ\phi_\theta)+\lambda R(\phi_\theta)]$，其中 $\phi_\theta=g_\theta(I_F,I_M)$。 | SAMCL 第 3 节第 150--158 行；VoxelMorph Abstract 支持图像对到形变场的学习映射。 | 一般目标；绝不写作 SAMCL 连续目标。 |
| F5 | TRE：$\operatorname{TRE}=\frac{1}{N}\sum_{i=1}^{N}\lVert \phi(\mathbf{p}_i)-\mathbf{q}_i\rVert_2$，坐标应为物理空间。 | SAMCL 只支持 TRE 的毫米报告；通用公式的原始指标来源尚待补。 | `TODO-EVIDENCE` 后才可入正文。 |
| F6 | 规则性候选：$r_{\le0}=\frac{1}{|\Omega|}\sum_{\mathbf{x}\in\Omega}\mathbb{1}[\det J_\phi(\mathbf{x})\le0]$。 | Jacobian 行列式用于描述局部体积变化；本轮未定位单一原始论文对该特定阈值统计的定义。 | `TODO-EVIDENCE`；不得把低比例写成充分准确性或必然拓扑保持。 |

## 7. 经核验 BibTeX 候选（正文集成时按最小实际使用集合写入文献库）

`balakrishnan2019voxelmorph` 已存在于 `bibliography/references.bib`，元数据与 PubMed 核验一致。本轮不修改文献库。以下 key 均为建议 key：

```bibtex
@article{sotiras2013deformable,
  author={Sotiras, Aristeidis and Davatzikos, Christos and Paragios, Nikos},
  title={Deformable Medical Image Registration: A Survey},
  journal={IEEE Transactions on Medical Imaging}, volume={32}, number={7}, pages={1153--1190}, year={2013},
  doi={10.1109/TMI.2013.2265603}
}
@article{rueckert1999ffd,
  author={Rueckert, Daniel and Sonoda, L. I. and Hayes, C. and Hill, D. L. G. and Leach, M. O. and Hawkes, D. J.},
  title={Nonrigid Registration Using Free-Form Deformations: Application to Breast MR Images},
  journal={IEEE Transactions on Medical Imaging}, volume={18}, number={8}, pages={712--721}, year={1999},
  doi={10.1109/42.796284}
}
@article{pluim2003mi,
  author={Pluim, Josien P. W. and Maintz, J. B. Antoine and Viergever, Max A.},
  title={Mutual-Information-Based Registration of Medical Images: A Survey},
  journal={IEEE Transactions on Medical Imaging}, volume={22}, number={8}, pages={986--1004}, year={2003},
  doi={10.1109/TMI.2003.815867}
}
@article{avants2008syn,
  author={Avants, Brian B. and Epstein, Charles L. and Grossman, Murray and Gee, James C.},
  title={Symmetric Diffeomorphic Image Registration with Cross-Correlation: Evaluating Automated Labeling of Elderly and Neurodegenerative Brain},
  journal={Medical Image Analysis}, volume={12}, number={1}, pages={26--41}, year={2008},
  doi={10.1016/j.media.2007.06.004}
}
@inproceedings{jaderberg2015stn,
  author={Jaderberg, Max and Simonyan, Karen and Zisserman, Andrew and Kavukcuoglu, Koray},
  title={Spatial Transformer Networks},
  booktitle={Advances in Neural Information Processing Systems}, volume={28}, year={2015}
}
@article{klein2009evaluation,
  author={Klein, Arno and Andersson, Jesper and Ardekani, Babak A. and others},
  title={Evaluation of 14 Nonlinear Deformation Algorithms Applied to Human Brain MRI Registration},
  journal={NeuroImage}, volume={46}, number={3}, pages={786--802}, year={2009},
  doi={10.1016/j.neuroimage.2008.12.037}
}
@article{rohlfing2012surrogates,
  author={Rohlfing, Torsten},
  title={Image Similarity and Tissue Overlaps as Surrogates for Image Registration Accuracy: Widely Used but Unreliable},
  journal={IEEE Transactions on Medical Imaging}, volume={31}, number={2}, pages={153--163}, year={2012},
  doi={10.1109/TMI.2011.2163944}
}
```

## 8. 不得进入 2.1.2 的内容

- SAMCL 的任务序列、有限经验回放、元持续学习、内外层更新、锐度感知优化、算法、消融、结果或创新结论；这些属于第五章 5.4。
- 灾难性遗忘、稳定性—可塑性、历史访问或持续学习设定；这些属于 2.2/2.3 或第五章。
- ScribbleCL 的任务、实验、指标、结果或任何未完成的 `TODO-EXPERIMENT` 内容。
- LDDMM 推导、方法排行榜、配准实验设置，或把图像相似性/Dice 当作充分准确性证据。

## 9. TODO-EVIDENCE

1. 为 TRE 的一般数学定义定位并核验一个原始指标来源，再允许 F5 进入正文；SAMCL 仅支持其在对应标志点上以毫米报告。
2. 为非正 Jacobian 比例的具体统计形式定位原始方法来源；在此之前，F6 只可作为候选，不得写成统一标准或准确性证明。

## 10. 给 GPT Pro 的固定输出要求

仅在作者确认可以开始起草后输出以下四个区块，且不得突破本包的证据与边界：

```text
[THESIS DRAFT]
只给出 2.1.2 医学图像配准正文；不要改动 2.1.1、2.1.3 或其他章节。

[EVIDENCE UPDATE]
逐条列出实际采用的 claim_id、citation key、公式编号和仍未解决的 TODO-EVIDENCE。

[CODEX TASK — COPY ONLY THIS BLOCK]
只给出将正文、实际使用的 BibTeX 条目、证据账本和符号表写入仓库所需的精确操作；不得执行这些操作。

[NEXT]
说明需要作者确认或 Codex 继续核验的事项。若 TRE/Jacobian TODO-EVIDENCE 未关闭，不得把相应候选公式作为已核实事实。
```
