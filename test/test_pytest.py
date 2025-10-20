import math
import pytest 
from src.bmi import calc_bmi, categorize_bmi, format_bmi, batch_bmi

@pytest.mark.parametrize("w,h,unit,expected", [
    (70, 1.75, "metric", 22.857142857),
    (60, 1.70, "metric", 20.761245674),
    (154, 69, "imperial", 22.739726027),
])
def test_calc_bmi_values(w, h, unit, expected):
    assert math.isclose(calc_bmi(w, h, unit), expected, rel_tol=1e-9)

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

def test_batch_mixed_rows():
    rows = [
        {"id": 1, "weight": 70, "height": 1.75},
        {"id": 2, "weight": "bad", "height": 1.75},
    ]
    out = batch_bmi(rows, unit="metric")
    assert out[0]["category"] == "Normal"
    assert "error" in out[1]
