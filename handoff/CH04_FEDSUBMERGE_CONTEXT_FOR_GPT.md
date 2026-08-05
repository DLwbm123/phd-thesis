# 第四章 FedSubMerge 复审上下文包（2026-08-05）

## 事实源与集成内容

- 正文：`chapters/ch04_fedsubmerge.tex`；三张未改动的矢量图位于 `figures/ch04/`。
- 最终事实源为 `sources/fedsubmerge/ Subspace Merging for Replay-Free Federated Continual Medical Image Classification 720/`：主稿 SHA-256 `8a21c2fadc4c5bd0eac0fe48931f03d756e25a392ee9a12af143a13a7828fb6e`，附录 SHA-256 `f0a4243107ee27b8815d79d5b56870282cb7793e768b40a040f5f307def4b455`。
- 章节含 7 个一级节、30 个显示公式、算法 `alg:fedsubmerge`、6 张表和 3 幅图。引文均已解析；新增 17 条 BibTeX 记录，另外 4 条复用既有的同一文献记录，均来自最终文献库。

## 复核重点

- 保持 receive--project--update--merge 递归：客户端接收服务器返回 PGS、投影当前梯度、在任务边界联合返回摘要与当前梯度更新 PGS，再上传服务器。
- FedSubMerge 是统一服务器融合；FedSubMerge-AD 是逐层选邻、含目标节点自身的个性化融合。`n=K-1` 为统一融合，`n=0` 仅目标节点 PGS。
- 理论只在光滑和有效更新完全投影等条件下解释旧任务损失的一阶机制；不能外推为 ACC、BWT、收敛或隐私保证。截断后的子空间不保证嵌套。
- 无回放表示不在后续优化中重用历史原始样本，不表示 PGS 无泄露或具有形式化隐私。

## 数值与账本

- `evidence/experiments.csv` 已登记 196 个主表值、40 个异质性值、27 个规模/参与率值、28 个消融值及图中汇总值；点估计没有标准差或显著性结论。
- 主要现象：两种所提方法均在七个设置取得无回放比较方法中的最高 ACC；AD 在五个设置 ACC 更高，统一融合在七个设置 BWT 更高。

## 当前工程状态

- `qa/chapter_status.csv` 标记第四章及其小节为 `drafted_pending_review`。下一动作仅为作者/GPT Pro 全章复审和修订，不授权第五章。
- 本地 XeLaTeX 生成 105 页 PDF，第四章为印刷页 51--69，PDF SHA-256 为 `14c5ca7194c96b09febe7f72e41abf4ce388237facf4ef2797eaaa7cd8d9428d`。`config/thesis_info.tex` 保持 `cjk-font = fandol` 未改。
- `pdffonts` 确认 FandolSong、FandolHei、FandolKai 等正文 CJK 字体均已嵌入并子集化。MuPDF 已逐页复核第三章代表页 34 与第四章印刷页 51--69：中文、公式、表格和图件均正常可见。macOS Quick Look/PDFKit 亦能正常显示中文。
- 因此，Poppler `pdftoppm` 对本 PDF 的中文空白仅认定为该工具的 CJK 渲染/映射限制，而非论文的跨平台字体故障；不修改字体配置，也不使用 macOS 专用字体。第四章现可提交、推送和同步 Overleaf，后续动作仍仅为作者/GPT Pro 全章复审，不授权第五章。
