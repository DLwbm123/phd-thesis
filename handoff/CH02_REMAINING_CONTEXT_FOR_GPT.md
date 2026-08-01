# 第二章剩余内容整章证据上下文（仅供 GPT Pro 撰写；2026-08-01）

## 0. 使用边界与当前状态

- 本文件是**证据化写作蓝图**，不是可直接粘贴的博士论文正文；输出时应把条目重组为连贯中文论证，不能复制本文件的项目符号句式。
- 已批准且不得改写：`2.1.1 医学图像分割` 与 `2.1.2 医学图像配准`（均 `drafted_and_verified`）。它们的标签依次为 `subsec:foundations-segmentation`、`subsec:foundations-registration`；已有公式标签为 `eq:foundations-seg-*` 和 `eq:foundations-reg-*`。2.1.2 的结尾已明确过渡到“图像、检查或病例层面的分类”。
- 本次 GPT 输出须一次性覆盖 2.1.3、2.2（含引言与三小节）、2.3（含引言与三小节）及 2.4；它们目前均未写作。第三章为 `drafted_pending_review`，不得在本轮复审、修改或批准。
- 术语优先级：使用“**训练信息受限**”及其具体访问条件；“数据不全”只作概括，绝不指像素随机缺失或数据被物理删除。建议保留批准的 2.2 标题，以首段说明其严格含义；若后续作者要求标题与总题目完全一致，可改为“训练信息受限场景下的学习问题”，但这不是本轮自动修改建议。
- 禁止：重复第一章研究现状；复制第三章的 Domain/Class/Organ-CL 协议、A-Dice、BWTR、RMA、E-FWT、结果表或数字；介绍 FedSubMerge、ZScribbleSeg、ScribbleCL、SAMCL 的特有流程、超参或结论；把联邦聚合表述为形式化隐私保证；将有限回放写成无回放；虚构 ScribbleCL 实验。

## 1. 章节逻辑、映射与去重

逻辑链：**分割、配准、分类的预测对象和评价尺度** → **监督、历史样本及跨中心信息在训练阶段的可访问范围** → **顺序任务到达时的模型更新设定** → **遗忘与稳定性—可塑性及方法族** → **为第三至第五章给出统一而不抢先的基础**。

|拟写内容|第二章位置|已有内容/后文|第二章保留的基础层级|必须避免|
|---|---|---|---|---|
|图像/检查/病例分类|2.1.3|2.1.1/2.1.2 已定义像素域与变换；第4章为分类应用|输出空间、CE/BCE、指标和患者级评价边界|第4章的客户端子空间、结果或任务协议|
|访问条件|2.2|第1章已给动机；第4/5章给具体问题|谁在何阶段可访问何种信息|长篇现状综述或把各约束混成“缺数据”|
|持续学习定义|2.3.1--2.3.2|第3章已给分割基准|任务/测试上下文/历史访问为正交维度|第3章的三场景细则、公式和实验指标|
|方法路线|2.3.3|第4/5章将给特有设计|机制、信息、代价、适用条件、局限|FedSubMerge 融合规则；ZScribbleSeg 损失组合；SAMCL 联合目标|
|总结|2.4|连接第三至第五章|任务—访问—顺序学习的三层关系|新贡献、结果或实验承诺|

### 统一符号建议（仅候选，暂不登记）

现有 `\Omega,K,\theta,f_\theta,p_{\theta,k}` 已用于空间分割；`\mathcal T,t,\mathcal D_t,\theta_t` 已用于第三章。因此分类避免复用位置概率，建议采用：样本 `(\mathbf x_i,y_i)`，样本级 logit `\mathbf z_\theta(\mathbf x_i)`，概率 `q_{\theta,c}(\mathbf x_i)`，预测 `\hat y_i`。仍令 `K` 为类别数，但须在首次处声明与 2.1.1 一致；多标签用标签向量 `\mathbf y_i\in\{0,1\}^K`。

