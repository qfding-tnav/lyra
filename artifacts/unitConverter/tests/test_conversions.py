import pytest

from src import celsius_to_fahrenheit


@pytest.mark.parametrize(
    ("celsius", "expected"),
    [
        (0, 32.0),
        (100, 212.0),
        (25, 77.0),
        (37.5, 99.5),
    ],
)
def test_celsius_to_fahrenheit_positive_cases(celsius, expected):
    assert celsius_to_fahrenheit(celsius) == expected


@pytest.mark.parametrize(
    ("celsius", "expected"),
    [
        (-40, -40.0),
        (-273.15, -459.67),
    ],
)
def test_celsius_to_fahrenheit_negative_and_boundary_values(celsius, expected):
    assert celsius_to_fahrenheit(celsius) == expected


@pytest.mark.parametrize(
    ("celsius", "expected"),
    [
        (0.001, round(0.001 * 9 / 5 + 32, 2)),
        (1e10, round(1e10 * 9 / 5 + 32, 2)),
        (0.5555555556, round(0.5555555556 * 9 / 5 + 32, 2)),
    ],
)
def test_celsius_to_fahrenheit_rounding_and_large_input_regression(celsius, expected):
    assert celsius_to_fahrenheit(celsius) == expected


def test_celsius_to_fahrenheit_returns_float_for_integer_input():
    result = celsius_to_fahrenheit(0)
    assert isinstance(result, float)
