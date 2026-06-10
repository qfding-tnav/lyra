"""Length conversion utilities powered by Pint."""

from __future__ import annotations

from numbers import Real

from pint import DimensionalityError, UndefinedUnitError, UnitRegistry

ureg = UnitRegistry()


class LengthConversionError(ValueError):
    """Base exception for length conversion errors."""


class InvalidValueError(LengthConversionError):
    """Raised when the provided value is not numeric."""


class InvalidUnitError(LengthConversionError):
    """Raised when a provided unit is missing or unsupported."""


class InvalidDimensionError(LengthConversionError):
    """Raised when a provided unit is not a length unit."""


def _validate_numeric_value(value: Real) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise InvalidValueError("value must be a numeric type")
    return float(value)


def _validate_unit_name(unit: str, field_name: str):
    if not isinstance(unit, str) or not unit.strip():
        raise InvalidUnitError(f"{field_name} must be a non-empty string")

    normalized_unit = unit.strip()

    try:
        parsed_unit = ureg.parse_units(normalized_unit)
    except UndefinedUnitError as exc:
        raise InvalidUnitError(f"unsupported unit: {normalized_unit}") from exc

    if parsed_unit.dimensionality != ureg.meter.dimensionality:
        raise InvalidDimensionError(
            f"{field_name} must be a length unit, got: {normalized_unit}"
        )

    return parsed_unit


def convert_length(value: Real, from_unit: str, to_unit: str) -> float:
    """Convert a numeric value from one length unit to another.

    Args:
        value: The numeric magnitude to convert.
        from_unit: The source length unit.
        to_unit: The target length unit.

    Returns:
        The converted numeric value as a float.

    Raises:
        InvalidValueError: If ``value`` is not numeric.
        InvalidUnitError: If either unit string is missing or unsupported.
        InvalidDimensionError: If either unit is not a length unit.
    """

    numeric_value = _validate_numeric_value(value)
    source_unit = _validate_unit_name(from_unit, "from_unit")
    target_unit = _validate_unit_name(to_unit, "to_unit")

    quantity = numeric_value * source_unit

    try:
        converted = quantity.to(target_unit)
    except DimensionalityError as exc:
        raise InvalidDimensionError(
            f"cannot convert from {from_unit!r} to {to_unit!r}"
        ) from exc

    return float(converted.magnitude)
