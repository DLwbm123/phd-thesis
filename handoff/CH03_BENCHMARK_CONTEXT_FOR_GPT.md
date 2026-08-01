# 第三章 Benchmark 整章证据上下文（仅供 GPT Pro 整章写作）

## 0. 使用边界

- 本包只提供证据、结构、公式和写作边界，不是第三章正文；不得逐句翻译英文稿。
- 章节定位：**持续医学图像分割的场景定义、统一协议、综合评价与系统实证**；不是综述，也不是单一抗遗忘算法。
- 只可把下列结果限定为该原始工程中的数据、网络、任务顺序、训练预算与实现版本；三类场景不穷尽持续医学影像问题，不得据此宣称所有任务上的统一排名。
- 不引入第四章 FedSubMerge、第五章 ScribbleCL 或 SAMCL 的方法内容。ScribbleCL 仍为 `TODO-EXPERIMENT`。

## 1. 原始材料清单与版本判断

|路径|作用与关系|采用状态|
|---|---|---|
|`sources/benchmark/Benchmark_pa/main.tex`|主论文唯一主入口；含正文、6 个活动表、4 个活动主图、内嵌 `thebibliography`，并引用补充材料的训练细节。|实际采用版本，1,431 行；无独立 `.bib`。|
|`sources/benchmark/Benchmark_pa/supplementary.tex`|补充材料；给出 ResUNet32、输出头、训练超参数、回放设置和各法超参数。|实际采用版本，119 行。|
|`sources/benchmark/Benchmark_pa/img/benchmark_overview_new.pdf`|主图 `fig:benchmark_overview`，概览三场景、协议、方法家族和评价维度。已实际视觉检查。|活动图。|
|`.../img/task_robustness_adice.pdf`、`task_robustness_bwt_from_bottom.pdf`|`fig:task_order_robustness` 的两个子图；十个 Domain-CL 顺序的 A-Dice/BWTR。已实际视觉检查 A-Dice 图。|活动图。|
|`.../img/domain_memory_size_adice.pdf`、`SAM_confusion_matrix.pdf`|`fig:memory` 的缓存规模曲线与 SAM/LoRA 任务矩阵。前者已实际视觉检查。|活动图；后者缺正文数值账本。|
|`.../img/plots_for_benchmark.pdf`|`fig:figure_machine_learning`，CL 与相邻学习范式的关系。|活动图，但只宜放 3.7/附录，不能替代本章实证。|
|`img/Balance.pdf`、`radar.pdf`、`tsne_of_prostate.png`、两张 `seg_tricks*.png`、`task_robustness_bwt.pdf`|源树存在但在主稿中注释或未引用。|不作为正式第三章证据；若需使用必须重新核实。|
|源树中的 `ce.pdf`、`dse.pdf`、`mpe.pdf`、`task_robustness_fwt.pdf`|无活动 LaTeX 引用。|不进入本章，除非作者提供对应说明和数值来源。|

### 编译与版本核验

- 在仓库外临时副本运行 `latexmk -pdf -interaction=nonstopmode -file-line-error main.tex` 未成功：本机 TinyTeX 缺少 `makecell.sty`，并缺 Palatino `ppl` 字体度量；未在 `sources/` 写入任何构建产物，也未补装依赖。因此**没有可核验的主论文 PDF 页数**，不可写成“原论文已在本机成功编译”。
- 源目录无 Git 元数据、无论文 PDF、无训练脚本、无配置、无指标实现、无随机种子或逐运行日志；当前可见的唯一版本依据是上述实际文件清单及内容一致性。
- 主论文表格、公式、图片均直接取自 `main.tex`；补充材料只补足设置。主稿与补充材料均未给出代码链接或 commit。
- `sources/benchmark/` 的开始与结束清单均为 31 个普通文件；按“每个文件 SHA-256 + 相对路径”排序后得到的清单 SHA-256 均为 `b9a529ada136e552fcd183df573d98c32048b0db53d3b0169a8490af879e8cad`。主文件 SHA-256 为 `b88ae877066b6e826f968a2239c9047d56c32e33bacfe94ffa2c3b10c2b8a1ee`，补充材料为 `34813f5d264b97b6404a9b74fca5fdf889ec33d97c4ff8c5b101073cf7fcba4b`；未变更。

