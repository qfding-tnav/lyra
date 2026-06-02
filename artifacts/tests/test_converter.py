import math
import unittest

from artifacts.src.converter import (
    ConversionError,
    UnitConverter,
    convert,
    format_value,
    get_categories,
    get_units,
    parse_value,
)


class ConverterTests(unittest.TestCase):
    def test_area_category_is_available(self):
        self.assertIn("area", get_categories())

    def test_area_units_are_available(self):
        unit_keys = [unit.key for unit in get_units("area")]
        self.assertEqual(
            unit_keys,
            [
                "square_meter",
                "square_kilometer",
                "square_centimeter",
                "square_millimeter",
                "square_foot",
                "square_inch",
                "square_yard",
                "acre",
                "hectare",
            ],
        )

    def test_area_conversion_square_meter_to_square_foot(self):
        result = convert("area", 1, "square_meter", "square_foot")
        self.assertTrue(math.isclose(result, 10.763910416709722, rel_tol=1e-12))

    def test_area_conversion_acre_to_square_meter(self):
        result = convert("area", 1, "acre", "square_meter")
        self.assertTrue(math.isclose(result, 4046.8564224, rel_tol=1e-12))

    def test_area_conversion_hectare_to_acre(self):
        result = convert("area", 1, "hectare", "acre")
        self.assertTrue(math.isclose(result, 2.471053814671653, rel_tol=1e-12))

    def test_area_conversion_square_centimeter_to_square_meter(self):
        result = convert("area", 10000, "square_centimeter", "square_meter")
        self.assertEqual(result, 1)

    def test_empty_input_returns_none(self):
        self.assertIsNone(convert("area", "", "square_meter", "square_foot"))

    def test_non_numeric_input_raises_error(self):
        with self.assertRaises(ConversionError):
            parse_value("abc")

    def test_infinite_input_raises_error(self):
        with self.assertRaises(ConversionError):
            parse_value(float("inf"))

    def test_negative_values_are_supported(self):
        result = convert("area", -2.5, "square_meter", "square_foot")
        self.assertLess(result, 0)

    def test_format_value_handles_none(self):
        self.assertEqual(format_value(None), "")

    def test_unit_converter_switches_to_area_and_resets(self):
        converter = UnitConverter()
        converter.set_input("42")
        converter.set_category("area")
        self.assertEqual(converter.category, "area")
        self.assertEqual(converter.input_value, "")
        self.assertEqual(converter.from_unit, "square_meter")
        self.assertEqual(converter.to_unit, "square_kilometer")

    def test_unit_converter_swap_and_output(self):
        converter = UnitConverter()
        converter.set_category("area")
        converter.set_input("1")
        converter.from_unit = "square_meter"
        converter.to_unit = "square_foot"
        self.assertEqual(converter.get_output(), "10.76391")
        converter.swap_units()
        self.assertEqual(converter.from_unit, "square_foot")
        self.assertEqual(converter.to_unit, "square_meter")


if __name__ == "__main__":
    unittest.main()
