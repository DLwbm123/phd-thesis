# GPT Pro 复审上下文包：第二章整章（2026-08-01）

## 当前任务与批准边界

- 第二章已完整集成，整体状态为 `drafted_pending_review`；本包只支持作者/GPT Pro 整章复审，不生成新正文。
- 2.1.1“医学图像分割”和 2.1.2“医学图像配准”均为 `drafted_and_verified`，本轮未修改；2.1.3 至 2.4 是本轮新增且待复审的正文。
- 第二章结构为：2.1 三类医学图像任务；2.2 训练信息受限条件；2.3 持续学习定义、遗忘与方法路线；2.4 总结。2.2 首段已明确“数据不全”只是训练信息受限的概括。

## 新增且应复核的内容

- 12 个公式标签：`eq:foundations-cls-probability`、`eq:foundations-cls-loss`、`eq:foundations-cls-metrics`、`eq:foundations-replay-objective`、`eq:foundations-fed-learning`、`eq:foundations-partial-ce`、`eq:foundations-cl-update`、`eq:foundations-gradient-interference`、`eq:foundations-ewc`、`eq:foundations-gradient-projection`、`eq:foundations-maml`、`eq:foundations-sam`。
- 两张表：`tab:foundations-information-access` 与 `tab:foundations-cl-method-families`。
- 复用既有引用，并新增 Goodfellow、Fawcett、Brodersen、Geiping、Bonawitz、Abadi、Finn、Foret 八项文献。

## 复审重点

- 分类中多分类/多标签的概率、损失、阈值、指标汇总与患者级划分边界。
- 无回放、有限回放、原始数据不可集中和部分监督不可混写；未标注位置不等于背景；普通 FedAvg 不等于形式化隐私保证。
- MAML、SAM 与梯度子空间只作为通用基础，不泄露第四、第五章方法或性能；MAML/SAM 不自动保证抗遗忘。
- 不得重复第三章的场景细则、A-Dice、BWTR、RMA、E-FWT 或实验数字。

## 全文状态

- 第三章继续 `drafted_pending_review`，本轮未复审或修改；不得开始第四章。
- ScribbleCL 继续 `TODO-EXPERIMENT` / `blocked_by_experiments`。
- `TODO-EVIDENCE-REG-001/002`（TRE 与非正 Jacobian 统计）保持开放，未写入本轮正文。
