"""Area conversion utilities."""

from __future__ import annotations

from numbers import Real


_UNIT_TO_SQUARE_METER = {
    "square_meter": 1.0,
    "m2": 1.0,
    "square_centimeter": 0.0001,
    "cm2": 0.0001,
    "square_kilometer": 1_000_000.0,
    "km2": 1_000_000.0,
    "square_foot": 0.09290304,
    "ft2": 0.09290304,
    "square_inch": 0.00064516,
    "in2": 0.00064516,
    "acre": 4046.8564224,
    "hectare": 10_000.0,
}


SUPPORTED_UNITS = tuple(sorted(_UNIT_TO_SQUARE_METER.keys()))


def _validate_numeric_value(value: Real) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError("value must be a real number")
    return float(value)



def _validate_unit(unit: str, argument_name: str) -> str:
    if not isinstance(unit, str) or not unit.strip():
        raise TypeError(f"{argument_name} must be a non-empty string")

    normalized = unit.strip().lower()
    if normalized not in _UNIT_TO_SQUARE_METER:
        raise ValueError(
            f"Unsupported area unit '{unit}'. Supported units: {', '.join(SUPPORTED_UNITS)}"
        )
    return normalized



def convert_area(value: Real, from_unit: str, to_unit: str) -> float:
    """Convert an area value from one supported unit to another."""
    numeric_value = _validate_numeric_value(value)
    source_unit = _validate_unit(from_unit, "from_unit")
    target_unit = _validate_unit(to_unit, "to_unit")

    if source_unit == target_unit:
        return numeric_value

    value_in_square_meters = numeric_value * _UNIT_TO_SQUARE_METER[source_unit]
    return value_in_square_meters / _UNIT_TO_SQUARE_METER[target_unit]
