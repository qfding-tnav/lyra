"""Length conversion utilities."""

UNIT_TO_METERS = {
    "m": 1.0,
    "km": 1000.0,
    "mile": 1609.344,
    "ft": 0.3048,
}


def convert_length(value: float, from_unit: str, to_unit: str) -> float:
    """Convert a length value between supported units.

    Supported units are meters ("m"), kilometers ("km"), miles ("mile"),
    and feet ("ft").
    """
    if from_unit not in UNIT_TO_METERS:
        raise ValueError(f"Unsupported from_unit: {from_unit}")
    if to_unit not in UNIT_TO_METERS:
        raise ValueError(f"Unsupported to_unit: {to_unit}")

    value_in_meters = value * UNIT_TO_METERS[from_unit]
    return value_in_meters / UNIT_TO_METERS[to_unit]
