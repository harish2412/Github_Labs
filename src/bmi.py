from __future__ import annotations
from typing import Iterable, Mapping, Dict, Any, List
from numbers import Real

__all__ = ["validate_inputs","calc_bmi","categorize_bmi","format_bmi","batch_bmi"]

_METRIC_MAX_HEIGHT_M = 2.7
_METRIC_MAX_WEIGHT_KG = 700.0
_IMPERIAL_FACTOR = 703.0

def _ensure_number(x: Any, name: str) -> None:
    if isinstance(x, bool) or not isinstance(x, Real):
        raise ValueError(f"{name} must be numeric")

def validate_inputs(weight: float, height: float, unit: str = "metric") -> None:
    if unit not in {"metric", "imperial"}:
        raise ValueError("unit must be 'metric' or 'imperial'")
    _ensure_number(weight, "weight"); _ensure_number(height, "height")
    if weight <= 0 or height <= 0:
        raise ValueError("weight and height must be > 0")
    if unit == "metric":
        if height > _METRIC_MAX_HEIGHT_M or weight > _METRIC_MAX_WEIGHT_KG:
            raise ValueError("unreasonable metric inputs: check units (m, kg)")
    else:
        if height > 107.0 or weight > 1540.0:
            raise ValueError("unreasonable imperial inputs: check units (in, lb)")

def calc_bmi(weight: float, height: float, unit: str = "metric") -> float:
    validate_inputs(weight, height, unit)
    h2 = height * height
    return weight / h2 if unit == "metric" else (weight / h2) * _IMPERIAL_FACTOR

def categorize_bmi(bmi: float) -> str:
    _ensure_number(bmi, "bmi")
    if bmi < 18.5: return "Underweight"
    if bmi < 25.0: return "Normal"
    if bmi < 30.0: return "Overweight"
    return "Obesity"

def format_bmi(bmi: float, decimals: int = 2) -> str:
    _ensure_number(bmi, "bmi")
    if not isinstance(decimals, int) or decimals < 0:
        raise ValueError("decimals must be a non-negative integer")
    return f"{bmi:.{decimals}f}"

def batch_bmi(rows: Iterable[Mapping[str, Any]], unit: str = "metric") -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for r in rows:
        w = r.get("weight"); h = r.get("height")
        try:
            if w is None or h is None:
                raise ValueError("missing 'weight' or 'height'")
            bmi = calc_bmi(w, h, unit=unit)
            out.append({**dict(r), "bmi": bmi, "category": categorize_bmi(bmi)})
        except Exception as e:
            out.append({**dict(r), "error": str(e)})
    return out
