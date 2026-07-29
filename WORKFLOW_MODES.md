# 写作集成工作流分层

本工程将“每个已批准小节的快速可靠集成”与“章节级发布审查”分开执行。目的不是减少证据、编译或 Git 安全门槛，而是避免把与本轮无关的全仓审查、全 PDF 巡检和上下文包重建重复到每一个小节。

## A. 快速小节集成（默认）

适用于单个已批准小节，且不修改模板、跨章节结构、图表、构建配置或 `sources/`。

每轮必须完成：

1. 检查工作区、分支与 `origin/main` 是否可快进；有分叉、冲突或范围外修改即停止。
2. 读取 `AGENTS.md`、`STATE.md`、相关章节卡及本轮任务。总契约、作者协议、作者声音和项目配置在本会话首次任务或其文件变更后重读即可。
3. 精确写入批准稿；核对本轮引文、BibTeX key/DOI/归一化题名、CSV 结构及新增 ID/术语唯一性。
4. 以 `git diff` 核对只触及任务允许的文件；在会话首尾核对 `sources/` 指纹，且每轮确认 `sources/` 不在 diff 中。
5. 运行一次完整 `latexmk` 构建，并检查本轮日志中的 LaTeX 错误、未定义引文/引用、重复标签、缺失文件、TODO/TBD/?? 和新增版面警告。
6. 对新增正文执行差异范围的作者表达与参考论文重合检查：

   ```bash
   bash scripts/verify_fast_section.sh chapters/chXX_name.tex
   ```

7. 仅视觉检查受影响的小节页面及因新增引用而变化的参考文献页面。
8. 更新简明 `STATE.md`、`qa/chapter_status.csv` 与 `handoff/LATEST_CODEX_REPORT.md`，提交并推送 GitHub；若修改了 Overleaf 编译输入，随后同步 Overleaf。

`handoff/CONTEXT_PACKET_FOR_GPT.md` 只在 GPT Pro 明确需要新上下文包、完成一个章节或进入新章节时重建；日常小节集成只在 `LATEST_CODEX_REPORT.md` 写清下一节即可。

## B. 章节里程碑审查（强制）

在以下任一节点运行完整审查：一个章节完成、进入下一章、向导师/合作者发送版本、外部评阅前，或用户明确要求全量审查。

```bash
bash scripts/build_and_audit.sh
```

还必须执行：全章/全库引用与证据一致性检查、全章 PDF 视觉巡检、全部 `sources/` 文件数与 SHA-256 指纹复核、完整上下文包重建，以及对报告中遗留问题的复核。

## 覆盖规则

具体 `CODEX_TASK_*.md` 明确要求的检查优先于本文件。其要求未更新前，历史任务仍可能采用全量流程；后续 GPT Pro 任务应引用本文件的 A 模式，除非本轮属于 B 模式。
