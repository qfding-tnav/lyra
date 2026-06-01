import math

import pytest

from src.converter import ConversionError, UNIT_CATEGORIES, convert, get_categories, get_units


@pytest.mark.parametrize(
    ("unit", "expected_factor"),
    [
        ("millimeter", 0.001),
        ("centimeter", 0.01),
        ("meter", 1.0),
        ("kilometer", 1000.0),
        ("inch", 0.0254),
        ("foot", 0.3048),
        ("yard", 0.9144),
        ("mile", 1609.344),
    ],
)
def test_length_unit_factors_are_defined_relative_to_meters(unit, expected_factor):
    assert UNIT_CATEGORIES["length"].units[unit] == expected_factor


@pytest.mark.parametrize(
    ("value", "from_unit", "to_unit", "expected"),
    [
        (1500, "meter", "kilometer", 1.5),
        (1, "inch", "centimeter", 2.54),
        (1, "mile", "meter", 1609.344),
        (6, "foot", "yard", 2.0),
        (3.5, "kilometer", "mile", 2.174799476),
        (25, "millimeter", "inch", 0.9842519685),
    ],
)
def test_representative_length_conversions(value, from_unit, to_unit, expected):
    result = convert(value, "length", from_unit, to_unit)
    assert math.isclose(result, expected, rel_tol=1e-9, abs_tol=1e-9)


def test_same_unit_conversion_returns_original_value():
    assert convert(42.125, "length", "meter", "meter") == 42.125


@pytest.mark.parametrize("value", ["", None, "abc"])
def test_invalid_numeric_input_raises_error(value):
    with pytest.raises(ConversionError):
        convert(value, "length", "meter", "kilometer")


@pytest.mark.parametrize("value", [1e-12, 1e12])
def test_very_small_and_large_values_are_supported(value):
    result = convert(value, "length", "meter", "kilometer")
    assert math.isclose(result, value / 1000.0, rel_tol=1e-12, abs_tol=1e-18)


def test_length_category_is_available():
    categories = get_categories()
    assert categories["length"] == "Length"


def test_length_units_are_exposed_for_ui_selection():
    units = get_units("length")
    assert units == {
        "millimeter": "Millimeter (mm)",
        "centimeter": "Centimeter (cm)",
        "meter": "Meter (m)",
        "kilometer": "Kilometer (km)",
        "inch": "Inch (in)",
        "foot": "Foot (ft)",
        "yard": "Yard (yd)",
        "mile": "Mile (mi)",
    }


@pytest.mark.parametrize(
    ("category", "from_unit", "to_unit"),
    [
        ("weight", "meter", "kilometer"),
        ("length", "parsec", "meter"),
        ("length", "meter", "parsec"),
    ],
)
def test_unsupported_category_or_units_raise_error(category, from_unit, to_unit):
    with pytest.raises(ConversionError):
        convert(1, category, from_unit, to_unit)
