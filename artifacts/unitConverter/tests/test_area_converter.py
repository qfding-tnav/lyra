import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from src.area_converter import convert_area, SUPPORTED_UNITS


def test_supported_units_include_expected_core_units():
    expected = {
        'square_meter', 'm2', 'square_centimeter', 'cm2', 'square_kilometer', 'km2',
        'square_foot', 'ft2', 'square_inch', 'in2', 'acre', 'hectare'
    }
    assert expected.issubset(set(SUPPORTED_UNITS))


def test_square_meter_to_square_centimeter():
    assert convert_area(1, 'square_meter', 'square_centimeter') == 10000.0


def test_square_kilometer_to_square_meter():
    assert convert_area(1, 'square_kilometer', 'square_meter') == 1_000_000.0


def test_same_unit_no_op():
    assert convert_area(12.5, 'm2', 'm2') == 12.5


def test_fractional_value_conversion():
    assert math.isclose(convert_area(0.5, 'hectare', 'square_meter'), 5000.0)


def test_alias_conversion():
    assert math.isclose(convert_area(10, 'ft2', 'square_meter'), 0.9290304)


def test_unsupported_from_unit_raises_value_error():
    with pytest.raises(ValueError, match='Unsupported area unit'):
        convert_area(1, 'yard2', 'm2')


def test_unsupported_to_unit_raises_value_error():
    with pytest.raises(ValueError, match='Unsupported area unit'):
        convert_area(1, 'm2', 'yard2')


def test_non_numeric_value_raises_type_error():
    with pytest.raises(TypeError, match='value must be a real number'):
        convert_area('abc', 'm2', 'cm2')


def test_bool_value_raises_type_error():
    with pytest.raises(TypeError, match='value must be a real number'):
        convert_area(True, 'm2', 'cm2')


def test_blank_unit_raises_type_error():
    with pytest.raises(TypeError, match='must be a non-empty string'):
        convert_area(1, '   ', 'cm2')
