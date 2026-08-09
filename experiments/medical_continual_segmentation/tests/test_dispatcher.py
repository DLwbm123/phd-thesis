from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SPEC = spec_from_file_location("core_dispatcher", ROOT / "scripts" / "dispatch_core_experiments.py")
dispatcher = module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = dispatcher
SPEC.loader.exec_module(dispatcher)


def test_run_id_matching_does_not_confuse_superseded_prefix():
    command = "python main.py --run-id medseg_class_pce_ft_seed42_final --device cuda:0"
    assert dispatcher.process_matches_run(command, "medseg_class_pce_ft_seed42_final")
    assert not dispatcher.process_matches_run(command, "medseg_class_pce_ft_seed42")


def test_reference_plan_is_exactly_ten_additional_tasks():
    references = [job for job in dispatcher.core_jobs() if job.priority == "P3"]
    assert len(references) == 10
    assert {job.scenario for job in references} == {"class", "domain", "organ"}
    assert all(job.method == "pce_ft" and job.independent_task for job in references)


def test_only_core_methods_are_schedulable():
    assert {job.method for job in dispatcher.core_jobs()} == {"pce_ft", "pce_ewc"}
