# Codex 最新报告：导师框架迁移（2026-07-31）

## 分支、保护与范围

- 分支：`framework/supervisor-2026-07-31`；迁移基线：`c74d0b2`。未切换或合并 `main`，未执行 reset、clean 或 checkout 丢弃工作。
- 未提交工作开始前已保存可恢复补丁：`/Users/bominwang/Downloads/phd-thesis-framework-migration-20260731-162417.patch`，SHA-256 `38f301511f65a5bef35b4c254dd1eb12662d22dc292a05c051f3736015593d5a`。该补丁未加入仓库。
- GitHub 迁移提交：`0a839010742f85bde98fc2e167d836cf5bea8316`，已推送至 `origin/framework/supervisor-2026-07-31`；未合并或覆盖 `main`。
- Overleaf 已在完整部署构建后同步，远端提交：`9b394141049b58fda5379cd868378ad73a5c4ac5`，部署来源为上述 GitHub 迁移提交。

## 结构与内容迁移

- 正文入口已改为连续六章：Benchmark（旧第4章）→ 第3章；FedSubMerge（旧第6章）→ 第4章；ZScribbleSeg（旧第3章）与 SAMCL（旧第5章）→ 第5章的5.3.1与5.4；总结（旧第7章）→ 第6章。旧章节文件不再被 `main.tex` 引用，`chapter_cards/ch07.md` 已退役。
- 第一章按 1.1.1--1.1.4、1.2.1--1.2.3、1.3.1--1.3.4 和 1.4 重构；原 1.5 已并入 1.4 末尾。保留已核实引用与审慎边界，并首次定义“数据不全”不等于缺失值或物理删除。
- 第一章贡献顺序为 Benchmark → FedSubMerge → ZScribbleSeg/ScribbleCL → SAMCL。原始 ZScribbleSeg 仍为静态弱监督方法；ScribbleCL 保持 `TODO-EXPERIMENT`。SAMCL 明确有限回放；FedSubMerge 不声称形式化隐私。
- 第二章 2.1.1 保持迁移前已验证正文和公式；只调整章名和2.1.2后的骨架。2.1.2 状态仍为 `queued`。

## 账本与状态

- `evidence/claims.csv`：151 条记录均保留；10 条 ZScribbleSeg 记录人工映射至 5.3.1；旧 1.2/1.3 记录按语义重映射，8 条旧 1.5 结构记录并入 1.4 并改写为六章说明。
- `evidence/experiments.csv` 与 `evidence/equations.csv` 为空，未虚构实验或公式；`evidence/limitations.csv` 已重映射至 4.7、5.6 和 6.3。
- `qa/chapter_status.csv` 标记第一章为 `drafted_pending_review` / `drafted_pending_reverification`，2.1.1 为 `drafted_and_verified`，2.1.2 为 `queued`。

## 构建与 QA

- 执行：`latexmk -C main.tex`，随后 `latexmk -xelatex -interaction=nonstopmode -file-line-error main.tex`；退出码均为 0。
- PDF：55 页，730,359 字节，SHA-256 `c56578652aed221e1a8cb23e0cd1de07740e180f7433b367948cfff167527e64`。
- 静态检查：46 个活动引用键全部存在；84 个活动标签无重复；无 undefined citation/reference、missing file、duplicate label 或 overfull/underfull 警告。
- 已运行 `style_audit.py` 与 `reference_overlap_audit.py`。前者只提示第一章“同时”30 次，需作者结合文意复审；后者未发现达到 28 个规范化字符阈值的参考论文长文本重合。
- PDF 视觉核验覆盖封面、目录/前置部分、第一章页、第二章 2.1.1 页、第三至第六章首页与参考文献首页；Quick Look 正常渲染中文封面和新暂定题目。基于 Poppler 的临时渲染器未显示正文 CJK 字形，故以 XeLaTeX 构建日志、Quick Look 和无版面警告共同核验；未观察到裁切或异常空白。

## 作者待审与下一动作

- `AUTHOR-DECISION-REQUIRED`：暂定题目是否采用候选一；是否正式采用连续六章；“数据不全”定义与第一章 1.1.2--1.1.4、1.2.3、1.3.2、1.4 的表述强度。
- ScribbleCL 仍缺任务协议、代码版本、数据划分、种子、逐阶段日志、性能矩阵、表格与可复现证据；在这些材料齐备前不得写结果或称为新算法。
- 下一步只能是作者复审第一章、题目与六章目录；不得直接继续 2.1.2。
