import pytest

from src import celsius_to_fahrenheit, fahrenheit_to_celsius, miles_to_km
from src.conversions import (
    celsius_to_fahrenheit as celsius_to_fahrenheit_from_module,
)
from src.conversions import (
    fahrenheit_to_celsius as fahrenheit_to_celsius_from_module,
)
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


class TestCelsiusToFahrenheit:
    @pytest.mark.parametrize(
        ("celsius", "expected"),
        [
            (0, 32.0),
            (100, 212.0),
            (-40, -40.0),
            (37, 98.6),
        ],
    )
    def test_known_temperature_conversions_return_expected_values(self, celsius, expected):
        assert celsius_to_fahrenheit(celsius) == expected

    def test_decimal_input_is_rounded_to_two_decimals(self):
        assert celsius_to_fahrenheit(0.555) == 33.0

    def test_integer_input_returns_float(self):
        result = celsius_to_fahrenheit(10)
        assert isinstance(result, float)

    @pytest.mark.parametrize("invalid_value", ["abc", None, [], {}, True, False])
    def test_invalid_inputs_raise_value_error(self, invalid_value):
        with pytest.raises(ValueError):
            celsius_to_fahrenheit(invalid_value)

    def test_very_small_input_is_rounded_correctly(self):
        assert celsius_to_fahrenheit(0.001) == 32.0

    def test_very_large_input_returns_correctly_rounded_result(self):
        celsius = 1_000_000
        assert celsius_to_fahrenheit(celsius) == 1_800_032.0

    def test_function_is_importable_from_package_level(self):
        assert celsius_to_fahrenheit is celsius_to_fahrenheit_from_module


class TestFahrenheitToCelsius:
    @pytest.mark.parametrize(
        ("fahrenheit", "expected"),
        [
            (32, 0.0),
            (212, 100.0),
            (-40, -40.0),
            (98.6, 37.0),
        ],
    )
    def test_known_temperature_conversions_return_expected_values(self, fahrenheit, expected):
        assert fahrenheit_to_celsius(fahrenheit) == expected

    def test_decimal_input_is_rounded_to_two_decimals(self):
        assert fahrenheit_to_celsius(33) == 0.56

    def test_integer_input_returns_float(self):
        result = fahrenheit_to_celsius(50)
        assert isinstance(result, float)

    @pytest.mark.parametrize("invalid_value", ["abc", None, [], {}, True, False])
    def test_invalid_inputs_raise_value_error(self, invalid_value):
        with pytest.raises(ValueError):
            fahrenheit_to_celsius(invalid_value)

    def test_very_small_input_is_rounded_correctly(self):
        assert fahrenheit_to_celsius(32.001) == 0.0

    def test_very_large_input_returns_correctly_rounded_result(self):
        fahrenheit = 1_000_000
        assert fahrenheit_to_celsius(fahrenheit) == 555537.78

    def test_function_is_importable_from_package_level(self):
        assert fahrenheit_to_celsius is fahrenheit_to_celsius_from_module