## 2. 原论文到博士章节的映射

|原论文内容|第三章位置|保留的事实基础|博士论文需要重组/扩写|不进入正文|
|---|---|---|---|---|
|Introduction, lines 194--302|3.1|问题缺口、三场景、超越遗忘的评价动机|接到第一章“任务持续演化与训练信息受限”，避免“首个”绝对表述|逐句背景铺陈、泛化临床承诺。|
|Definitions, lines 329--434|3.2--3.3|任务集、数据分布、标签空间和三场景条件|统一训练/测试时点、身份可用性和背景语义的缺失边界|未写明的 task-free 假设。|
|Desiderata/metrics, lines 435--578|3.5|A-Dice、BWTR、RMA、E-FWT、WCD、MPE、DRR|明确适用范围、方向、比较边界与性能矩阵|没有代码支撑的实现细节。|
|Methods/datasets, lines 581--656 + supplement|3.4|方法家族、数据、预处理和超参数|按协议而非按方法宣传组织|未报告的硬件、种子、早停和实现版本。|
|Results, lines 657--925|3.6--3.7|三张完整结果表、顺序/缓存分析|按稳定性、可塑性、泛化与资源权衡综合分析|把单表最优外推为通用方法。|
|Discussion, lines 971--1057|3.7--3.8|研究边界和未来方向|转为证据限定的局限与小结|基础模型的未经充分协议化比较。|

## 3. 全章论证链与段落级提纲

|节|功能、论断顺序与过渡|建议段落数/证据|结论边界|
|---|---|---|---|
|3.1 引言|从顺序到达的中心、类别、器官变化切入；指出单一遗忘不足；说明本章先给出场景、协议、指标再比较代表策略；过渡到形式定义。|4 段；`B-CLAIM-001--003`、`B-FIG-001`。|不称“唯一/首个”；不承诺临床部署。|
|3.2 问题定义|定义任务序列、数据集、训练后模型与阶段—任务 Dice 矩阵；说明历史数据访问是方法条件、而不是统一假设；过渡到三类变化。|4 段；`B-EQ-001`、`B-TAB-002`。|源稿没有 task identity 在训练/测试是否提供的正式协议，必须 `NOT-REPORTED`。|
|3.3 场景|先给共同点，再依次说明 Domain/Class/Organ 的分布、标签、目标、背景语义与不可统一处。|每小节 2--3 段；`B-CLAIM-004--006`、`B-TAB-002`、`B-FIG-001`。|Class-CL 背景语义的实现协议未完整形式化；不把三者作为穷尽分类。|
|3.4 数据与统一协议|以“数据—阶段—预处理—网络—方法—预算”组织；明确缺失字段，不以常识补齐。|5 段 + 2 表；`B-TAB-003`、`B-CLAIM-007`。|样本量、种子、硬件、代码版本、早停均 `NOT-REPORTED`。|
|3.5 指标|先给性能矩阵，再逐一给 A-Dice/BWTR/RMA/E-FWT/WCD/MPE/DRR；说明 E-FWT 仅 Domain-CL。|6 段；`B-EQ-002--008`。|公式可由主稿核验，代码实现不可核验（BLOCKER）。|
|3.6 结果|按场景和能力维度综合三张表，之后写任务顺序与缓存敏感性；完整引用表而非逐方法复述。|6--8 段 + 3 表 + 2 图；`B-EXP-001--004`。|所有数字只限 ResUNet32、给定任务序列/预算；SAM 图不单列结论。|
|3.7 发现与局限|归纳“性能/遗忘不足以完整评价”“稳定—可塑性—资源取舍”“前向泛化未解决”；随后列证据缺口。|4 段；`B-CLAIM-008--011`、`B-LIM-001--008`。|将机制解释写为作者分析，不能作因果证明。|
|3.8 小结|回收场景、协议和指标语言，并说明其为第四、五章提供参照；不得重复结果数字。|2 段；前节证据。|不将 benchmark 当作后续方法组件。|

