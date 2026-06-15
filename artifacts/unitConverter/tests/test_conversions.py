import pytest

from src import celsius_to_fahrenheit, miles_to_km
from src.conversions import miles_to_km as miles_to_km_from_module


class TestMilesToKm:
    def test_zero_miles_returns_zero_point_zero(self):
        assert miles_to_km(0) == 0.0

    def test_one_mile_returns_expected_rounded_kilometers(self):
        assert miles_to_km(1) == 1.609

    @pytest.mark.parametrize(
        ("miles", "expected"),
        [
            (5, 8.047),
            (10, 16.093),
            (2.5, 4.023),
        ],
    )
    def test_common_inputs_return_expected_values(self, miles, expected):
        assert miles_to_km(miles) == expected

    def test_integer_input_returns_float(self):
        result = miles_to_km(3)
        assert isinstance(result, float)

    def test_negative_input_converts_and_rounds_mathematically(self):
        assert miles_to_km(-1) == -1.609

    def test_very_small_input_rounds_to_three_decimals(self):
        assert miles_to_km(0.0001) == 0.0

    def test_value_with_more_than_three_decimals_is_rounded_correctly(self):
        assert miles_to_km(1.2345) == round(1.2345 * 1.60934, 3)

    def test_very_large_input_returns_correctly_rounded_result(self):
        miles = 1_000_000
        assert miles_to_km(miles) == 1_609_340.0

    def test_function_is_importable_from_package_level(self):
        assert miles_to_km is miles_to_km_from_module


class TestCelsiusToFahrenheitRegression:
    @pytest.mark.parametrize(
        ("celsius", "expected"),
        [
            (0, 32.0),
            (100, 212.0),
            (-40, -40.0),
            (37, 98.6),
        ],
    )
    def test_existing_conversion_behavior_remains_unchanged(self, celsius, expected):
        assert celsius_to_fahrenheit(celsius) == expected
