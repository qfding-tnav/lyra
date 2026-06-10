import math
import unittest

from src.length_converter import (
    InvalidDimensionError,
    InvalidUnitError,
    InvalidValueError,
    convert_length,
)


class ConvertLengthPositiveTests(unittest.TestCase):
    def test_converts_meters_to_centimeters(self):
        self.assertEqual(convert_length(1, "meter", "centimeter"), 100.0)

    def test_converts_kilometers_to_meters(self):
        self.assertEqual(convert_length(2, "kilometer", "meter"), 2000.0)

    def test_converts_inches_to_feet(self):
        self.assertEqual(convert_length(12, "inch", "foot"), 1.0)

    def test_converts_miles_to_kilometers(self):
        self.assertTrue(
            math.isclose(
                convert_length(3, "mile", "kilometer"),
                4.828032,
                rel_tol=0.0,
                abs_tol=1e-12,
            )
        )

    def test_returns_same_value_for_same_units(self):
        self.assertEqual(convert_length(42, "meter", "meter"), 42.0)

    def test_accepts_float_input(self):
        self.assertEqual(convert_length(2.5, "kilometer", "meter"), 2500.0)


class ConvertLengthNegativeTests(unittest.TestCase):
    def test_rejects_string_value(self):
        with self.assertRaisesRegex(InvalidValueError, "value must be a numeric type"):
            convert_length("10", "meter", "centimeter")

    def test_rejects_none_value(self):
        with self.assertRaisesRegex(InvalidValueError, "value must be a numeric type"):
            convert_length(None, "meter", "centimeter")

    def test_rejects_boolean_value(self):
        with self.assertRaisesRegex(InvalidValueError, "value must be a numeric type"):
            convert_length(True, "meter", "centimeter")

    def test_rejects_empty_from_unit(self):
        with self.assertRaisesRegex(InvalidUnitError, "from_unit must be a non-empty string"):
            convert_length(1, "", "meter")

    def test_rejects_empty_to_unit(self):
        with self.assertRaisesRegex(InvalidUnitError, "to_unit must be a non-empty string"):
            convert_length(1, "meter", "   ")

    def test_rejects_unknown_from_unit(self):
        with self.assertRaisesRegex(InvalidUnitError, "unsupported unit: meterss"):
            convert_length(1, "meterss", "meter")

    def test_rejects_unknown_to_unit(self):
        with self.assertRaisesRegex(InvalidUnitError, "unsupported unit: centimetr"):
            convert_length(1, "meter", "centimetr")

    def test_rejects_non_length_from_unit(self):
        with self.assertRaisesRegex(
            InvalidDimensionError,
            "from_unit must be a length unit, got: second",
        ):
            convert_length(1, "second", "meter")

    def test_rejects_non_length_to_unit(self):
        with self.assertRaisesRegex(
            InvalidDimensionError,
            "to_unit must be a length unit, got: kilogram",
        ):
            convert_length(1, "meter", "kilogram")


class ConvertLengthBoundaryAndRegressionTests(unittest.TestCase):
    def test_converts_zero_value(self):
        self.assertEqual(convert_length(0, "meter", "centimeter"), 0.0)

    def test_converts_negative_value(self):
        self.assertEqual(convert_length(-3, "meter", "centimeter"), -300.0)

    def test_converts_very_large_value(self):
        self.assertEqual(convert_length(1e12, "kilometer", "meter"), 1e15)

    def test_converts_very_small_value(self):
        self.assertTrue(
            math.isclose(
                convert_length(1e-12, "meter", "nanometer"),
                1e-3,
                rel_tol=0.0,
                abs_tol=1e-18,
            )
        )

    def test_trims_whitespace_around_units(self):
        self.assertEqual(convert_length(1, "  meter  ", " centimeter "), 100.0)

    def test_public_import_exposes_convert_length(self):
        from src import convert_length as package_convert_length

        self.assertEqual(package_convert_length(5, "meter", "centimeter"), 500.0)


if __name__ == "__main__":
    unittest.main()