## 4. 问题定义、统一记号与候选公式

### 4.1 统一符号

|符号|本章建议定义|与原文|
|---|---|---|
|`t\in\mathcal{T}=\{1,\ldots,T\}`|当前连续训练阶段/任务索引。|一致（main 367--373）。|
|`\mathcal{D}_t=\{(x_i^t,y_i^t)\}_{i=1}^{N_t}`|第 `t` 阶段训练集。|一致。|
|`\mathbb{D}_t=P(\mathcal{X}_t,\mathcal{Y}_t)`|第 `t` 任务的图像—标签联合分布。|一致。|
|`Y_t`|任务 `t` 的解剖结构/子结构标签集合；必须另行写明是否含背景。|一致；背景协议不完整。|
|`d_{t,i}`|完成第 `t` 任务训练后的模型在任务 `i` 测试集上的平均 Dice。|一致（517）。|
|`d_i^{NC}`、`d_{0,i}`|仅训练任务 `i` 的 Non-CL Dice；随机初始化模型在任务 `i` 的 Dice。|一致（538、549）。|
|`\theta_t`、`\mathrm{Param}(\theta_t)`|第 `t` 阶段参数及其数量。|一致（564）。|

训练后完整性能矩阵应表示为 `\mathbf D=[d_{t,i}]_{t,i=1}^{T}`；这是**作者重组记号**，用于把原文逐项 `d_{t,i}` 统一为矩阵，不是原文公式。源稿只明确给出训练后评测定义，未说明每个阶段是否测试全部历史/未来任务的执行脚本，未来任务项由 E-FWT 定义隐含需要。

|ID|精确 LaTeX、方向和范围|来源/性质|
|---|---|---|
|B-EQ-001|`\mathcal{D}_t=\{(x_i^t,y_i^t)\}_{i=1}^{N_t},\quad (x_i^t,y_i^t)\overset{\mathrm{i.i.d.}}{\sim}P(\mathcal{X}_t,\mathcal{Y}_t).`|main 367--373；作者将同段定义合并。|
|B-EQ-002|`\mathrm{A\!\!\text{-}\!Dice}=\frac{1}{T}\sum_{i=1}^{T}d_{T,i}`；越大越好，Dice 通常在 `[0,1]`。|main 524--526，原论文公式。|
|B-EQ-003|`\mathrm{BWTR}=\frac{1}{T-1}\sum_{i=1}^{T-1}\frac{d_{T,i}-d_{i,i}}{d_{i,i}}`；越大越好；要求 `d_{i,i}>0`，0 表示最终与初学性能相同。|main 529--531，原论文公式。|
|B-EQ-004|`\mathrm{RMA}=\frac{1}{T-1}\sum_{i=2}^{T}\frac{d_{i,i}}{d_i^{NC}}`；越接近 1 表示与独立训练相当；需 `d_i^{NC}>0`，可大于 1。|main 535--540，原论文公式。|
|B-EQ-005|`\mathrm{E\!\text{-}FWT}=\frac{2}{T(T-1)}\sum_{t=1}^{T-1}\sum_{i=t+1}^{T}(d_{t,i}-d_{0,i})`；越大越好；仅 Domain-CL，范围不在源稿中给定。|main 545--549，原论文公式。|
|B-EQ-006|`\mathrm{WCD}=d_{\mathrm{all}}`；越大越好；只用于 Class-CL 最终已见类别。|main 551--553，原论文定义。|
|B-EQ-007|`\mathrm{MPE}=\frac{1}{T-1}\sum_{t=2}^{T}\frac{\mathrm{Param}(\theta_t)-\mathrm{Param}(\theta_{t-1})}{\mathrm{Param}(\theta_1)}`；越小越好，初始 backbone 相同才可公平比较。|main 560--565，原论文公式。|
|B-EQ-008|`\mathrm{DRR}=\frac{1}{T-1}\sum_{t=1}^{T-1}\frac{N_t^{\mathrm{replay}}}{N_t^{\mathrm{train}}}`；越小越好；星号另标原始图像回放。|main 571--575，原论文公式。|

