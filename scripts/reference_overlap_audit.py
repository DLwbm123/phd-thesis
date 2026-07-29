#!/usr/bin/env python3
"""Find long exact textual overlaps between thesis chapters and reference thesis.

This audit is designed to prevent accidental copying. It is not a plagiarism
classifier and it must not be used to conceal overlap through superficial
paraphrasing.
"""
from __future__ import annotations

import argparse
import difflib
import re
from collections import defaultdict
from pathlib import Path

COMMON = {
    "研究背景及意义", "国内外研究现状", "本文主要研究内容", "论文组织结构",
    "本章小结", "总结与展望", "实验设置", "结果与分析", "问题设定",
}


def tex_files(root: Path):
    if root.is_file() and root.suffix == ".tex":
        yield root
    elif root.exists():
        yield from sorted(root.rglob("*.tex"))


def normalize(block: str) -> str:
    block = re.sub(r"(?<!\\)%.*", "", block)
    block = re.sub(r"\\(?:cite\w*|ref|eqref|label|includegraphics|url|href)\*?(?:\[[^\]]*\])?\{[^{}]*\}", "", block)
    block = re.sub(r"\\begin\{[^{}]*\}|\\end\{[^{}]*\}", "", block)
    block = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^\]]*\])?", "", block)
    block = re.sub(r"\$.*?\$|\\\[.*?\\\]", "", block, flags=re.S)
    block = re.sub(r"[{}\[\]`~^_&|<>]", "", block)
    block = re.sub(r"[\s，。；：、！？,.!?;:()（）\-—]+", "", block)
    return block


def load_paragraphs(root: Path):
    result = []
    for file in tex_files(root):
        text = file.read_text(encoding="utf-8", errors="ignore")
        for i, block in enumerate(re.split(r"\n\s*\n", text), start=1):
            norm = normalize(block)
            if len(norm) >= 30:
                result.append((file, i, norm))
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--thesis", default="chapters")
    ap.add_argument("--reference", default="sources/reference_thesis")
    ap.add_argument("--min-chars", type=int, default=28)
    ap.add_argument("--output", default="qa/reference_overlap_report.md")
    args = ap.parse_args()

    thesis_root = Path(args.thesis)
    ref_root = Path(args.reference)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    if not ref_root.exists() or not any(tex_files(ref_root)):
        output.write_text("# 参考论文文本重合审查报告\n\n未找到参考论文的 `.tex` 正文，审查未运行。\n", encoding="utf-8")
        return 0

    thesis = load_paragraphs(thesis_root)
    refs = load_paragraphs(ref_root)
    seed_len = min(14, max(8, args.min_chars // 2))
    index = defaultdict(set)
    for idx, (_, _, text) in enumerate(refs):
        for pos in range(0, max(1, len(text) - seed_len + 1), max(1, seed_len // 2)):
            index[text[pos:pos+seed_len]].add(idx)

    matches = []
    seen = set()
    for tf, ti, ttext in thesis:
        candidates = set()
        for pos in range(0, max(1, len(ttext) - seed_len + 1), max(1, seed_len // 2)):
            candidates.update(index.get(ttext[pos:pos+seed_len], ()))
        for ridx in candidates:
            rf, ri, rtext = refs[ridx]
            match = difflib.SequenceMatcher(None, ttext, rtext, autojunk=False).find_longest_match()
            if match.size < args.min_chars:
                continue
            span = ttext[match.a:match.a+match.size]
            if span in COMMON or any(span == x for x in COMMON):
                continue
            key = (str(tf), ti, str(rf), ri, span)
            if key not in seen:
                seen.add(key)
                matches.append((match.size, tf, ti, rf, ri, span))

    matches.sort(key=lambda x: -x[0])
    with output.open("w", encoding="utf-8") as f:
        f.write("# 参考论文文本重合审查报告\n\n")
        f.write("> 本报告用于防止误复制，不是查重系统。发现重合后应回到本研究证据重新组织论证，不能只做同义词替换。\n\n")
        f.write(f"最低报告长度：{args.min_chars} 个归一化字符。\n\n")
        if not matches:
            f.write("未发现达到阈值的长文本精确重合。\n")
        else:
            f.write("| 长度 | 本论文位置 | 参考论文位置 | 重合片段 |\n|---:|---|---|---|\n")
            for size, tf, ti, rf, ri, span in matches[:100]:
                short = span[:120] + ("…" if len(span) > 120 else "")
                f.write(f"| {size} | `{tf}` 段 {ti} | `{rf}` 段 {ri} | `{short}` |\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
