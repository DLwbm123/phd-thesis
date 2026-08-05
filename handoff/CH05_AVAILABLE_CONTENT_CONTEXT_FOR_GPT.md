# 第五章可写内容复审上下文包（2026-08-05）

- 正文来自作者批准草稿 `CH05_DRAFT_FOR_REVIEW.tex`（SHA-256 `2f377a56ffb4970dbf839a8511da18e24301003ce34c99167c571ffdcd5d7e23`）。
- 5.3.1 是 ZScribbleSeg 的静态弱监督方法和原始实验；不得改写为原生持续学习方法。前列腺结果采用 Table 9 和算术一致的 `0.706`，不采用相邻正文的 `0.726`。
- 5.3.2 只写入已审计的 MMWHS 三阶段协议、四个核心方法、无历史原始图像回放边界与分析公式。`experiments/scribblecl/reports/core_results.md` 明确结果仍在运行，故没有任何 ScribbleCL 数值或方向性结论。
- 5.4 是 SAMCL 的有限原始图像对回放、元持续学习和锐度感知优化。Dice 与 TRE 的 BWT 方向必须分开解释；SAMCL 不在所有任务上统一优于 MER。Algorithm 1 的元更新印刷形式仍待最终代码核对。
- 复制的原始矢量图仅为 `figures/ch05/samcl_framework.pdf` 和 `figures/ch05/samcl_qualitative.pdf`，其 SHA-256 分别为 `bd950fcf8320c604e577f92d47d2b0bf17a6141457896c1debbbe2e8f0704559` 和 `321fa6987a264182351685ee443f9489b135ce57347adb24c5e34da82afe6930`。没有对 PNG 图件转换、截图或拼接。
