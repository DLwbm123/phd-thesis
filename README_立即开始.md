# 博士论文 GPT Pro × Codex Sol High 受控自动写作启动包（V2）

本版本按以下要求重新设计：

1. **从第一章绪论开始，按第一章至第七章顺序写作**；
2. **GPT Pro 负责学术写作，Codex Sol High 负责本地材料整理、LaTeX 集成、编译与审计**；
3. 使用参考毕业论文的 `fduthesis` **排版模板实现文件**，但不复制其摘要、正文、图表、标题、个人信息、参考文献或任何句段；
4. 不以“规避 AI 检测”为目标，而以原创论证、作者化表达、证据可追溯和人工可负责为标准；
5. 自动运行模板化语言审查与参考论文文本重合审查，发现问题只报告，不用机械同义替换掩盖问题。

## 一、推荐工作流

```text
Codex Sol High 准备本地上下文与证据
        ↓
GPT Pro 撰写一个完整小节
        ↓
Codex Sol High 写入 LaTeX、核对引用、编译、运行 QA
        ↓
GPT Pro 在章节节点进行学术与作者表达复审
```

你每轮只需要完成一次复制：将 GPT Pro 输出的 `[CODEX TASK]` 整块复制到 Codex。

## 二、为什么以 GPT Pro 为写作主力

- 绪论、研究主线、创新点、跨工作综合和中文学术表达需要长距离论证与判断；
- Codex 的优势是读取本地工程、检索源文件、修改多个文件、运行脚本、编译和展示 diff；
- 因此采用 **GPT Pro 主写、Codex Sol High 主执行与复核**，而不是让两个模型同时自由重写同一段正文。

详细分工见 `MODEL_ROLE_MATRIX.md`。

## 三、模板已经准备好

本目录本身就是一个干净的 `fduthesis` 工程：

```text
main.tex
config/thesis_info.tex
chapters/ch01_introduction.tex ... ch07_conclusion.tex
fduthesis.cls / fduthesis.def / 校徽资源
bibliography/references.bib
config/build_flags.tex
```

只复制了参考工程中的模板实现文件和模板资源。所有正文与元数据均为新建占位内容。模板来源与使用边界见：

- `TEMPLATE_PROVENANCE.md`
- `REFERENCE_TEMPLATE_POLICY.md`

先在 `config/thesis_info.tex` 中填写姓名、导师、院系、学号等信息；暂时不填写也可以编译。空工程默认关闭参考文献输出，Codex 在写入第一条真实引用时会把 `config/build_flags.tex` 中的开关设为 true。

## 四、放入原始研究材料

将五个工程分别解压到：

```text
sources/reference_thesis/   # 仅用于排版核对与文本重合审计
sources/zscribble/
sources/benchmark/
sources/samcl/
sources/fedsubmerge/
```

四项工作是事实源。参考毕业论文不是内容源，写作代理不得从中提取或改写句子。

## 五、第一次运行 Codex

在本目录打开 Codex Sol High，输入：

```text
请读取并严格执行 prompts/codex/00_初始化参考模板与工程.md。
完成后更新 handoff/LATEST_CODEX_REPORT.md 和 handoff/CONTEXT_PACKET_FOR_GPT.md。
```

Codex 会：

- 核对干净模板和七章骨架；
- 自动识别或整理原始材料路径；
- 编译空白论文；
- 运行风格与文本重合审查；
- 为第一章 1.1.1 节生成本地上下文包。

## 六、开始由 GPT Pro 写绪论

在当前 ChatGPT Project 中使用 Pro 模型，加载：

```text
prompts/gpt/00_主写作代理提示词.md
```

然后发送：

```text
开始撰写 1.1.1 医学影像智能分析及其临床价值。
```

GPT Pro 每轮输出：

```text
[THESIS DRAFT]
[EVIDENCE UPDATE]
[CODEX TASK — COPY ONLY THIS BLOCK]
[NEXT]
```

只复制第三个区块到 Codex。Codex 成功后，在 GPT 对话中回复：

```text
继续，Codex 已成功
```

## 七、写作顺序

```text
第一章 绪论
→ 第二章 相关理论与关键技术
→ 第三章 ZScribbleSeg
→ 第四章 Benchmark
→ 第五章 SAMCL
→ 第六章 FedSubMerge
→ 第七章 总结与展望
→ 中英文摘要与全书终审
```

摘要虽然位于论文前置部分，但在第七章完成后定稿，避免与正文不一致。

## 八、作者表达与原创性

请先阅读：

- `AUTHORSHIP_PROTOCOL.md`
- `AUTHOR_VOICE.md`
- `qa/style_red_flags.csv`

本流程不会承诺任何 AI 检测结果，也不会使用随机改写、故意制造语病或同义词替换来“过检测”。它通过以下方式降低模板化和非作者化表达：

- 每个论断绑定真实来源；
- 每段围绕具体科学对象展开；
- 写出方法选择背后的真实研究判断和边界；
- 禁止空泛套话、无证据拔高和机械对称结构；
- 使用你自己的术语、实验设定和贡献边界；
- 章节完成后由你进行最终学术确认。

## 九、常用命令

```bash
make thesis        # 编译论文
make style         # 作者表达审查
make overlap       # 与参考论文正文的重合审查
make qa            # 依次运行编译、风格和重合审查
make clean
```

也可以将 GPT 生成的任务保存到 `tasks/INBOX.md`，再运行：

```bash
bash scripts/run_codex_task.sh
```
