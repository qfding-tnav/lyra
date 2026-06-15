"""Conversion helper functions."""


def km_to_miles(km: float) -> float:
    """Convert kilometers to miles rounded to 4 decimal places."""
    return round(km * 0.621371, 4)