访问集合建议：`\mathcal D_t`（当前阶段数据，复用第三章）、`\mathcal H_t`（可重新访问的历史原始样本）、`\mathcal M_t`（有限保存记忆，须注明保存形式）、`\mathcal D_t^{(k)}`（第 `k` 个客户端本地数据）、`\Omega_L`（空间任务的已标注位置）。`\mathcal C` 留给类别集合，避免与 FedSubMerge 的客户端集合冲突；客户端集合使用 `\mathcal K_{\rm cli}`。正式集成前需登记并复核第4/5章预留记号。

## 2. 逐节写作提纲（非正文）

|部分|功能、论断顺序与段落建议|公式/表/证据锚点|过渡、边界与建议篇幅|
|---|---|---|---|
|2.1.3|3--4 段：分类粒度→二/多/多标签输出→损失→评价与患者级划分。|CH2R-EQ-001--004；无独立表。Litjens；FedSubMerge 246--265。|承接配准的“病例层输出”，结尾转入“训练时可访问什么”。不写联邦持续算法；900--1,200 字。|
|2.2 引言|1--2 段：按监督、历史访问、跨中心访问分开定义限制；指出三者可叠加。|CH2R-CLAIM-003；CH2R-TAB-001。|不把“数据不全”误作缺失值；350--500 字。|
|2.2.1|3 段：联合训练基线→有限/替代/无回放访问集→资源和概念边界。|CH2R-EQ-005；FedSubMerge 246--261、SAMCL 178--192。|转向跨中心时强调历史访问与数据位置是不同轴；800--1,000 字。|
|2.2.2|3--4 段：本地数据和全局目标→本地训练/聚合→异质性→隐私风险与附加机制。|CH2R-EQ-006--007；FedAvg；Geiping；Bonawitz；Abadi。|仅说明联邦持续学习在时间轴上再叠加任务序列；850--1,100 字。|
|2.2.3|3 段：监督粒度→`\Omega_L` 与 PCE→与半监督/伪标签/先验的边界。|CH2R-EQ-008；ScribbleSup；Can；ZScribble 293--305。|转入“即使当前数据可用，顺序更新仍会遗忘”；750--950 字。|
|2.3 引言|1 段：任务演化与访问条件的交叉，方法不由单一场景决定。|CH2R-CLAIM-011；无表。|不得复述第三章实验协议；250--350 字。|
|2.3.1|3--4 段：序列/更新/测试→TI/DI/CI 与单/多头→task-aware/task-free→集中/联邦及访问条件正交性。|CH2R-EQ-009；Hadsell；van de Ven；De Lange。|只用抽象定义与例子；900--1,100 字。|
|2.3.2|3 段：遗忘定义→一阶梯度干扰→稳定性/可塑性及正负迁移。|CH2R-EQ-010；CH2R-CLAIM-014--016。|不可写第三章的四个指标公式；700--900 字。|
|2.3.3|5--6 段：按机制比较正则/蒸馏、回放、隔离、投影；最后极简介绍低秩子空间、元学习、SAM。|CH2R-EQ-011--016；CH2R-TAB-002。|所有特有算法留在第4/5章；1,400--1,800 字。|
|2.4|1--2 段：重申任务、访问、顺序更新三层；指向第3--5章。|无新公式/表。|不声称方法性能；300--450 字。|

建议总量约 7,300--9,300 中文字（约 11--15 个排版页，取决于公式与两张表），以证据密度为准而非机械扩写。

## 3. 2.1.3 分类：定义、公式与评价候选

### 3.1 任务与预测边界

- 图像级：一张二维图像或三维体为单位；检查级：多视图/序列经聚合后输出；病例级：多个检查或时间点经明确规则汇集。必须说明训练、验证和测试按患者（而不是切片/图像）划分，以避免同一患者泄漏至不同集合。
- 二分类：一个风险/类别概率；互斥多分类：每例一个类别，概率和为 1；多标签：多个标签可同时为真，每一标签独立 sigmoid，概率不要求和为 1。不要把多标签 BCE 用于互斥多分类而不解释。
- 分类基础可借用 FedSubMerge 的“医学图像—诊断标签”样本对，但其测试任务身份、任务特定头、通信轮和投影均属第4章边界（本地原稿 246--285）。

