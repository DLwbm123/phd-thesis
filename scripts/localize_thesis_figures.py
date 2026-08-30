#!/usr/bin/env python3
"""Translate PDF figure labels; preserve the original plots and medical images.

Run with Python + PyMuPDF. The immutable source revision is the imported
pre-defense manuscript; its chapter 4/5 asset paths predate the chapter swap.
The two overview diagrams are separately redrawn in native TikZ.
"""
from collections import Counter
from pathlib import Path
import re
import subprocess

import fitz

fitz.TOOLS.set_small_glyph_heights(True)

ROOT = Path(__file__).resolve().parents[1]
SOURCE_REVISION = "b34b0e4"
FONT = ROOT / "FontStyle/SimHei.ttf"
METRICS = fitz.Font(fontfile=str(FONT))
TRANSLATIONS = {
    "Continual": "持续", "Learning": "学习", "Test-time": "测试时",
    "Adaptation": "适应", "Transfer": "迁移", "Unuspervised": "无监督",
    "Unsupervised": "无监督", "Domain": "领域", "Representation": "表征",
    "Generative": "生成式", "Models": "模型", "Multi-task": "多任务",
    "Few-shot": "少样本", "Meta-": "元", "Reinforcement": "强化",
    "Federated": "联邦", "Novel Class": "新类别", "Discovery": "发现",
    "Open": "开放", "World": "世界", "Method": "方法",
    "Task Order": "任务顺序", "Buffer Size": "回放容量",
    "SAM with LoRA Fine-Tuning": "SAM 低秩适配微调",
    "Domain-CL": "域增量", "Organ-CL": "器官增量", "Class-CL": "类别增量",
    "Accuracy (%)": "准确率（%）", "Trained through task t": "已完成任务 t",
    "Evaluated task τ": "评价任务 τ", "self-only": "仅自身",
    "default": "默认", "uniform": "统一融合", "Neighborhood size n": "相关客户端数 n",
    "(a) Neighborhood size n": "（a）相关客户端数 n", "Energy threshold γ": "能量阈值 γ",
    "(b) Energy threshold γ": "（b）能量阈值 γ", "ACC (%)": "准确率（%）",
    "BWT (%)": "后向迁移（%）", "Fixed": "固定图像", "Moving": "移动图像",
    "Brain MR-MR": "脑部 MR–MR", "Abdomen CT-CT": "腹部 CT–CT",
    "Lung CT-CT": "肺部 CT–CT", "Abdomen MR-CT": "腹部 MR–CT",
    "Continual Medical Image Registration": "持续医学图像配准",
    "Universal Medical Image Registration": "多任务配准推理",
    "Deployment Phase": "推理阶段", "Training Phase": "训练阶段",
    "Inputs from All Tasks": "各任务图像输入", "Sequential": "顺序训练",
    "Multitask": "多任务训练", "Independent": "独立训练",
    "In-domain Generalization": "域内前向泛化",
    "Out-of-domain Generalization": "域外前向泛化",
}
TRANSLATIONS.update({f"Task {i}": f"任务 {i}" for i in range(1, 7)})
TRANSLATIONS.update({f"Order{c}": f"顺序{c}" for c in "ABCDEFGHIJ"})


def numbers(text):
    return Counter(re.findall(r"-?\d*\.\d+|-?\d+", text.replace("−", "-")))


def put_label(page, rect, text, size, color=(0, 0, 0), vertical=False):
    """Fit one translated line to the original label's horizontal/vertical extent."""
    rect = fitz.Rect(rect)
    extent = rect.height if vertical else rect.width
    size = min(size, .97 * extent / METRICS.text_length(text, fontsize=1))
    width = METRICS.text_length(text, fontsize=size)
    offset = (METRICS.ascender + METRICS.descender) * size / 2
    if vertical:
        point = ((rect.x0 + rect.x1) / 2 + offset, rect.y1 - (rect.height - width) / 2)
    else:
        point = (rect.x0 + (rect.width - width) / 2, (rect.y0 + rect.y1) / 2 + offset)
    page.insert_text(point, text, fontname="thesiszh", fontfile=str(FONT),
                     fontsize=size, color=color, rotate=90 if vertical else 0)


def main():
    for destination in sorted((ROOT / "figures").rglob("*.pdf")):
        if destination.name in {"benchmark_overview_new.pdf", "fedsubmerge_overview.pdf"}:
            continue
        old_path = destination.relative_to(ROOT).as_posix()
        old_path = old_path.replace("/ch04/", "/OLD04/").replace("/ch05/", "/ch04/").replace("/OLD04/", "/ch05/")
        original = subprocess.check_output(["git", "show", f"{SOURCE_REVISION}:{old_path}"], cwd=ROOT)
        doc = fitz.open(stream=original, filetype="pdf")
        page = doc[0]
        before_numbers = numbers(page.get_text())
        labels = []
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                text = "".join(span["text"] for span in line["spans"]).strip()
                if text not in TRANSLATIONS:
                    continue
                span = line["spans"][0]
                rect = fitz.Rect(line["bbox"])
                labels.append((rect, TRANSLATIONS[text], span["size"],
                               fitz.sRGB_to_pdf(span["color"]), line["dir"][1] < -.9))
                page.add_redact_annot(rect, fill=None)
        # Remove text only. Keep every original image, curve, bar, cell and marker.
        page.apply_redactions(images=0, graphics=0, text=0)
        for args in labels:
            put_label(page, *args)
        assert numbers(page.get_text()) == before_numbers, destination

        # These two source charts have outlined labels. Cover only their label
        # regions, leaving axes, observations, error bars and boxes unchanged.
        outlined = []
        if destination.name == "plot_memory_nnn.pdf":
            outlined = [((62, 177, 114, 189), "回放 50", 9),
                        ((62, 190, 114, 202), "回放 100", 9),
                        ((62, 203, 114, 215), "回放 200", 9)]
        elif destination.name == "plot_sam_new.pdf":
            outlined = [((470, 28, 505, 39), "无 SAM", 8),
                        ((470, 40, 505, 52), "有 SAM", 8),
                        ((54, 235, 116, 250), "CTCT→CTCT", 8),
                        ((151, 235, 216, 250), "MRCT→MRCT", 8),
                        ((249, 235, 317, 250), "CTCT→MRCT", 8),
                        ((341, 235, 404, 250), "CTCT→NLST", 8),
                        ((438, 235, 509, 250), "OASIS→NLST", 8)]
        for rect, label, size in outlined:
            page.draw_rect(rect, color=None, fill=(1, 1, 1), overlay=True)
            put_label(page, rect, label, size)
        doc.subset_fonts()
        doc.save(destination, garbage=4, deflate=True)
        print(f"{destination.relative_to(ROOT)}: {len(labels)} text labels, {len(outlined)} outlined labels; numeric text preserved")


if __name__ == "__main__":
    main()
