"""Conversion helper utilities."""


def _validate_numeric_input(value: float) -> float:
    """Validate a numeric input and return it as a float.

    Raises:
        ValueError: If the provided value is not numeric.
    """
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError("Value must be a numeric type.")
    return float(value)


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit, rounded to 2 decimals.

    Raises:
        ValueError: If celsius is not numeric.
    """
    validated_celsius = _validate_numeric_input(celsius)
    result = validated_celsius * 9 / 5 + 32
    return round(result, 2)


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert Fahrenheit to Celsius, rounded to 2 decimals.

    Raises:
        ValueError: If fahrenheit is not numeric.
    """
    validated_fahrenheit = _validate_numeric_input(fahrenheit)
    result = (validated_fahrenheit - 32) * 5 / 9
    return round(result, 2)


def kilograms_to_pounds(kilograms: float) -> float:
    """Convert kilograms to pounds, rounded to 2 decimals.

    Raises:
        ValueError: If kilograms is not numeric.
    """
    validated_kilograms = _validate_numeric_input(kilograms)
    result = validated_kilograms * 2.20462
    return round(result, 2)


def miles_to_km(miles: float) -> float:
    """Convert miles to kilometers rounded to 3 decimals."""
    result = miles * 1.60934
    return round(result, 3)