|ID / 精确 LaTex|符号、范围、方向与边界|原始来源 / 是否建议正文|
|---|---|---|
|CH2R-EQ-001 `q_{\theta,c}(\mathbf x)=\frac{\exp z_{\theta,c}(\mathbf x)}{\sum_{j=1}^{K}\exp z_{\theta,j}(\mathbf x)},\quad \hat y=\arg\max_c q_{\theta,c}(\mathbf x).`|互斥 K 类；`\mathbf z` 为 logits；概率和为1。|分类标准定义；使用 `litjens2017survey` 作医学任务锚点，正式引入前补一条可核验的原始/教材级概率模型来源。建议正文。|
|CH2R-EQ-002 `q_{\theta,c}(\mathbf x)=\sigma(z_{\theta,c}(\mathbf x)),\quad \hat y_c=\mathbbm{1}[q_{\theta,c}(\mathbf x)\ge \tau_c].`|多标签；阈值可按类设定，不能默认 `0.5` 最优。|同上；建议正文，需在文献核验时补足原始概率模型锚点。|
|CH2R-EQ-003 `\mathcal L_{\rm CE}=-\frac1n\sum_{i=1}^n\sum_{c=1}^K y_{i,c}\log q_{\theta,c}(\mathbf x_i).`|互斥多类，`y` 独热；小概率要数值稳定实现。|标准最大似然定义；建议正文，但列为 MEDIUM 的原始来源补核项。|
|CH2R-EQ-004 `\mathcal L_{\rm BCE}=-\frac1{nK}\sum_{i=1}^n\sum_{c=1}^K[y_{i,c}\log q_{\theta,c}(\mathbf x_i)+(1-y_{i,c})\log(1-q_{\theta,c}(\mathbf x_i))].`|多标签或独立二类；类别权重不是默认组成部分。|标准最大似然定义；建议正文，须与多标签语义绑定。|

混淆矩阵中，二分类的 `TP,TN,FP,FN` 必须按阳性类和阈值确定。候选指标：`Acc=(TP+TN)/(TP+TN+FP+FN)`；`BAcc=(TPR+TNR)/2`；`Sensitivity=TP/(TP+FN)`；`Specificity=TN/(TN+FP)`；`Precision=TP/(TP+FP)`；`Recall=Sensitivity`；`F1=2TP/(2TP+FP+FN)`；AUROC 是阈值遍历下 TPR--FPR 曲线面积。前七项阈值依赖；AUROC 衡量排序、仍不说明某一临床阈值下的校准或实用性。空分母、阳性/阴性缺失、宏/微/加权平均必须在实现中明示。类别不平衡时不能仅报告 Accuracy，建议至少配合 BAcc、敏感度/特异度或 F1；多标签应逐标签报告汇总方式。**本章不必把八个指标都排成八个公式**：推荐在叙述中定义混淆矩阵并用一个紧凑指标式组，余者文字说明；具体第4章指标由原始实验协议决定。

## 4. 2.2 训练信息受限：统一访问模型

令当前阶段可训练数据为 `\mathcal D_t`；`\mathcal H_t` 指可重新访问的历史原始样本；`\mathcal M_t` 指有限记忆（必须标明是样本、特征、logit、原型或生成模型）；`\mathcal D_t^{(k)}` 指客户端 `k` 的本地数据；`\Omega_L` 指空间标注位置。它们分别描述**时间可访问性、保存表示、空间位置与组织位置**，不可相互替代。

### 4.1 2.2.1 历史不可访问与无回放