**指标核验结果。** RMA 的分母确为每个后续任务的独立 Non-CL 参考；E-FWT 的基线确为随机初始化 `d_{0,i}`，并对每个已训练阶段到所有未来域求和，非仅相邻域；BWTR 比较最终阶段与刚学到该任务时的性能，非历史最佳或相邻阶段。源树**没有指标实现代码**，所以“公式—代码一致性”对 RMA/E-FWT/MPE/DRR 均为 `NOT-VERIFIABLE`（`B-LIM-001`，BLOCKER）。最小数值单元核查：若 `T=3`，RMA 恰为 `(d_{2,2}/d_2^{NC}+d_{3,3}/d_3^{NC})/2`；E-FWT 恰含 `(d_{1,2}-d_{0,2})`、`(d_{1,3}-d_{0,3})`、`(d_{2,3}-d_{0,3})` 三项，和原式索引一致。

## 5. 三类场景、数据与任务序列

|场景|医学动机/变化|标签、输出与背景|阶段、访问与测试|与相近范式的区别|
|---|---|---|---|---|
|Domain-CL|多中心、扫描协议和人群差异；`P(\mathcal X_{t_1})\ne P(\mathcal X_{t_2})`。|标签空间相同 `Y_{t_1}=Y_{t_2}`；单头 2 通道；背景语义未另述。|6 个顺序中心任务；历史原始数据是否可访问取决于方法；E-FWT 评未来未训练域。测试 task identity `NOT-REPORTED`。|区别于域适应/泛化：本章要求顺序学习后保持既往域；但源稿未给形式化比较协议。|
|Class-CL|同一心脏 FOV 中持续加入结构；图像分布相同。|`Y_{t_1}\ne Y_{t_2}`；8 通道单头；当前背景可含旧/未来类，构成 background shift。|3 阶段：LV/LA/MYO→RV/RA→AA/PA；最终 WCD。任务身份/旧类标签可访问性 `NOT-REPORTED`。|不同于类增量分类：稠密像素输出及背景语义改变；不同于多任务学习：按阶段、非同时训练。|
|Organ-CL|器官、病灶与模态都变；`P(\mathcal X_{t_1})\ne P(\mathcal X_{t_2})`。|标签集合不交 `Y_{t_1}\cap Y_{t_2}=\emptyset`；多头，每任务 2 通道。|4 阶段：左心房 MRI→前列腺 MRI→肝 CT→脑肿瘤 FLAIR MRI；E-FWT 不适用。|不同于多任务学习：非同时获得；跨任务目标不同，不能把跨任务 Dice 当作 forward generalization。|

|数据/场景|模态、区域、中心/域及任务|样本量与划分|预处理/标签|来源定位|
|---|---|---|---|---|
|NCI-ISBI13、I2CVB、PROMISE12 / Domain-CL|前列腺 T2 MRI；六中心 A--F：NCI-ISBI13 A/B，I2CVB C，PROMISE12 D/E/F。|每个分割任务随机 60%/15%/25% 训练/验证/测试；**每中心样本量未报告**。|C 中心裁剪对齐；轴位 `256×256`；非零体素均值/标准差归一化；前列腺标签。|main 636--649；`dataset_prostate2`、`dataset_prostate`、`dataset_prostate3`、`dataset_domaincl`。|
|MMWHS / Class-CL|心脏 CT；7 个全心结构。|同上；总体样本量 `NOT-REPORTED`。|轴位、平面分辨率 `0.78×0.78` mm、平均层厚 1.60 mm，resize `256×256`；三阶段类别如上。|main 650--656；`care25ASA1`、`discussion_inter_seg3`、`care25ASA2`。|
|LAScarQS / Organ-CL T1|左心房 LGE MRI，左心房分割。|同上；样本量 `NOT-REPORTED`。|每图零均值单位方差，切片 `256×256`。|main 660--665；`dataset_lascars`、`dataset_lascars2`。|
|PROMISE12 / Organ-CL T2|前列腺 MRI。|同上；采用 Domain-CL 中心 D。|同上。|main 660--665；`dataset_prostate3`。|
|LiTs / Organ-CL T3|肝脏 CT。|同上；样本量 `NOT-REPORTED`。|同上。|main 660--665；`dataset_taskcl`。|
|FeTS 2021 / Organ-CL T4|脑 FLAIR MRI，脑肿瘤。|同上；样本量 `NOT-REPORTED`。|同上。|main 660--665；`dataset_taskcl2`。|

