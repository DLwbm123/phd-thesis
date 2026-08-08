# GPT Pro 复审上下文包：第一、二章对齐后（2026-08-08）

## 当前审阅范围

- 本包对应 Mode B 里程碑：第一章与第二章已按批准稿完成结构、概念图、公式、术语和账本对齐；完整审查见 `handoff/MODE_B_CH01_CH02_ALIGNMENT_AUDIT.md`。
- 全文保持连续六章。第一章为 `drafted_and_verified`；第二章为 `drafted_pending_review`；第三、四章为 `drafted_pending_review`，本轮未改其正文。

## 第一章的固定主线

- 1.3 顺序必须保持：Benchmark（场景与评价）→ FedSubMerge（分布式无回放）→ ScribbleCL（部分监督持续分割）→ SAMCL（知识保持与跨任务泛化）。
- 图 1-1 分别说明任务组织、时间与历史访问、数据位置与协同优化，强调三者可组合；图 1-2 只表示论文组织关系，不表示算法链。
- Chapter 3 提供场景与评价基础；Chapter 4 研究无回放联邦持续分类；Chapter 5 的分割线为 ZScribbleSeg（静态弱监督基础）→ ScribbleCL（持续扩展），配准线为有限回放 SAMCL。

## 第二章的固定边界

- “训练信息受限”是严格术语；“数据不全”仅是第一章背景的直观概括，不指随机缺失值或物理删除。
- HD、HD95、ASSD 是不同的物理坐标边界指标；不得在第五章或其他结果中替换已有的 HD 名称。
- `Acc` 是单个分类任务的样本级总体准确率；`ACC` 是第四章阶段--任务性能矩阵计算的最终平均准确率。
- 图像空间维度为 $d\in\{2,3\}$；梯度维度为 $p=\dim(\mathbf{g})$，投影矩阵为 $\mathbf{I}_p$。
- 完整联合训练表示完整历史访问，可采用集中式或分布式组织，不等于跨机构集中原始数据。

## 不可越过的保护边界

- 不得修改 Chapter 5、`evidence/experiments.csv` 或任何 ScribbleCL 的任务协议、方法地位、基线、实验状态、数字、TODO 或结论。
- Chapter 1 的 Scribble 挑战子节、RQ3、创新点（3）和其 `TODO-EXPERIMENT` 经 SHA-256 与基线逐字一致。
- 继续区分静态 ZScribbleSeg、论文级 ScribbleCL 持续扩展与有限回放 SAMCL；不得将静态结果外推为 ScribbleCL 结果。

## 待作者/GPT Pro 复审

- 第一章：检查 1.1.4 与 1.2.1 的压缩是否保持“动机/文献缺口”角色，且不与第二章机制定义重复。
- 第二章：检查边界指标、Acc/ACC、训练信息访问条件和 $d/p$ 区分是否满足答辩时的严格表述。
- ScribbleCL 保持 `TODO-EXPERIMENT` / `blocked_by_experiments`；只有在协议、日志、性能矩阵、表格和证据账本齐备后才可补写任何实验结论。
