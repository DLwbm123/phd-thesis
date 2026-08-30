# 原始材料映射（预答辩修订 V4，2026-08-30）

| 材料 | 已核实工程根目录 | 主 TeX / 参考文献 | 新章节用途 | 内容写作权限 |
|---|---|---|---|---|
| 参考毕业论文 | `sources/reference_thesis/Thesis reference/` | `main.tex`；`main.bib`、`strings.bib` | 仅模板核对、版面检查和文本重合审查 | 禁止作为正文来源；不得导入正文、标题、图表、元数据或文献库 |
| Benchmark | `sources/benchmark/Benchmark_pa/` | `main.tex`；文献表内嵌于主文件 | 第三章场景定义、数据组织、统一协议、指标、实验和局限；第一章持续学习现状与挑战 | 允许，需证据定位；本章不是单一算法 |
| FedSubMerge | `sources/fedsubmerge/ Subspace Merging for Replay-Free Federated Continual Medical Image Classification 720/` | `FedSubMerge_final.tex`；`FedSubMerge_appendix.tex`；`references.bib` | 第五章问题建模、方法、理论、实验和讨论；第一章联邦持续学习现状与挑战 | 允许，需证据定位；不得声称形式化隐私 |
| ZScribbleSeg | `sources/zscribble/Zscribble_MEDIA_arxiv/` | `main_clean_new.tex`；`cas-refs.bib`；补充材料与补充文献 | 第四章 4.3.1 中与实现一致的全局一致性与空间先验；不转录原有离线实验；第一章弱/部分监督现状与挑战 | 允许，需证据定位；不得追溯性写成持续学习算法 |
| ScribbleCL 新增实验 | 由作者在仓库外或 `sources/scribblecl/` 建立只读事实源 | 代码版本、配置、数据划分、日志、表格、图、随机种子和实验说明 | 第四章 4.3 中 ZSDERpp 方法与已提供的 Domain-CL 结果；第一章只写有证据的结论 | 已登记 Domain-CL 点估计可用于写作；Class-CL 与 Organ-CL 不得推断结果 |
| SAMCL | `sources/samcl/MICCAI 2024: Toward Universal Medical Image Registration/` | `Paper-0150.tex`；`Paper-0150.bib` | 第四章 4.4 方法与实验；第一章持续配准现状与挑战 | 允许，需证据定位；明确有限回放 |

## 新章节到事实源的映射

```text
第三章  ← Benchmark
第四章 4.3.1 ← ZScribbleSeg 的两个弱监督组成
第四章 4.3   ← 新增 ScribbleCL 方法与 Domain-CL 实验
第四章 4.4   ← SAMCL
第五章      ← FedSubMerge；5.7 为有边界的工程流程与集成设计
```

## 原始工程构建入口核验

- 迁移任务不得修改 `sources/`；原始入口以本地实际文件为准。
- ZScribbleSeg、Benchmark、SAMCL 和 FedSubMerge 的入口及构建方式沿用迁移前已核实记录，但 FedSubMerge 应优先核对作者最近更新的主文件与图表资源是否一致。
- ScribbleCL 在形成正文前必须建立单独的实验清单与可回溯结果，不得把临时终端输出当作最终证据。

## 使用规则

1. 原始论文是事实源，不是可直接粘贴的博士论文正文；
2. 英文论文内容必须按中文博士论文论证重新组织，不逐句翻译；
3. 第一章研究现状中新增外部文献必须核实原始论文元数据和具体结论；
4. Benchmark、FedSubMerge、ZScribbleSeg 和 SAMCL 的结果必须分别标明来源；
5. ZScribbleSeg 原始结果与 ScribbleCL 新增结果不得混写；
6. 图可复用时须确认来源与版权，并重写中文图注；参考毕业论文的图不得复用；
7. 章节编号迁移后，所有证据记录的 `section_id` 和 `chapter` 字段必须同步更新。