- 完整联合训练可访问 `\bigcup_{\tau\le t}\mathcal D_\tau`；有限原始回放只可访问当前数据和容量受限的 `\mathcal M_{t-1}\subset\mathcal H_t`；替代回放可保存压缩表示/生成器/原型；无历史原始样本回放设定为 `\mathcal H_t=\varnothing`（就原始样本而言），但不禁止保存参数、统计量或受限摘要。
- “当前不能访问”是训练阶段的访问约束，不推出历史数据已经删除；回放也不自动恢复完整历史分布，且记忆选择和预算会形成偏差。FedSubMerge 明示只有当前任务数据可用、早期图像不能访问或回放（246--261）；SAMCL 的 `\mathcal M` 是有限经验回放（178--192），两者不得混写。
- CH2R-EQ-005：`\min_\theta\;\mathbb E_{(\mathbf x,y)\sim\mathcal D_t}[\ell_\theta(\mathbf x,y)]+\lambda\,\mathbb E_{(\mathbf x,y)\sim\mathcal M_{t-1}}[\ell_\theta(\mathbf x,y)]`。适用于有显式记忆的抽象回放；`\mathcal M_{t-1}=\varnothing` 时第二项不应伪装成可估计的旧数据损失。来源：Rolnick et al. 2019 (`method_replay_er`)；建议正文。

### 4.2 2.2.2 多中心分布式数据与隐私约束

- 客户端在本地持有 `\mathcal D_t^{(k)}` 并训练；服务器聚合模型更新。数据量、标签、成像设备/人群域、任务到达时间与参与客户端可异质。静态联邦只讨论给定数据分布的协作；联邦持续学习再增加任务序列和历史访问约束。
- CH2R-EQ-006（抽象联邦目标）：`\min_\theta\;\sum_{k\in\mathcal K_{\rm cli}}\frac{n_k}{\sum_j n_j}\,\mathbb E_{(\mathbf x,y)\sim\mathcal D^{(k)}}[\ell(f_\theta(\mathbf x),y)]`。CH2R-EQ-007（FedAvg）：`\theta^{(r+1)}=\sum_{k\in\mathcal S_r}\frac{n_k}{\sum_{j\in\mathcal S_r}n_j}\theta_k^{(r+1)}`。适用参与集合 `\mathcal S_r`；须说明权重/参与规则。来源：McMahan et al. 2017；建议正文。
- 原始数据不集中仅限制原始样本共享，不等价于形式化隐私。参数或梯度可能泄露训练样本（Geiping et al. 2020）。安全聚合隐藏单个客户端更新的聚合过程；差分隐私提供依赖机制与预算的可量化保护；二者并非 FedAvg 的自然结论。仅作一段边界说明，不给出部署承诺。

### 4.3 2.2.3 部分监督与稀疏标注

- 监督粒度可从图像级标签、点、框、涂鸦、部分切片到稠密掩膜排列；弱监督描述标注形式较弱，半监督通常另有无标签样本，部分监督强调已标注位置/区域不覆盖完整目标。未标注位置没有自动背景语义。
- CH2R-EQ-008：`\mathcal L_{\rm PCE}(\theta)=-\frac1{|\Omega_L|}\sum_{\mathbf u\in\Omega_L}\sum_{c=0}^{K-1}Y_c(\mathbf u)\log p_{\theta,c}(\mathbf u)`。适用于有离散空间标注集合，且 `|\Omega_L|>0`；与 2.1.1 的全域 CE 仅在求和域上不同。来源：Lin et al. 2016；Can et al. 2018；本地 ZScribble 原稿 293--305；建议正文。
- 标签传播、伪标签、一致性与结构/形状先验只能作为“补足监督缺口的类别”简述，不能写出 ZScribbleSeg 的混合比例、空间先验、损失组合或结果。

## 5. 2.3 持续学习：定义、张力与方法机制

### 5.1 2.3.1 问题定义与基本场景