## 6. 对比方法与统一设置

- 共同 backbone：ResUNet32；Domain-CL 为 2 通道头，Class-CL 为 8 通道头，Organ-CL 为每任务 2 通道多头（supplement 14--16）。
- 每到达任务：SGD，150 epochs，初始 LR 0.008，80 epoch 后乘 0.5，batch 8；Domain/Organ 交叉熵，Class 使用 MiB 无偏交叉熵（supplement 17--18）。随机种子、硬件、模型选择/早停、实现仓库和 commit 均 `NOT-REPORTED`。
- 回放：buffer 32，replay batch 8，默认 reservoir sampling；Class-CL 对 replay 做“slight modifications”，但没有细节（supplement 20--22）。

|类别|方法|实施来源/已报告参数|
|---|---|---|
|正则化|Regu-EWC、Regu-SI、Regu-LwF|EWC `λ=1,γ=0.1`；SI `c=5,ξ=1`；LwF penalty 3、temperature 2、weight decay 0.0005（supplement 25--31）。|
|回放|Repl-ER、GSS、GEM、GPM、AGEM、DER、DER++、FDR|GSS gradient comparison batch 8；GEM margin 0.5；GPM subspace threshold 0.97；DER penalty 0.4；FDR penalty 0.5；其余见共同 buffer 设置。DER++ 表述为沿用 formulation，无单独超参。|
|参数隔离|ParIso-PNN、ParIso-DAN|PNN 无额外超参；DAN linear combination for adaptation。两者扩展网络（supplement 38--40）。|
|Class-CL 专项|ClassCL-PLOP、ClassCL-MiB|PLOP pooled-output distillation 0.01、uncertainty threshold 0.001；MiB distillation 10、`α=1.0`（supplement 24--27）。|
|参照|Non-CL、JointTrain|Non-CL 顺序普通训练；JointTrain 汇集全部任务训练数据。后者是访问条件不同的参照上界，不能与受限访问方法作同条件优越性宣称（main 589--598）。|

## 7. 表格与图像账本

### 7.1 表格账本（所有数值可回溯）

|ID|原表/场景/数据|内容与可支持范围|博士论文处置|
|---|---|---|---|
|B-TAB-001|`tab:related_work`，main 278--302|相关 survey/benchmark 覆盖的场景和评价维度。仅支持定位差异，不能证明“首个”。|3.1 压缩为相关工作对比或附录。|
|B-TAB-002|`tab:CL_settings`，341--365|三场景的 label/distribution 条件。|3.3 保留并中文重排。|
|B-TAB-003|`tab:domain-cl`，694--723|完整 Domain-CL 数值，见下列紧凑账本。|3.6 保留。|
|B-TAB-004|`tab:class-cl`，727--758|完整 Class-CL 数值，见下列紧凑账本。|3.6 保留。|
|B-TAB-005|`tab:Organ-CL`，779--818|完整 Organ-CL 数值，见下列紧凑账本。|3.6 保留。|

数值格式均为 `A-Dice; BWTR; RMA; [E-FWT/WCD]; MPE; DRR`，`*` 表原始样本回放；`/` 为未报告/不适用。

