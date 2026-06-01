from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class UnitCategory:
    name: str
    base_unit: str
    units: Dict[str, float]
    labels: Dict[str, str]


UNIT_CATEGORIES: Dict[str, UnitCategory] = {
    "length": UnitCategory(
        name="Length",
        base_unit="meter",
        units={
            "millimeter": 0.001,
            "centimeter": 0.01,
            "meter": 1.0,
            "kilometer": 1000.0,
            "inch": 0.0254,
            "foot": 0.3048,
            "yard": 0.9144,
            "mile": 1609.344,
        },
        labels={
            "millimeter": "Millimeter (mm)",
            "centimeter": "Centimeter (cm)",
            "meter": "Meter (m)",
            "kilometer": "Kilometer (km)",
            "inch": "Inch (in)",
            "foot": "Foot (ft)",
            "yard": "Yard (yd)",
            "mile": "Mile (mi)",
        },
    )
}


class ConversionError(ValueError):
    pass


def get_categories() -> Dict[str, str]:
    return {key: category.name for key, category in UNIT_CATEGORIES.items()}



def get_units(category: str) -> Dict[str, str]:
    unit_category = UNIT_CATEGORIES.get(category)
    if not unit_category:
        raise ConversionError(f"Unsupported category: {category}")
    return unit_category.labels



def convert(value: float | int | str, category: str, from_unit: str, to_unit: str) -> float:
    if value is None or value == "":
        raise ConversionError("A numeric value is required")

    try:
        numeric_value = float(value)
    except (TypeError, ValueError) as exc:
        raise ConversionError("Invalid numeric input") from exc

    unit_category = UNIT_CATEGORIES.get(category)
    if not unit_category:
        raise ConversionError(f"Unsupported category: {category}")

    if from_unit not in unit_category.units:
        raise ConversionError(f"Unsupported source unit: {from_unit}")
    if to_unit not in unit_category.units:
        raise ConversionError(f"Unsupported target unit: {to_unit}")

    if from_unit == to_unit:
        return numeric_value

    value_in_base = numeric_value * unit_category.units[from_unit]
    converted_value = value_in_base / unit_category.units[to_unit]
    return converted_value
