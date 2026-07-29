#!/usr/bin/env python3
"""Rule-based author-voice audit. This is not an AI detector.

It flags canned phrasing, repeated paragraph openings, and overused transitions.
It never rewrites text automatically and should be interpreted by a researcher.
"""
from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from pathlib import Path


def strip_comments(text: str) -> str:
    return re.sub(r"(?<!\\)%.*", "", text)


def iter_tex_files(root: Path):
    if root.is_file() and root.suffix == ".tex":
        yield root
    elif root.exists():
        yield from sorted(root.rglob("*.tex"))


def paragraphs(text: str):
    text = strip_comments(text)
    for block in re.split(r"\n\s*\n", text):
        cleaned = re.sub(r"\\(?:chapter|section|subsection|subsubsection|label|cite\w*|ref|eqref)\*?(?:\[[^\]]*\])?\{[^{}]*\}", "", block)
        cleaned = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^\]]*\])?", "", cleaned)
        cleaned = re.sub(r"[{}$]", "", cleaned)
        cleaned = re.sub(r"\s+", "", cleaned)
        if len(cleaned) >= 30:
            yield cleaned


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="chapters")
    ap.add_argument("--patterns", default="qa/style_red_flags.csv")
    ap.add_argument("--output", default="qa/style_audit_report.md")
    args = ap.parse_args()

    root = Path(args.input)
    pattern_file = Path(args.patterns)
    output = Path(args.output)
    findings = []
    opening_counter = Counter()
    file_paragraphs = []

    rules = []
    if pattern_file.exists():
        with pattern_file.open(encoding="utf-8-sig", newline="") as f:
            rules = list(csv.DictReader(f))

    for tex in iter_tex_files(root):
        text = tex.read_text(encoding="utf-8", errors="ignore")
        for rule in rules:
            pat = rule["pattern"]
            if rule["mode"] == "regex":
                count = len(re.findall(pat, text))
            else:
                count = text.count(pat)
            threshold = int(rule.get("threshold") or 1)
            if count >= threshold:
                findings.append((str(tex), rule["category"], pat, count, rule["reason"]))
        for para in paragraphs(text):
            opening = para[:12]
            opening_counter[opening] += 1
            file_paragraphs.append((str(tex), para))

    repeated = [(op, c) for op, c in opening_counter.items() if c >= 3]
    repeated.sort(key=lambda x: (-x[1], x[0]))

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as f:
        f.write("# 作者表达审查报告\n\n")
        f.write("> 本报告是规则型写作质量检查，不是 AI 检测器，也不能预测任何检测结果。\n\n")
        f.write("## 规则命中\n\n")
        if findings:
            f.write("| 文件 | 类别 | 模式 | 次数 | 原因 |\n|---|---|---:|---:|---|\n")
            for item in findings:
                f.write(f"| `{item[0]}` | {item[1]} | `{item[2]}` | {item[3]} | {item[4]} |\n")
        else:
            f.write("未发现达到阈值的预设模式。\n")
        f.write("\n## 重复段落开头\n\n")
        if repeated:
            f.write("| 归一化开头 | 次数 |\n|---|---:|\n")
            for op, count in repeated[:30]:
                f.write(f"| `{op}` | {count} |\n")
        else:
            f.write("未发现出现三次及以上的相同段落开头。\n")
        f.write("\n## 解释原则\n\n")
        f.write("命中不等于错误。技术术语可合理重复；需要人工判断是否为空泛套话、机械衔接或必要的精确表达。禁止为了消除命中而无意义替换同义词。\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
