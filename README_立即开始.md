# 博士论文 GPT Pro × Codex Sol High 受控写作启动包（V3）

本版本依据 2026-07-31 导师讨论后的论文框架更新。框架迁移已完成；后续写作须以作者复审后的题目与术语边界为准。

## 作者复审后的工作题目

中文：**面向任务持续演化与训练信息受限的医学影像持续学习研究**
英文：**Continual Learning for Medical Image Analysis under Evolving Tasks and Limited Training Information**

“训练信息受限”是正文的严格技术术语，指特定训练阶段不能完整调用潜在可用的监督、历史或跨中心原始信息；“数据不全”仅可作为研究背景的概括性说法，不指随机缺失值或物理删除。

## 一、当前论文主线

```text
数据无法全部访问
  ├─ 部分监督 / 标注不完整
  ├─ 历史数据不可全部访问或不可回放
  └─ 多中心原始数据不可集中
                +
中心、设备、器官、类别和模态持续演化
                ↓
以持续学习为主线：场景与评价 → 联邦无回放方法 → 弱监督分割与配准持续学习
```

## 二、推荐六章结构

```text
第一章 绪论
第二章 医学影像深度学习相关理论与关键技术
第三章 持续医学图像分割的场景定义与综合评测研究
第四章 基于梯度子空间融合的无回放联邦持续医学图像分类研究
第五章 面向弱监督分割与配准的医学影像持续学习研究
第六章 总结与展望
```

导师讨论稿没有给出第六章却写了“第七章 总结与展望”。本版本默认把总结与展望连续编号为第六章，不保留空章。

## 三、迁移已完成后的正文边界

当前分支已完成导师框架迁移。不要重新迁移章节；应先阅读 `THESIS_CONTRACT.md`、当前章节卡和交接上下文，再按作者审阅结论推进。

```text
不得丢弃任何未提交修改，不得直接覆盖或合并 `main`。
第二章 2.1.1 保持已核实正文，2.1.2 在作者明确授权前保持 `queued`。
```

每轮受控写作或审阅后应维护：

- 新目录和连续六章的编译 PDF；
- 第一章迁移 diff；
- `handoff/LATEST_CODEX_REPORT.md`；
- 新的 `handoff/CONTEXT_PACKET_FOR_GPT.md`；
- ScribbleCL 尚缺实验的明确清单。

## 四、模型分工

```text
Codex Sol High：读取本地工程、迁移结构、检索事实源、集成 LaTeX、编译和 QA
GPT Pro：学术论证、中文正文、创新点、跨章节综合和审稿
作者：确认标题、章节逻辑、实验真实性和最终表达
```

不要让 GPT 与 Codex 同时自由重写同一小节。Codex 可以调整章节标题、标签、引用位置和过渡语句，但不得在无证据时生成新的科学结论。

## 五、四项工作在新结构中的位置

```text
Benchmark    → 第三章
FedSubMerge  → 第四章
ScribbleCL（引用静态弱监督模块 + 新增持续研究） → 第五章 5.3
SAMCL        → 第五章 5.4
```

文献 `zhang2026zscribbleseg` 仅是 ScribbleCL 当前任务弱监督模块的技术来源。只有新增的 Class-CL / Organ-CL 任务、基线、指标和结果属于 ScribbleCL 论文工作；结果未完成时写 `TODO-EXPERIMENT`。

## 六、迁移后写作顺序

```text
第一章迁移与作者复审
→ 第二章按新骨架继续
→ 第三章 Benchmark
→ 第四章 FedSubMerge
→ 第五章 ScribbleCL + SAMCL
→ 第六章总结与展望
→ 中英文摘要与全书终审
```

摘要虽然位于前置部分，但在第六章完成后定稿。

## 七、日常工作流

1. Codex 读取 `THESIS_CONTRACT.md`、作者协议、当前章节卡和本地事实源；
2. Codex 生成当前小节的证据上下文包；
3. GPT Pro 完成一个可独立验收的小节；
4. Codex 写入 LaTeX、核对引用与数字、完整编译并运行差异范围 QA；
5. 作者审阅研究边界和表达；
6. 章节完成时运行全仓风格、重合、引用、图表和 PDF 巡检。

## 八、作者表达与原创性

请始终读取：

- `AUTHORSHIP_PROTOCOL.md`
- `AUTHOR_VOICE.md`
- `qa/style_red_flags.csv`

本流程不承诺 AI 检测结果，也不使用随机改写、故意制造语病或无意义同义词替换。每个论断应绑定真实来源、实验或明确的作者分析。

## 九、常用命令

```bash
make thesis
make style
make overlap
make qa
make clean
```

单小节快速核验：

```bash
bash scripts/verify_fast_section.sh chapters/chXX_name.tex
```

框架迁移完成前，不要继续撰写 2.1.2。