- CH2R-EQ-009：`\theta_t=\operatorname*{Update}(\theta_{t-1},\mathcal A_t),\quad \mathcal A_t\subseteq\{\mathcal D_t,\mathcal H_t,\mathcal M_{t-1},\text{task identity},\text{client messages}\}`。这是访问依赖的抽象模型而非实验协议；来源：De Lange et al. 2022、van de Ven et al. 2022；建议正文。
- 任务增量（TI）通常在测试可用任务身份并可选任务头；域增量（DI）保持预测语义、输入域改变；类增量（CI）逐步扩展可识别类且通常不提供任务身份。单头/多头、task-aware/task-free 是测试条件；历史访问是另一独立维度。不要声称现实任务必然边界已知。
- 第三章的三种医学分割基准可作为“具体实例在第三章给出”的前瞻性一句，不重述定义、序列、表格、指标或结论。集中式与联邦持续学习共享顺序更新问题，后者额外受客户端与通信约束。

### 5.2 2.3.2 遗忘与稳定性—可塑性

- 灾难性遗忘指在后续更新后旧任务性能下降或损失上升；前向泛化和正/负向迁移描述先前学习对新任务的影响。报告任何数值时必须在后文按相应协议与指标定义。
- CH2R-EQ-010：`\ell_{t-1}(\theta_t)\approx\ell_{t-1}(\theta_{t-1})+\nabla_\theta\ell_{t-1}(\theta_{t-1})^\top(\theta_t-\theta_{t-1})`。这是一阶局部解释：新更新与旧任务梯度同向可能降低旧损失、反向可能加剧干扰；非凸远距离更新不能据此作保证。来源：GEM (Lopez-Paz & Ranzato 2017) 的梯度约束动机；建议正文。
- 稳定性是保持既有能力，过强则限制当前学习；可塑性是适应新数据，过强则可能损害旧能力。不得将二者说成可由单一固定超参完全解决。

### 5.3 2.3.3 方法路线与通用优化工具

|机制|保留的信息；如何更新|资源/适用条件/主要局限|原始锚点及后文边界|
|---|---|---|---|
|参数正则化|旧参数重要性；惩罚偏离|不需原图；重要性近似可能失效|EWC；不可推出第4章子空间方案|
|函数正则/蒸馏|旧模型 logits/输出；保持函数响应|需教师与可用输入；输出空间变化困难|LwF；不写方法章蒸馏设计|
|回放/替代回放|样本、特征、logit、原型或生成表示；联合训练|存储/生成偏差、隐私与合规条件|ER、GEM/AGEM、DER；SAMCL 的有限缓冲细节禁止|
|隔离/动态结构|任务专属参数或路由；冻结/扩展|参数增长、任务身份或容量需求|PNN；不宣称单头适用|
|梯度约束/投影|记忆梯度或保护子空间；约束/投影当前梯度|需估计历史方向，可能压缩可塑性|GEM、A-GEM、GPM；不写 FedSubMerge 的客户端融合|
|元学习与 SAM|跨任务初始化/更新规则；邻域最坏损失|双层计算/额外梯度；并不等同持续学习保证|MAML、SAM；只定义基本目标，不写 SAMCL|

候选最小公式（每个进入正文前保持一式一用途，避免堆砌）：

|ID / 精确 LaTex|范围、来源与建议|
|---|---|
|CH2R-EQ-011 `\mathcal L_t^{\rm EWC}(\theta)=\mathcal L_t(\theta)+\frac{\lambda}{2}\sum_i F_i(\theta_i-\theta_{t-1,i}^*)^2`|`F_i` 为旧参数重要性近似；EWC，Kirkpatrick et al. 2017；建议正文。|
|CH2R-EQ-012 `\mathcal L_t^{\rm LwF}=\mathcal L_t^{\rm sup}+\lambda\,\mathcal L_{\rm distill}(f_\theta(\mathbf x),f_{\theta_{t-1}}(\mathbf x))`|抽象蒸馏，温度/具体 KL 留在来源或方法章；Li & Hoiem 2018；建议正文。|
|CH2R-EQ-013 `\tilde g=\arg\min_v\frac12\lVert v-g\rVert_2^2\;\mathrm{s.t.}\;v^\top g_m\ge0,\;m<t`|GEM 型约束，需记忆梯度；Lopez-Paz & Ranzato 2017；建议正文。|
|CH2R-EQ-014 `\tilde g=g-\mathbf U\mathbf U^\top g`|`\mathbf U` 的列正交且表示待保护方向；GPM / 本地 FedSubMerge 503--523；建议正文，但不得引入服务器/客户端合并。|
|CH2R-EQ-015 `\theta'=\theta-\alpha\nabla_\theta\mathcal L_{\rm in}(\theta),\quad \min_\theta\mathcal L_{\rm out}(\theta')`|一阶 MAML 说明；Finn et al. 2017；建议简述，可不排公式以控制篇幅。|
|CH2R-EQ-016 `\min_\theta\max_{\lVert\epsilon\rVert_2\le\rho}\mathcal L(\theta+\epsilon)`|SAM 的邻域最坏损失；Foret et al. 2021；建议简述，可不推导 `\epsilon`。|

