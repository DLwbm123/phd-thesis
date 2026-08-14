#!/usr/bin/env python3
"""Print a deterministic SHA-256 fingerprint of every Overleaf build input."""
from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPLICIT = (
    ".gitignore",
    "main.tex",
    "latexmkrc",
    "Makefile",
    "FDSDSthesis.cls",
    "macros.tex",
    "bibliography/references.bib",
    "scripts/run_bibtex.sh",
)
TREE_EXTENSIONS = {
    "FontStyle": None,
    "fig": None,
    "SRC": {".tex"},
    "chapters": {".tex"},
    "figures": None,
    "tables": None,
}


def paths() -> list[Path]:
    selected = [ROOT / name for name in EXPLICIT]
    for directory, extensions in TREE_EXTENSIONS.items():
        root = ROOT / directory
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if extensions is None or path.suffix in extensions:
                selected.append(path)
    return sorted(set(selected), key=lambda path: path.relative_to(ROOT).as_posix())


digest = hashlib.sha256()
for path in paths():
    relative = path.relative_to(ROOT).as_posix().encode()
    digest.update(relative + b"\0")
    digest.update(path.read_bytes())
    digest.update(b"\0")
print(digest.hexdigest())
