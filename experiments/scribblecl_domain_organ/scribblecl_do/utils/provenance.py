from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import os
import random

import numpy as np
import torch


def file_sha256(path: str | Path) -> str:
    h = sha256()
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(8 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def tree_sha256(root: str | Path) -> str:
    root = Path(root)
    h = sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file() and "__pycache__" not in p.parts):
        h.update(str(path.relative_to(root)).encode())
        h.update(bytes.fromhex(file_sha256(path)))
    return h.hexdigest()


def seed_everything(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