推荐正式正文最多保留 EWC、抽象回放、一个梯度约束/投影以及 MAML/SAM 中的一式或纯文字定义；余下为表中比较。这样给第4/5章留下方法特异性空间。

## 6. 候选表格（至多两张；不建议概念图）

1. **CH2R-TAB-001 训练信息访问条件比较表**：列为“条件、当前/历史原始数据、可保存信息、原始数据是否集中、监督覆盖、典型风险、与后文关系”；行用完整联合、有限回放、无回放、跨中心分布式、部分监督。信息源为 FedSubMerge、SAMCL、ZScribble 与本节原始文献。建议进入正文，使用 `\begin{table}[htbp]\centering\small\begin{tabular}{p{...}...}`，不列算法性能；不会与第3章指标表重复。
2. **CH2R-TAB-002 持续学习方法路线比较表**：列为“机制、保留的历史信息、更新约束/扩展、资源代价、适用条件、主要局限、代表方法”；行用 2.3.3 六类。建议进入正文；不含第4/5章方法细节或结果。
3. 不建议新增概念图：访问条件和方法路线以两张比较表已足够，额外流程图易误把后续方法章机制提前视觉化。

## 7. 临时证据候选与最小文献集合

### 7.1 论断与限制候选

|ID|拟支持内容；定位/来源；置信度；禁止外推；正式建议|
|---|---|
|CH2R-CLAIM-001|分类输出可位于图像、检查或病例尺度；`litjens2017survey`；高；不等同空间分割；C2-021。|
|CH2R-CLAIM-002|患者级划分避免同一患者跨集合；需在具体数据协议中落实；中；不能据此声称所有既有实验已无泄漏；C2-022。|
|CH2R-CLAIM-003|训练信息受限包括监督、历史和跨中心访问限制；`THESIS_CONTRACT.md` 28--34；高；不等同物理删除；C2-023。|
|CH2R-CLAIM-004|FedSubMerge 只访问当前本地任务数据，历史图像不可回放；本地原稿 246--261；高；不是一般联邦学习必然事实；C2-024。|
|CH2R-CLAIM-005|有限回放与无回放是不同访问条件；SAMCL 178--192、FedSubMerge 246--261；高；不能把二者统一命名；C2-025。|
|CH2R-CLAIM-006|联邦原始数据不集中不构成形式化隐私保证；FedSubMerge 1243--1248；高；不得声称其天然安全；C2-026。|
|CH2R-CLAIM-007|梯度可泄露训练样本；Geiping 2020；高；不推出任意更新必然重建；C2-027。|
|CH2R-CLAIM-008|涂鸦仅覆盖部分位置，PCE 只在标注像素计算；ZScribble 293--305；高；未标注像素不是背景；C2-028。|
|CH2R-CLAIM-009|场景类型与历史访问条件正交；De Lange/van de Ven；中；现实协议仍须具体定义；C2-029。|
|CH2R-CLAIM-010|任务身份可在 TI 测试选择任务头；FedSubMerge 263--265；高；不能推广到 task-free；C2-030。|
|CH2R-CLAIM-011|持续学习目标是在顺序更新下兼顾当前适应与既有能力；Hadsell 2020；高；非性能结论；C2-031。|
|CH2R-CLAIM-012|稳定性和可塑性存在张力；Hadsell 2020；高；不是固定二分法；C2-032。|
|CH2R-CLAIM-013|正则化、回放、隔离和投影依赖不同历史信息；EWC/LwF/GEM/PNN/GPM；高；不比较本论文结果；C2-033。|
|CH2R-CLAIM-014|元学习是跨任务快速适应的优化框架；Finn 2017；高；不等于任意 CL 方法；C2-034。|
|CH2R-CLAIM-015|SAM 追求邻域内低损失参数；Foret 2021；高；不提前宣称配准收益；C2-035。|
|CH2R-CLAIM-016|ScribbleCL 仍 `TODO-EXPERIMENT`；`STATE.md`；高；不得生成结论；LIM-C2R-012。|

