from __future__ import annotations
from hashlib import sha256
from pathlib import Path
import random
import numpy as np
import torch


def file_sha256(path):
    h=sha256()
    with open(path,"rb") as stream:
        for chunk in iter(lambda:stream.read(8<<20),b""): h.update(chunk)
    return h.hexdigest()


def tree_sha256(root):
    root=Path(root); h=sha256()
    excluded={"__pycache__",".pytest_cache","runs","reports","results","private_provenance"}
    def included(path):
        parts=path.relative_to(root).parts
        return not excluded.intersection(parts) and not (parts and parts[0].startswith("runs"))
    for p in sorted(x for x in root.rglob("*") if x.is_file() and included(x)): h.update(str(p.relative_to(root)).encode()); h.update(bytes.fromhex(file_sha256(p)))
    return h.hexdigest()


def seed_all(seed):
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
    if torch.cuda.is_available(): torch.cuda.manual_seed_all(seed)
