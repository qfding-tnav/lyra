import pytest

from src.length_converter import convert_length


def test_convert_kilometers_to_meters_exact():
    assert convert_length(1, "km", "m") == 1000


def test_convert_mile_to_kilometer_approximately():
    assert convert_length(1, "mile", "km") == pytest.approx(1.609344, abs=1e-9)


def test_convert_feet_to_meters_approximately():
    assert convert_length(1, "ft", "m") == pytest.approx(0.3048, abs=1e-9)


def test_identity_conversion_meters():
    assert convert_length(5, "m", "m") == 5


def test_identity_conversion_miles():
    assert convert_length(2.5, "mile", "mile") == 2.5


def test_convert_meters_to_kilometers():
    assert convert_length(2500, "m", "km") == pytest.approx(2.5, abs=1e-9)


def test_convert_meters_to_feet():
    assert convert_length(1, "m", "ft") == pytest.approx(3.280839895013123, abs=1e-9)


def test_convert_kilometers_to_miles():
    assert convert_length(1, "km", "mile") == pytest.approx(0.621371192237334, abs=1e-9)


def test_zero_value_conversion():
    assert convert_length(0, "m", "km") == 0


def test_negative_value_converts_mathematically():
    assert convert_length(-1, "km", "m") == -1000


def test_decimal_input_value_conversion():
    assert convert_length(1.2345, "km", "m") == pytest.approx(1234.5, abs=1e-9)


def test_unsupported_source_unit_raises_value_error():
    with pytest.raises(ValueError, match=r"Unsupported from_unit: yard"):
        convert_length(1, "yard", "m")


def test_unsupported_target_unit_raises_value_error():
    with pytest.raises(ValueError, match=r"Unsupported to_unit: yard"):
        convert_length(1, "m", "yard")


def test_both_unsupported_units_raise_value_error_for_source_first():
    with pytest.raises(ValueError, match=r"Unsupported from_unit: yard"):
        convert_length(1, "yard", "parsec")
