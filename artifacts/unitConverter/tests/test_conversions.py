import os
import sys


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from conversions import km_to_miles


def test_km_to_miles_one_kilometer_returns_expected_value():
    assert km_to_miles(1.0) == 0.6214


def test_km_to_miles_zero_returns_zero():
    assert km_to_miles(0.0) == 0.0


def test_km_to_miles_typical_positive_value_is_correctly_rounded():
    assert km_to_miles(5.0) == 3.1069


def test_km_to_miles_negative_value_returns_negative_converted_result():
    assert km_to_miles(-1.0) == -0.6214


def test_km_to_miles_very_small_decimal_rounds_to_four_places():
    assert km_to_miles(0.0001) == 0.0001


def test_km_to_miles_large_value_preserves_correct_multiplication_and_rounding():
    assert km_to_miles(123456.789) == 76712.4683


def test_km_to_miles_rounds_half_up_at_fourth_decimal_boundary():
    assert km_to_miles(1.00004) == 0.6214


def test_km_to_miles_returns_float_type():
    assert isinstance(km_to_miles(2.0), float)