|限制 ID|内容与级别|
|---|---|
|CH2R-LIM-001|**HIGH**：分类 CE/BCE 与八个分类指标的“原始”数学出处尚须在正式集成前补可核验的权威原始/标准来源；现有医学综述不足以单独充当公式起源。|
|CH2R-LIM-002|**HIGH**：多标签任务的阈值、宏/微平均和临床效用不可从 FedSubMerge 互斥分类实验外推。|
|CH2R-LIM-003|**HIGH**：安全聚合/差分隐私的机制与隐私预算只能在引入其正式条件后表述，不能作为 FedAvg 属性。|
|CH2R-LIM-004|**MEDIUM**：`\mathcal H_t,\mathcal M_t,\Omega_L` 尚未登记，需要整章写定后一次性写入 notation。|
|CH2R-LIM-005|**MEDIUM**：2.2 标题与“训练信息受限”术语存在表层不一致；建议首段定义，是否改题由作者决定。|
|CH2R-LIM-006|**MEDIUM**：第三章已有任务符号和评价公式；2.3 只能使用抽象记号。|
|CH2R-LIM-007|**MEDIUM**：EWC/LwF/GEM/GPM 的正文公式必须与所用实现/定义保持一致，不能混接不同变体。|
|CH2R-LIM-008|**LOW**：2.1.2 的 `TODO-EVIDENCE-REG-001/002`（TRE/Jacobian）与本轮无关，保持开放且不得借本轮关闭。|
|CH2R-LIM-009|**LOW**：表格若过宽，优先压缩措辞而非缩小至不可读。|
|CH2R-LIM-010|**LOW**：MAML/SAM 只讲通用目标；其具体近似和 SAMCL 训练细节留第5章。|
|CH2R-LIM-011|**LOW**：ZScribbleSeg 仅可作部分监督事实锚点，不可追溯改写为持续学习。|
|CH2R-LIM-012|**BLOCKER**：无；上述 HIGH 项可通过保守表述或正式集成前补证据解决，不阻止 GPT 输出带明确 TODO 的整章草稿。|

### 7.2 最小充分引用集合

