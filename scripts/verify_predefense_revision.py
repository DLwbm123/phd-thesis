#!/usr/bin/env python3
"""Check that the writing-only revision retains equations and reported results.

Run from any directory with Python 3. The baseline is the reconciled GitHub and
Overleaf pre-defense manuscript. This does not rerun or validate experiments.
"""
import csv
import io
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = "b34b0e4"
RENAME = {
    "chapters/ch04_fedsubmerge.tex": "chapters/ch05_fedsubmerge.tex",
    "chapters/ch05_scribble_samcl.tex": "chapters/ch04_scribble_samcl.tex",
}


def previous(path):
    return subprocess.check_output(
        ["git", "show", f"{BASE}:{path}"], cwd=ROOT, text=True
    )


def equations(text):
    result = {}
    for block in re.findall(r"\\begin\{equation\}(.*?)\\end\{equation\}", text, re.S):
        label = re.search(r"\\label\{([^}]+)\}", block)
        assert label, "Unlabelled displayed equation"
        result[label[1]] = re.sub(r"\s+", "", block)
    return result


def tables(text):
    result = {}
    for block in re.findall(r"\\begin\{table\}.*?\\end\{table\}", text, re.S):
        label = re.search(r"\\label\{([^}]+)\}", block)
        if label:
            result[label[1]] = block
    return result


def numeric_rows(table):
    result = {}
    for line in table.splitlines():
        if " & " not in line or not line.rstrip().endswith(r"\\"):
            continue
        cells = line.rstrip()[:-2].split(" & ")
        name = cells[0].strip()
        if not name or name.startswith(("\\", "&")) or name in {"方法", "配置", "参与率"}:
            continue
        values = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", " & ".join(cells[1:]))
        # SAMCL's wide table is split into two panels with the same row names.
        result.setdefault(name, []).extend(values)
    return result


def main():
    old_paths = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", BASE, "chapters"], cwd=ROOT, text=True
    ).splitlines()
    old_equations, new_equations, old_tables, new_tables = {}, {}, {}, {}
    for old_path in old_paths:
        if not re.search(r"/ch0[1-6]_.*\.tex$", old_path):
            continue
        before = previous(old_path)
        after = (ROOT / RENAME.get(old_path, old_path)).read_text()
        old_equations.update(equations(before))
        new_equations.update(equations(after))
        old_tables.update(tables(before))
        new_tables.update(tables(after))
    assert old_equations == new_equations, "Displayed mathematical content changed"
    result_labels = [
        "tab:benchmark-domain-results", "tab:benchmark-class-results",
        "tab:benchmark-organ-results", "tab:scribblecl-domain-results",
        "tab:samcl-main-results", "tab:fedsubmerge-main-distribution",
        "tab:fedsubmerge-main-other", "tab:fedsubmerge-heterogeneity",
        "tab:fedsubmerge-scalability", "tab:fedsubmerge-ablation",
    ]
    row_count = 0
    for label in result_labels:
        before, after = numeric_rows(old_tables[label]), numeric_rows(new_tables[label])
        assert before == after, f"Result table changed: {label}"
        row_count += len(before)
    old_rows = list(csv.DictReader(io.StringIO(previous("evidence/experiments.csv"))))
    with (ROOT / "evidence/experiments.csv").open(newline="") as stream:
        new_rows = list(csv.DictReader(stream))
    for rows in (old_rows, new_rows):
        for row in rows:
            for old, new in RENAME.items():
                row["source_file"] = row["source_file"].replace(old, new)
    assert old_rows == new_rows, "Experiment ledger changed beyond chapter path remapping"
    includes = re.findall(r"\\include\{chapters/(ch\d\d_[^}]+)\}", (ROOT / "main.tex").read_text())
    assert [name[2:4] for name in includes] == [f"{i:02d}" for i in range(1, 7)]
    assert "ch04_scribble_samcl" in includes and "ch05_fedsubmerge" in includes
    abstracts = [(ROOT / f"SRC/abstract_{lang}_body.tex").read_text() for lang in ("zh", "en")]
    math_values = [re.findall(r"[-+]?(?:\d*\.\d+|\d+)", " ".join(
        re.findall(r"\$(.*?)\$", abstract))) for abstract in abstracts]
    assert math_values[0] == math_values[1], "Chinese/English abstract numbers differ"
    scribble = numeric_rows(new_tables["tab:scribblecl-domain-results"])
    federated = numeric_rows(new_tables["tab:fedsubmerge-main-distribution"])
    gains = [f"{float(scribble['ZSDERpp'][0]) - float(scribble['ZS-Sequential'][0]):.3f}",
             f"{float(federated['FedSubMerge-AD'][0]) - float(federated['FOT'][0]):.2f}"]
    assert all(gain in math_values[0] for gain in gains), "Abstract gains differ from tables"
    print(f"PASS: {len(old_equations)} equations, {len(result_labels)} result tables / "
          f"{row_count} rows, {len(old_rows)} ledger records; six chapters in order.")


if __name__ == "__main__":
    main()
