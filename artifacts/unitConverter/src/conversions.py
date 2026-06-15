"""Conversion helper utilities."""


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert a Celsius temperature to Fahrenheit rounded to 2 decimals."""
    result = celsius * 9 / 5 + 32
    return round(result, 2)


def miles_to_km(miles: float) -> float:
    """Convert miles to kilometers rounded to 3 decimals."""
    result = miles * 1.60934
    return round(result, 3)
