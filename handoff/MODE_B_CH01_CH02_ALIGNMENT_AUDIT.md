# Mode B 审查：第一、二章对齐修订（2026-08-08）

## 基线与范围

- 基线：`main` 的 `7d2950dcc86832044fd3489c59e1752a5be235ec`；开始时工作树干净，`origin/main` 已快进对齐。
- 批准事实源：`/Users/bominwang/Downloads/CH01_CH02_REVISION_SPEC.md`；执行约束：`/Users/bominwang/Downloads/CODEX_TASK_ch01_ch02_alignment_revision.md`。
- 修改范围限于第一、二章、两张 Chapter 1 TikZ 图、契约/章节卡/计划、证据/公式/符号/术语账本、状态与本审查上下文文件；未修改文献库、`sources/`、第三至第六章正文、Chapter 5 或 `evidence/experiments.csv`。

## 内容与账本结果

- Chapter 1 的 1.3 顺序为 Benchmark → FedSubMerge → ScribbleCL → SAMCL；四个 subsection 的标签保持不变。1.1.4、1.2.1 的限定段落、图 1-1 和图 1-2 按批准稿集成。
- Chapter 2 使用“训练信息受限条件下的学习问题”；分别登记 HD、HD95、ASSD、Acc 与 ACC，并以 $p$ / $\mathbf{I}_p$ 区分参数梯度维度和图像空间维度 $d$。表 2-1 明确完整历史访问可采用集中式或分布式组织。
- 已同步 `THESIS_CONTRACT.md`、章节卡、计划、章节状态、`evidence/claims.csv`、`evidence/equations.csv`、`qa/notation.csv` 和 `qa/terminology.csv`。CSV 模式、ID 和术语/符号键均无重复。

## 保护与来源复核

- `subsec:intro-challenge-scribble`：基线/当前 SHA-256 均为 `ce6c5f5c32c5e4430e509490bbdf637bcfe4c54c11a502f7c575633804aece24`。
- RQ3：基线/当前 SHA-256 均为 `251859b266f7e7b31107757c4d2ff5de2c7fce6e85fd024ef41c6b85b72b300e`。
- 创新点（3）及 `TODO-EXPERIMENT`：基线/当前 SHA-256 均为 `ac1d77c5ebb0ed2edfd6501eed716ab181baa5eea4c20b41d3369a0b40d39043`。
- `chapters/ch05_scribble_samcl.tex` SHA-256：`69dc03bf56bdd8140f26acdf0036087fb52f06ae4b89bf9f22f7af24168e0e32`，与基线一致。
- `sources/`：237 个非 AppleDouble 文件；排序 SHA-256 指纹 `6c5d3c84a5418fffc6f2c3130b0a3939343acc9403b15dd53fe76e18f17ebf8f`，与基线一致。

## 构建与视觉审查

- 执行 `bash scripts/build_and_audit.sh` 成功；`main.pdf` 为 123 页。最终日志无 LaTeX error、未定义引用/交叉引用、重复 label 或缺失文件。
- 公式/章节标签已解析：图 1-1 为印刷页 6、图 1-2 为印刷页 17；HD、HD95、ASSD 为 2.4--2.7；Acc 为 2.14；2.2 标题、表 2-1 和梯度投影标签均已解析。
- 视觉检查覆盖 PDF 物理页 20（图 1-1）、31（图 1-2）、36（HD/HD95/ASSD）、39（Acc/ACC）、40（2.2 标题）、43（表 2-1）和 45（$\mathbf{I}_p$）。所有图件为黑白灰，文字、公式、表格和箭头清晰，无裁切、重叠或歧义。
- `git diff --check` 通过。规则型作者表达审查仅报告全稿既有的连接词提示；参考论文文本重合审查未发现达到阈值的长文本精确重合。

## 未解决事项

- ScribbleCL 仍为 `TODO-EXPERIMENT` / `blocked_by_experiments`，任务协议、基线、日志、性能矩阵、表格和结论均未改写或补造。
- TRE 与非正 Jacobian 的既有 `TODO-EVIDENCE-REG-001/002` 继续开放，与本轮无关。
