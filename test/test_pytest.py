# test/test_pytest.py

import math
import pytest
from src.bmi import calc_bmi, categorize_bmi, format_bmi, batch_bmi

@pytest.mark.parametrize("w,h,unit,expected", [
    (70, 1.75, "metric", 22.857142857),
    (60, 1.70, "metric", 20.761245674),
    # Corrected expected for imperial case:
    (154, 69, "imperial", 22.73934047469019),
])
def test_calc_bmi_values(w, h, unit, expected):
    # Floating-point math varies slightly across platforms; use absolute tolerance.
    assert math.isclose(calc_bmi(w, h, unit), expected, rel_tol=0.0, abs_tol=1e-9)

def test_imperial_tolerance():
    bmi = calc_bmi(154, 69, "imperial")
    # Keep an absolute tolerance for consistency across Python builds.
    assert math.isclose(bmi, 22.73934047469019, rel_tol=0.0, abs_tol=1e-9)

@pytest.mark.parametrize("bmi,cat", [
    (18.49, "Underweight"),
    (18.50, "Normal"),
    (24.99, "Normal"),
    (25.00, "Overweight"),
    (29.99, "Overweight"),
    (30.00, "Obesity"),
])
def test_categorize_edges(bmi, cat):
    assert categorize_bmi(bmi) == cat

def test_format_bmi_default_and_custom():
    assert format_bmi(22.857142857) == "22.86"
    assert format_bmi(22.857142857, decimals=3) == "22.857"

@pytest.mark.parametrize("w,h,unit", [
    (0, 1.75, "metric"),
    (70, 0, "metric"),
    ("x", 1.75, "metric"),
    (70, 1.75, "foo"),
])
def test_invalid_inputs(w, h, unit):
    with pytest.raises(ValueError):
        calc_bmi(w, h, unit)

@pytest.mark.parametrize("w,h", [
    (True, 1.75),   # bools should be rejected
    (70, False),
])
def test_bool_inputs_rejected(w, h):
    with pytest.raises(ValueError):
        calc_bmi(w, h, "metric")

@pytest.mark.parametrize("decimals", [-1, 2.5, "2"])
def test_format_bmi_bad_decimals(decimals):
    with pytest.raises(ValueError):
        format_bmi(22.8, decimals=decimals)

def test_batch_mixed_rows_and_missing():
    rows = [
        {"id": 1, "weight": 70, "height": 1.75},
        {"id": 2, "weight": "bad", "height": 1.75},
        {"id": 3, "weight": 70},               # missing height
        {"id": 4, "height": 1.75},             # missing weight
    ]
    out = batch_bmi(rows, unit="metric")
    assert out[0]["category"] == "Normal"
    assert "error" in out[1]
    assert "error" in out[2]
    assert "error" in out[3]
