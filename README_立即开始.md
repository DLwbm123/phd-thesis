# 博士论文工程（GPT Pro 三版本融合稿）

当前正文入口为 `main.tex`，结构与边界以 `THESIS_CONTRACT.md` 为准，最新集成状态见 `STATE.md`。

## 当前章节

1. 绪论
2. 医学影像深度学习相关理论与关键技术
3. 医学影像持续学习平台设计与分割基准评测
4. 基于监督增强与特征一致性约束的弱监督医学影像持续分割研究
5. 基于子空间聚合的无回放联邦医学影像持续分类研究
6. 基于锐度感知元经验回放的医学影像持续配准研究
7. 总结与展望

MedCL 面向模型或预测 evaluation：用户在本地训练，平台不要求训练日志，也不执行训练或联邦聚合。平台未实际完成前，只能陈述设计、接口与测试方案。

## 构建与发布

```bash
latexmk -xelatex -interaction=nonstopmode -file-line-error main.tex
bash scripts/sync_latex_to_overleaf.sh
```

修改 Overleaf 编译输入后，先在本地完成构建与检查，再推送 GitHub，最后从干净工作区运行同步脚本。不得强推或擅自合并 `main`；`sources/`、构建产物、实验目录和证据账本不会同步到 Overleaf。
