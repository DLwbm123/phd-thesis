# 第五章最新复审上下文包（2026-08-12）

## 本轮已确认的 ScribbleCL 方法边界

- 当前任务只使用部分交叉熵、全局一致性和空间先验；全局一致性与空间先验均引用 `zhang2026zscribbleseg`，不引入来源工作的其他损失。
- 正文不转录来源工作的原有实验结果。
- ZSDERpp 作为一个整体方法处理 Domain-CL、Class-CL 和 Organ-CL。其缓冲区损失固定为：
  `0.5 L_feature + 0.5 L_PCE^buffer + 1.0 L_global^buffer + 0.1 L_spatial^buffer`。
- Domain-CL 使用共享输出头；Organ-CL 通过任务标识选择输出头；Class-CL 在同一方法内部进行背景概率聚合和旧模型一致性约束，不另行命名第二种方法。
- 缓冲区保存容量受限的历史图像--涂鸦对、参考特征和任务标识。该访问条件不同于无回放方法，也不同于只使用当前阶段密集标签的顺序训练。

## Domain-CL 最新结果

| 方法 | A-Dice | BWTR | RMA | E-FWT |
|---|---:|---:|---:|---:|
| Dense-Sequential | 0.676 | -0.237 | 1.086 | 0.260 |
| PCE-Sequential | 0.248 | -0.545 | 0.776 | 0.133 |
| ZS-Sequential | 0.510 | -0.324 | 0.732 | 0.234 |
| ZS-EWC | 0.543 | -0.298 | 0.761 | 0.216 |
| ZS-GPM | 0.612 | -0.206 | 0.808 | 0.241 |
| ZSDERpp | 0.701 | -0.152 | 0.899 | 0.225 |

- ZSDERpp 的 A-Dice 和 BWTR 为表中最高值。
- Dense-Sequential 的 RMA 和 E-FWT 为表中最高值。
- 与 ZS-GPM 相比，ZSDERpp 的 A-Dice、BWTR、RMA 分别提高 0.089、0.054、0.091，E-FWT 降低 0.016。
- 与 Dense-Sequential 相比，ZSDERpp 的 A-Dice 和 BWTR分别高 0.025 和 0.085，RMA 和 E-FWT 分别低 0.187 和 0.035。
- 由于历史访问条件不同，上述差值不能解释为稀疏监督直接优于密集监督。
- 当前表格未提供随机种子重复数、标准差或统计检验，只能分析点估计。
- Class-CL 与 Organ-CL 目前只写方法适配，不给出结果结论。

## SAMCL 边界

- SAMCL 继续保持有限原始图像对回放、元持续学习和锐度感知优化的原始定位。
- Dice 与 TRE 的 BWT 方向必须分开解释；SAMCL 不在所有任务上统一优于 MER。
- ScribbleCL 与 SAMCL 不共享同一算法，只在任务演化、历史访问和评价维度上进行比较。
