# 当前写作状态

## 框架版本

- 当前框架：导师讨论后 V3，生效日期 2026-07-31。
- 当前作者复审工作题目：面向任务持续演化与训练信息受限的医学影像持续学习研究。
- 术语层级：技术分析优先使用“训练信息受限”；“数据不全”仅为背景概括，不指缺失值或物理删除。
- 正文章节：连续六章；不得保留空白第六章。
- 总契约：`THESIS_CONTRACT.md`。

## 当前阶段

- 导师框架迁移与题目、第一章作者复审已于 2026-07-31 完成，连续六章结构已批准；第一章状态为 `drafted_and_verified`。2026-08-09 的 Mode B 作者贡献边界修订取代了先前与本边界冲突的第五章要求：1.2 只保留其他研究者的已有工作，四项论文工作统一为 Benchmark、FedSubMerge、ScribbleCL、SAMCL；文献 `zhang2026zscribbleseg` 仅为 ScribbleCL 的引用技术来源。
- 第二章剩余内容（2.1.3、2.2、2.3、2.4）已完成工程集成；第二章整体为 `drafted_pending_review`。2.1.1“医学图像分割”与 2.1.2“医学图像配准”继续为 `drafted_and_verified`；本轮批准范围内更新了 2.1.1 的 HD、HD95、ASSD 定义，2.1.3 的 Acc/ACC 区分，2.2 严格术语、表 2-1 完整联合训练行及 2.3.3 的 $d$/$p$ 符号边界。
- 第三章 Benchmark 继续为 `drafted_pending_review`，本轮不复审、不批准也不修改。作者已于本任务明确授权第四章开始并完成工程集成；旧的“第四章正文不得开始”限制已失效。
- 第四章 FedSubMerge 已完成批准稿、最终图表、文献和证据账本的工程集成，状态为 `drafted_pending_review`；尚未获得作者/GPT Pro 全章复审批准。
- 第五章已重构 ScribbleCL 的方法与实验设定：覆盖 Domain-CL、Class-CL 和 Organ-CL，并使用 Dense-Sequential、PCE-Sequential、ZS-Sequential、ZS-Regu 和 ZS-MiB。5.3.1 现以“监督增强、类别分布校正与结构先验正则化”说明当前任务弱监督目标。Dense-Sequential 已从第三章 Non-CL 填入；PCE-Sequential、ZS-Sequential、ZS-Regu 和 ZS-MiB 结果仍为 `TODO-EXPERIMENT` / `blocked_by_experiments`。实验分析、讨论和结论暂未写作；SAMCL 方法和原始实验保持不变。
- TRE 通用数学定义（`TODO-EVIDENCE-REG-001`）与非正 Jacobian 比例具体统计形式（`TODO-EVIDENCE-REG-002`）尚未闭合，但二者均未作为公式写入 2.1.2 正文。
- ScribbleCL 持续学习实验继续为 `TODO-EXPERIMENT` / `blocked_by_experiments`；PCE-Sequential、ZS-Sequential、ZS-Regu 和 ZS-MiB 需要实际运行、日志和性能矩阵后方可填入结果或结论。

## 当前分支与验证

- 迁移分支：`framework/supervisor-2026-07-31`。
- 迁移基线：`c74d0b2`。
- FedSubMerge 的最高优先级事实源为作者确认的最终包：`FedSubMerge_final.tex`（SHA-256 `8a21c2fadc4c5bd0eac0fe48931f03d756e25a392ee9a12af143a13a7828fb6e`）、`FedSubMerge_appendix.tex`（`f0a4243107ee27b8815d79d5b56870282cb7793e768b40a040f5f307def4b455`）及其最终文献库和三张图；第四章只以该包为依据。
- 未提交迁移补丁已保存于仓库外：`/Users/bominwang/Downloads/phd-thesis-framework-migration-20260731-162417.patch`，SHA-256 `38f301511f65a5bef35b4c254dd1eb12662d22dc292a05c051f3736015593d5a`。
- 2026-08-09 Mode B 完整构建成功，生成 123 页 `main.pdf`；无 LaTeX error、未定义引用/交叉引用、重复标签或缺失文件。已用 MuPDF 复核第一章 1.2、1.4/图 1-2 和第五章 5.3、5.5、5.6 页面。完整结果见 `handoff/LATEST_CODEX_REPORT.md`。
- 最近的 Mode B 审查见 `handoff/MODE_B_CH01_CH02_ALIGNMENT_AUDIT.md`；审查基线为 `7d2950dcc86832044fd3489c59e1752a5be235ec`，其中 `sources/`、`chapters/ch05_scribble_samcl.tex`、`evidence/experiments.csv` 及 Chapter 1 ScribbleCL 保护块均已复核未变。

## 下一动作

下一动作是第四、五章作者/GPT Pro 全章复审与必要修订；ScribbleCL 仅在 PCE-Sequential、ZS-Sequential、ZS-Regu 和 ZS-MiB 实际运行、日志和性能矩阵核验后补写结果及分析。
