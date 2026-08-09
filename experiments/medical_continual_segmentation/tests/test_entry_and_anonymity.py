from pathlib import Path
import re
import subprocess
import sys

import pytest

from medcl.trainers import dry_run

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = re.compile("|".join(("Scribble"+"CL","scribble"+"cl","Z"+"ScribbleSeg","z"+"scribble","wang"+"bomin","bomin"+"wang")),re.IGNORECASE)


def test_main_entry_is_main_py():
    assert (ROOT / "main.py").is_file()
    assert not any((ROOT / name).exists() for name in ("run.py", "train.py", "run_class.py", "run_domain.py", "run_organ.py", "scripts/run_pilot.py"))


def test_all_scenarios_route_through_main():
    text=(ROOT/"main.py").read_text(); assert 'SCENARIOS = ("class", "domain", "organ")' in text


def test_runtime_tree_is_anonymous():
    roots=[ROOT/"main.py",ROOT/"medcl",ROOT/"configs",ROOT/"scripts",ROOT/"tests",ROOT/"runs",ROOT/"README.md"]
    hits=[]
    for root in roots:
        paths=[root] if root.is_file() else [p for p in root.rglob("*") if p.is_file() and "__pycache__" not in p.parts]
        for path in paths:
            if FORBIDDEN.search(str(path.relative_to(ROOT))) or FORBIDDEN.search(path.read_text(errors="ignore")): hits.append(str(path))
    assert hits == []


def test_cli_help_is_anonymous():
    value=subprocess.run([sys.executable,str(ROOT/"main.py"),"--help"],capture_output=True,text=True,check=True).stdout
    assert FORBIDDEN.search(value) is None


def test_run_ids_are_anonymous():
    text=(ROOT/"medcl/trainers/engine.py").read_text(); assert "medseg_" in text; assert FORBIDDEN.search(text) is None


@pytest.mark.parametrize("method",["enhanced_ft","enhanced_ewc","enhanced_si"])
def test_enhanced_methods_are_blocked(method):
    with pytest.raises(RuntimeError,match="blocked_by_static_gate"): dry_run("domain",method)