```text
B-EXP-001 Domain-CL (B-TAB-003):
EWC .672±.021;-.242±.039;1.086±.014;.255±.152;0;0 | SI .676±.024;-.236±.042;1.084±.008;.259±.151;0;0 | LwF .663±.029;-.090±.027;.894±.021;.224±.153;0;0
ER .750±.021;-.100±.027;1.054±.014;.256±.150;0;.027* | GSS .726±.026;-.140±.040;1.059±.010;.255±.150;0;.036* | GEM .718±.018;-.095±.022;.994±.024;.251±.154;0;.042* | GPM .661±.010;-.188±.010;1.013±.022;.212±.080;0;.113 | AGEM .740±.015;-.093±.023;1.023±.027;.253±.155;0;.042* | DER .715±.011;-.126±.015;1.018±.016;.249±.148;0;.027* | DER++ .725±.013;-.105±.018;1.012±.013;.251±.149;0;.027* | FDR .728±.015;-.111±.028;1.025±.033;.252±.136;0;.042*
PNN .789±.002;0±0;1.003±.014;.235±.148;1.112;0 | DAN .786±.008;0±0;1.016±.021;.312±.210;.111;0 | Non-CL .676±.021;-.237±.038;1.086±.008;.260±.151;0;0 | JointTrain .830±.040;/;/;/;0;0
B-EXP-002 Class-CL (B-TAB-004):
EWC .487±.020;-.552±.042;.999±.022;.513±.022;0;0 | SI .469±.007;-.602±.016;1.018±.028;.570±.020;0;0 | LwF .384±.022;-.575±.013;.782±.046;.602±.002;0;0
ER .654±.034;-.243±.068;1.015±.029;.596±.019;0;.011* | GSS .456±.003;-.611±.016;.991±.038;.600±.006;0;.018* | GEM .684±.036;-.304±.038;1.014±.031;.622±.031;0;.010* | GPM .575±.023;-.219±.033;.892±.014;.513±.014;0;.068 | AGEM .595±.017;-.370±.032;1.020±.019;.562±.026;0;.010* | DER .628±.027;-.219±.070;.913±.029;.622±.029;0;.011* | DER++ .638±.036;-.208±.056;.932±.034;.633±.043;0;.011* | FDR .666±.012;-.146±.046;.917±.035;.627±.015;0;.010*
PNN .770±.012;0±0;.976±.021;.620±.020;1.056;0 | DAN .729±.009;0±0;.897±.022;.543±.127;.111;0 | PLOP .708±.025;-.104±.026;.986±.038;.707±.009;0;0 | MiB .751±.008;-.039±.003;1.004±.018;.697±.008;0;0 | Non-CL .471±.012;-.598±.015;1.014±.028;.572±.023;0;0 | JointTrain .810±.023;/;/;/;0;0
B-EXP-003 Organ-CL (B-TAB-005):
EWC .601±.008;-.371±.014;1.004±.012;0;0 | SI .621±.024;-.343±.025;1.003±.009;0;0 | LwF .594±.018;-.308±.044;.916±.004;0;0 | ER .729±.009;-.178±.021;.996±.011;0;.012* | GSS .717±.005;-.276±.055;.995±.009;0;.023* | GEM .599±.007;-.182±.068;.806±.059;0;.023* | GPM .605±.009;-.329±.034;.960±.027;0;.068 | AGEM .635±.013;-.193±.069;.873±.052;0;.023* | DER .717±.005;-.157±.022;.953±.013;0;.012* | FDR .631±.008;-.217±.008;.885±.013;0;.023* | PNN .839±.004;0;1.001±.006;1.074;0 | DAN .824±.005;0;.972±.016;.166;0 | Non-CL .603±.008;-.369±.005;1.006±.008;0;0 | JointTrain .881±.010;/;/;0;0
```

### 7.2 图像账本

