# GPT Pro 文字修改清单执行记录（2026-09-08）

按作者批准的 `thesis_writing_revision_for_codex.md` 执行，以七章实际输入为准。基线为 `7138a3a`。205 项按锚点完成，2 项按现有图节点适配，1 项旧句已删除；另完成 34 处指定短语清理。统计及预处理按作者追加指示，以原论文记载为准。

## 修改文件与 M 编号

| 文件 | 定点项目 |
|---|---|
| `chapters/ch02_foundations.tex` | M001–M006、M052–M069 |
| `chapters/ch03_medcl_benchmark.tex` | M007–M008、M015–M018、M024、M070–M091、M201、M206–M207 |
| `chapters/ch05_fedsubmerge.tex` | M009–M013、M023、M110–M141 |
| `chapters/ch06_registration.tex` | M014、M020–M022、M142–M166 |
| `chapters/ch04_scribble.tex` | M019、M092–M109、M204–M205 |
| `SRC/abstract_zh_body.tex` | M025 |
| `SRC/abstract_en_body.tex` | M026 |
| `chapters/ch01_introduction.tex` | M027–M051、M202–M203、M208 |
| `chapters/ch07_conclusion.tex` | M167–M191 |
| `figures/ch01/thesis_work_logic.tex` | M192–M196 |
| `figures/ch05/fedsubmerge_engineering.tex` | M197–M198 |
| `figures/ch07/future_three_level_roadmap.tex` | M199–M200 |

短语清理还修改 `figures/ch03/medcl_platform_architecture.tex`、`figures/ch03/medcl_workflow_design.tex`。同步更新 `STATE.md`、`qa/chapter_status.csv` 和本报告。

## 旧锚点处理

- M194：旧长句已被精简图取代，将现有节点改为“拟提交阶段模型或预测”。
- M195：当前图中“数据与协议”有两处，平台节点与承接箭头均改为“数据与评价”。
- M199：旧句已按作者此前要求删除，不重新加回。
- M200：现有方法节点改为“参数高效／持续适配”，保留辐射布局。
- 图 1.2 保留作者确认的纵向流程、中间三列与浅灰／深灰配色。

## V 项核对及剩余材料

依据现存 Benchmark 主文与补充材料、FedSubMerge 主文与附录、SAMCL 原论文 `Paper-0150.tex`，以及当前实验来源表核对。后续复现配置不替代原论文设置。

| 项目 | 已核对内容与仍缺少的材料 |
|---|---|
| V01 | 原 FedSubMerge 主表为 −6.55、−10.95；原图注确为 Hyper-Kvasir α=0.3。仍缺该图与主表共同对应的运行标识、未舍入矩阵、种子及汇总记录，保留数值，删除“取整后一致”的推测。检索到的另一份 PathMNIST 四任务转录图数据不适用于此项。 |
| V02 | 原 SAMCL 论文明确写 training/validation/test images。正文与表注明确为原论文的影像数，所有数量保留；原文未交代同患者多幅影像的分组规则，未补写。 |
| V03 | 原表注明确配对 t 检验、p<0.05、星号及下划线含义。保留标记；原论文未说明配对单位、单双侧与多重比较校正，未补造。 |
| V04 | 原 Benchmark 定义分母为仅在对应任务训练的独立模型；补充材料给出总体网络和训练设置。仍缺独立参照逐运行配置、模型选择及随机性记录，以及第四章各方法与参照的对应关系。后续 RMA 代码不作为原表生成流程的证明。 |
| V05 | 原 SAMCL 算法将保存对象记为固定／移动图像对，任务损失另含结构或地标信息。原文未说明附属标签的缓存或索引读取方式；保留算法与损失，不补写实现细节。 |
| V06 | 原 SAMCL 论文说明早期任务训练后进行域内／域外测试，但未逐方向标明源模型是独立训练还是持续阶段模型。依 M155 区分同任务与跨任务测试，未改写为 E-FWT。 |
| V07 | 原 Benchmark 主表有均值和离散值，但未明确其统计单位；十种顺序的标准差只在顺序鲁棒性图注明确。FedSubMerge 主表未给出跨重复统计说明。第四章仍保留种子 42 的点估计，不新增重复次数、标准差或显著性。 |
| V08 | 按作者要求采用原 SAMCL 论文记载：CT 裁剪至 [-200,300]，CT／MR 线性归一化至 [0,1]。删除仅针对腹部的统一理由，不以复现设置改动数值。 |

M135 另与原 FedSubMerge 正文核对：各来源验证集和测试集分别合并为全局验证集与全局测试集。

## 验证与交付范围

全文 XeLaTeX/latexmk 构建成功，共 181 页。最终日志无 LaTeX 错误、未定义引用、重复标签、缺字及 Overfull；保留模板既有字体提示和 Underfull。已检查摘要、目录、修改的 TikZ 图及相关表格页面。中文摘要仅对长方法名增加局部换行，未改算法名称或模板。

核对确认七章展示公式、数值表格单元与显著性标记保持不变；仅按 M191 删除无引用的末章小结标签。风格检查的连接词命中不构成修改理由；参考重合检查仅命中未改动的成果列表中的会议名称。无新实验，未更改题目、算法、引用库、模板、已有图片或原始材料。

GitHub 发布七章、中英文摘要、5 份 TikZ 源及状态／本报告；Overleaf 同步 14 份编译输入。完整 PDF 保存在本地 `../writing_revision_20260908/PhD_Thesis_writing_revised_20260908.pdf`。远程推送回执在最终回复中给出。
