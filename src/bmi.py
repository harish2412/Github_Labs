from __future__ import annotations
from typing import Iterable, Dict, Any, List

_METRIC_MAX_HEIGHT_M = 2.7    # tallest human ever was ~2.72 m
_METRIC_MAX_WEIGHT_KG = 700.0 # extreme upper bound

def _ensure_number(x, name: str):
    if not isinstance(x, (int, float)):
        raise ValueError(f"{name} must be numeric")

def validate_inputs(weight: float, height: float, unit: str = "metric") -> None:
    """
    Validate basic sanity for weight and height given unit system.
    Metric: weight in kg, height in meters.
    Imperial: weight in pounds, height in inches.
    """
    if unit not in {"metric", "imperial"}:
        raise ValueError("unit must be 'metric' or 'imperial'")

    _ensure_number(weight, "weight")
    _ensure_number(height, "height")

    if weight <= 0 or height <= 0:
        raise ValueError("weight and height must be > 0")

    if unit == "metric":
        if height > _METRIC_MAX_HEIGHT_M or weight > _METRIC_MAX_WEIGHT_KG:
            # Loose caps to catch obvious unit mistakes (e.g., cm instead of m).
            raise ValueError("unreasonable metric inputs: check units (m, kg)")
    else:
        # Rough imperial sanity limits
        if height > 107.0 or weight > 1540.0:  # 107in=8'11", 1540lb ~700kg
            raise ValueError("unreasonable imperial inputs: check units (in, lb)")

def calc_bmi(weight: float, height: float, unit: str = "metric") -> float:
    """
    Calculate BMI.
    - metric: BMI = kg / m^2
    - imperial: BMI = (lb / in^2) * 703
    """
    validate_inputs(weight, height, unit)
    if unit == "metric":
        return weight / (height ** 2)
    return (weight / (height ** 2)) * 703.0

def categorize_bmi(bmi: float) -> str:
    """
    CDC/WHO standard categories:
    - <18.5: Underweight
    - 18.5–24.9: Normal
    - 25.0–29.9: Overweight
    - >=30.0: Obesity
    """
    _ensure_number(bmi, "bmi")
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25.0:
        return "Normal"
    if bmi < 30.0:
        return "Overweight"
    return "Obesity"

def format_bmi(bmi: float, decimals: int = 2) -> str:
    _ensure_number(bmi, "bmi")
    if not isinstance(decimals, int) or decimals < 0:
        raise ValueError("decimals must be a non-negative integer")
    return f"{bmi:.{decimals}f}"

def batch_bmi(rows: Iterable[Dict[str, Any]], unit: str = "metric") -> List[Dict[str, Any]]:
    """
    Compute BMI for many rows. Each row needs 'weight' and 'height'.
    Returns rows augmented with 'bmi' and 'category', or an 'error' string.
    """
    out: List[Dict[str, Any]] = []
    for r in rows:
        w, h = r.get("weight"), r.get("height")
        try:
            bmi_val = calc_bmi(w, h, unit=unit)
            out.append({**r, "bmi": bmi_val, "category": categorize_bmi(bmi_val)})
        except Exception as e:
            out.append({**r, "error": str(e)})
    return out