|ID|路径/label/视觉核验|可支持观察|不支持/处置|
|---|---|---|---|
|B-FIG-001|`img/benchmark_overview_new.pdf`; `fig:benchmark_overview`; main 232--237；已视觉核验。|三场景、顺序协议、三类方法和 A-Dice/BWTR/WCD/RMA/E-FWT/MPE/DRR 的关系。|可重绘中文概览；不把图内“key findings”当超出表格范围的证据。|
|B-FIG-002|`task_robustness_adice.pdf` + `task_robustness_bwt_from_bottom.pdf`; `fig:task_order_robustness`; 875--896；已视觉核验前者。|十种顺序下 A-Dice、BWTR 有变化；Repl-GSS 图示标准差最低。|未给十种任务排列与原始数值，不能逐项复算。|
|B-FIG-003|`domain_memory_size_adice.pdf`; `fig:memory_a`; 900--925；已视觉核验。|ER/FDR/GEM/DER/GSS 的 A-Dice 随 buffer 增大总体提高且趋于饱和。|图中不是完整数值表，不报告精确差异或显著性。|
|B-FIG-004|`SAM_confusion_matrix.pdf`; `fig:memory_b`; 910--918。|只可描述其为顺序 SAM/LoRA 的任务—任务 Dice 矩阵。|没有正文方法、设置、数值或分析，不能作为第三章主要发现。|
|B-FIG-005|`plots_for_benchmark.pdf`; `fig:figure_machine_learning`; 956--961。|概念性关系图。|非实证结果，建议附录或不使用。|

## 8. 可写的逐场景分析与跨场景发现

- `B-CLAIM-001`：三种变化的标签与分布条件不同，故不能只用遗忘或单一总分替代完整协议。来源 `tab:CL_settings`、metrics 513--578；高置信；不称穷尽。
- `B-CLAIM-002`：Domain-CL 的 E-FWT 是所有未来域相对随机初始化的平均，不能与 Class/Organ 直接对比。来源 542--549；高置信。
- `B-CLAIM-003`：RMA 衡量当前新任务与独立训练参考的相对表现，接近 1 不等价于所有历史任务表现好。来源 533--540；高置信。
- `B-CLAIM-004`：在 Domain-CL 表内，PNN/DAN 的 BWTR 为 0，而 MPE 分别 1.112/.111，显示零遗忘与参数增长的同时存在。来源 B-EXP-001；高置信；仅该设置。
- `B-CLAIM-005`：在 Class-CL 表内，PLOP/MiB 的 WCD 为 .707/.697，且 BWTR 为 -.104/-.039；这是处理背景语义变化的两种专项参照，不证明所有类别增量分割都如此。来源 B-EXP-002；高置信。
- `B-CLAIM-006`：在 Organ-CL 表内，PNN/DAN 的 A-Dice .839/.824、BWTR 0，且 MPE 1.074/.166；与 JointTrain .881 的不同访问条件必须并列说明。来源 B-EXP-003；高置信。
- `B-CLAIM-007`：主论文规定共同 backbone 与基础训练设置，补充材料给回放 buffer 32；这构成可报告的统一协议，但不包含种子、硬件、代码版本。来源 supplement 14--40；高置信。
- `B-CLAIM-008`：表内结果支持“最终平均性能、稳定性、可塑性和资源指标可能给出不同排序”，而非“某方法全面最优”。来源 B-EXP-001--003；作者综合分析，审慎措辞。
- `B-CLAIM-009`：Domain-CL 中多数 E-FWT 未超过 Non-CL .260，DAN .312±.210 是表内例外且方差大；可写“该设置下前向泛化仍非一致改善”，不能写“所有方法均失败”。来源 B-EXP-001；高置信。
- `B-CLAIM-010`：十个顺序的图与文中 Repl-GSS A-Dice/BWTR 标准差 .0134/.0123 支持任务顺序敏感性；不支持其它未列方法的精确比较。来源 845--895；中高置信。
- `B-CLAIM-011`：缓存图支持总体随 buffer 增加而提升并有饱和趋势；不支持因果性或固定最优容量。来源 921--925、B-FIG-003；中高置信。

## 9. 局限、冲突与 TODO 清单

