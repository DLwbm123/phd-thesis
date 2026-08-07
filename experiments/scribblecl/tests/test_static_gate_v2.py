import math

from scribblecl.gate import (
    checkpoint_selection_score,
    class_value,
    compare_validations,
)


def validation(per_class, bg_fraction=0.9, foreground_fraction=0.1):
    return {
        "epoch": 3,
        "benchmark_mean_bg_included": sum(per_class.values()) / 4,
        "background_patient_dice": per_class.get(0, per_class.get("0")),
        "foreground_patient_mean": sum(class_value(per_class, k) for k in (1, 2, 3)) / 3,
        "patient_per_class": per_class,
        "background_fraction": bg_fraction,
        "foreground_fraction": foreground_fraction,
        "nonempty_prediction_rate": {1: 0.5, 2: 0.5, 3: 0.5},
    }


def test_gate_accepts_integer_class_keys():
    previous = validation({0: 0.99, 1: 0.6, 2: 0.6, 3: 0.6})
    current = validation({0: 0.99, 1: 0.59, 2: 0.59, 3: 0.59})
    assert compare_validations(previous, current, "integer")["decision"] == "PASS"
    assert class_value(current["patient_per_class"], 1) == 0.59


def test_gate_accepts_json_string_class_keys():
    previous = validation({"0": 0.99, "1": 0.6, "2": 0.6, "3": 0.6})
    current = validation({"0": 0.99, "1": 0.59, "2": 0.59, "3": 0.59})
    current["nonempty_prediction_rate"] = {"1": 0.5, "2": 0.5, "3": 0.5}
    assert compare_validations(previous, current, "strings")["decision"] == "PASS"


def test_checkpoint_selection_uses_foreground_mean():
    record = validation({0: 0.999, 1: 0.3, 2: 0.3, 3: 0.3})
    assert checkpoint_selection_score(record) == 0.3
    assert record["benchmark_mean_bg_included"] > checkpoint_selection_score(record)


def test_high_background_cannot_hide_foreground_collapse():
    previous = validation({0: 0.99, 1: 0.6, 2: 0.6, 3: 0.6})
    current = validation({0: 0.9999, 1: 0.1, 2: 0.1, 3: 0.1})
    result = compare_validations(previous, current, "collapse")
    assert result["decision"] == "STOP"
    assert result["current_bg_included_mean"] > 0.3
    assert math.isclose(result["current_foreground_mean"], 0.1)
    assert any("foreground_mean_drop" in reason for reason in result["failure_reasons"])