|citation key|完整元数据与官方来源|支持位置|库内状态/冲突|
|---|---|---|---|
|`litjens2017survey`|Litjens et al., *A survey on deep learning in medical image analysis*, MedIA 2017, DOI [10.1016/j.media.2017.07.005](https://doi.org/10.1016/j.media.2017.07.005)|2.1.3 医学任务锚点|已存在；不作 CE 起源。|
|`mcmahan2017fedavg`|McMahan et al., *Communication-Efficient Learning of Deep Networks from Decentralized Data*, AISTATS 2017, [PMLR](https://proceedings.mlr.press/v54/mcmahan17a.html)|2.2.2 FedAvg|已存在。|
|`sheller2020federated`|Sheller et al., *Federated learning in medicine*, ACM TIST 2020, DOI 10.1145/3349825|2.2.2 医学协作背景|已存在；背景而非 FedAvg 起源。|
|`geiping2020inverting`|Geiping et al., *Inverting Gradients—How easy is it to break privacy in federated learning?*, NeurIPS 2020, [official](https://papers.neurips.cc/paper_files/paper/2020/hash/c4ede56bbd98819ae6112b20ac6bf145-Abstract.html)|2.2.2 泄露边界|需核查库内 key/元数据。|
|`bonawitz2017practical`|Bonawitz et al., *Practical Secure Aggregation for Privacy-Preserving Machine Learning*, CCS 2017, DOI [10.1145/3133956.3133982](https://doi.org/10.1145/3133956.3133982)|2.2.2 安全聚合|需新增前核验。|
|`abadi2016deep`|Abadi et al., *Deep Learning with Differential Privacy*, CCS 2016, DOI [10.1145/2976749.2978318](https://doi.org/10.1145/2976749.2978318)|2.2.2 DP 边界|需新增前核验。|
|`lin2016scribblesup`|Lin et al., *ScribbleSup*, CVPR 2016, [official](https://openaccess.thecvf.com/content_cvpr_2016/html/Lin_ScribbleSup_Scribble-Supervised_Convolutional_CVPR_2016_paper.html)|2.2.3|已存在。|
|`can2018scribble`|Can et al., *Scribble-based weakly supervised learning for brain tumor segmentation*, MIDL 2018, DOI 10.48550/arXiv.1803.07434|2.2.3 医学涂鸦|已存在；正式元数据再核。|
|`delange2022continual`, `vandeven2022three`, `hadsell2020embracing`|De Lange et al., *A continual learning survey*, TPAMI 2022; van de Ven et al., *Three types of continual learning*, Nature MI 2022; Hadsell et al., *Embracing change*, Trends CI 2020|2.3.1--2.3.2|均已存在。|
|`kirkpatrick2017ewc`, `li2018lwf`, `method_replay_er`, `method_replay_gem`, `method_replay_agem`, `method_dyn_pnn`, `saha2021gpm`|EWC PNAS 2017; LwF TPAMI 2018; ER NeurIPS 2019; GEM NeurIPS 2017; A-GEM ICLR 2019; PNN arXiv 2016; GPM ICLR 2021|2.3.3|均已存在或以现有 key 核查。|
|`finn2017maml`, `foret2021sam`|Finn et al., *Model-Agnostic Meta-Learning*, ICML 2017, [PMLR](https://proceedings.mlr.press/v70/finn17a.html); Foret et al., *Sharpness-Aware Minimization*, ICLR 2021, [official](https://mlanthology.org/iclr/2021/foret2021iclr-sharpnessaware/)|2.3.3|需要正式加入前核验。|
|本地 `FedSubMerge_main_no_appendix.tex`; `Paper-0150.tex`; `main_clean_new.tex`|本地原始工作，定位见本文件|访问条件和边界|只作事实锚点；不虚构正式出版信息。|

## 8. GPT Pro 一次性输出清单

1. 从现有 `\subsection{医学图像分类}` 起，输出所有剩余 LaTeX 正文；不改 2.1.1/2.1.2，不触及第3章。
2. 使用 CH2R-EQ-001--016 中真正必要的最小集合；分类指标可用一组紧凑公式，方法工具不要逐式推导。为每个采用的式子给可核验 citation key。
3. 最多采用 CH2R-TAB-001、CH2R-TAB-002 两张表；不给出图、实验数值、第三章指标和未证实临床结论。
4. 明确写出：无回放、有限回放、原始数据不集中、部分监督分别是什么；联邦数据不集中不等于隐私保证；SAMCL 是有限回放；ScribbleCL 仍为 `TODO-EXPERIMENT`。
5. 集成任务应同时更新实际使用的证据、术语、符号和状态账本，并完整编译、引用/标签检查、视觉检查；正式集成前先解决 CH2R-LIM-001--003 或将相关陈述降为严格限定的标准定义。
6. 预期交付为“一份覆盖 2.1.3--2.4 的完整 LaTeX 草稿 + 引用清单 + 账本变更建议”，而不是分节零散续写。当前没有 BLOCKER；但不得以本上下文替代原始来源核验。
