"""Conversion helper utilities."""


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert a Celsius temperature to Fahrenheit rounded to 2 decimals."""
    result = celsius * 9 / 5 + 32
    return round(result, 2)