|优先级|ID|问题与处理|
|---|---|---|
|BLOCKER|B-LIM-001|无任何指标实现代码或实验脚本，RMA/E-FWT 等不能完成公式—代码一致性核验；正文必须说“公式—表格已核对，代码不可得”，不得称已复现。|
|BLOCKER|B-LIM-002|无主论文可编译 PDF：本机临时副本受缺失 `makecell.sty`/Palatino metric 阻塞。不得报告 PDF 页数或“编译通过”。|
|HIGH|B-LIM-003|所有数据集样本量、按中心样本数、固定随机种子、硬件、早停、运行次数、代码版本均未报告。数字可引表，复现实验设置不可写全。|
|HIGH|B-LIM-004|Class-CL 背景、旧类标签访问、task identity 供给与测试路由未形式化；仅能报告原稿明确的八通道头和 background-shift 解释。|
|HIGH|B-LIM-005|三张主表含均值±标准差但未写明种子/重复数和统计检验；不写显著性。|
|MEDIUM|B-LIM-006|`fig:memory_b` 涉及 SAM/LoRA，但无完整设置和数值表；不作为主章节结论。|
|MEDIUM|B-LIM-007|源目录存在注释图和未引用 PDF，不能当作现行结果；只列为材料存在。|
|LOW|B-LIM-008|主稿中 `Regu-LWF`/`Regu-LwF` 大小写不一致；博士章节统一为 `Regu-LwF`，不改变事实。|

## 10. 最小文献集合（后续集成再逐项迁移）

|key|原论文/本章用途|库状态|
|---|---|---|
|Benchmark work itself|本章来源工作；源稿没有正式出版信息或 DOI 的明确声明。|`TODO-EVIDENCE`：不得虚构出版信息。|
|`method_replay_gem`|BWT/FWT 背景及 E-FWT 对照。|需核查 `bibliography/references.bib` 后再迁移。|
|`method_regu_ewc`、`method_regu_si`、`method_regu_lwf`|正则化代表。|同上。|
|`method_replay_er`、`method_replay_gss`、`method_replay_agem`、`method_regu_gpm`、`method_replay_der`、`method_replay_xder`、`method_replay_fdr`|回放代表。|同上。|
|`method_dyn_pnn`、`method_dyn_dan`、`method_seg_mib`、`method_seg_plop`|参数隔离与 Class-CL 专项。|同上。|
|`dataset_prostate2`、`dataset_prostate`、`dataset_prostate3`、`dataset_domaincl`、`dataset_lascars`、`dataset_lascars2`、`dataset_taskcl`、`dataset_taskcl2`|数据来源。|同上；MMWHS 对应 key 需从主稿完整 bibliography 再核验。|
|`lifelong_unet`、`whatwrong`、`clseg_survey`、`medcl_survey`、`general_survey`|相关工作边界。|同上。|

## 11. GPT Pro 一次性整章写作清单

- 目标篇幅：3.1 800--1,000 字；3.2 900--1,100；3.3 1,800--2,200；3.4 1,400--1,700；3.5 1,500--1,800；3.6 2,400--3,000；3.7 1,000--1,300；3.8 400--600；总计约 10,200--12,700 中文字，约 22--28 个论文版面，最终以学校模板为准。
- 必须用公式：B-EQ-001--008；B-EQ-005 仅放 Domain-CL；不要自行补 Dice 原始定义，除非第二章交叉引用可用。
- 必须用表：B-TAB-002--005；B-TAB-001 只作简化相关工作对比。图优先 B-FIG-001--003；B-FIG-004、005 仅受限使用。
- 3.1--3.8 必须按第 3 节提纲组织，每个主要结论绑定 `B-CLAIM`/`B-EXP`；使用“在该基准设置下”“表中显示”“可观察到”等审慎措辞。
- 与第一章衔接：第一章提出场景与评价不完备；与第二章衔接：复用连续任务、稳定—可塑性和指标语言；与第四、五章衔接：提供对任务访问和评价维度的参照，而不预设其结果。
- **写作前阻塞项：**B-LIM-001 与 B-LIM-002 必须在章节中透明披露；B-LIM-003--005 限制复现性与统计结论。若作者要求“公式—代码已核验”或完整样本/种子/硬件表，必须先补充原始代码或日志。
