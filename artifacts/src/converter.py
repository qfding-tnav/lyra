from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Unit:
    key: str
    name: str
    symbol: str
    factor: float
    category: str


@dataclass(frozen=True)
class CategoryConfig:
    label: str
    ordered_unit_keys: List[str]
    default_from_unit: str
    default_to_unit: str
    allow_negative: bool = False


UNITS: Dict[str, Dict[str, Unit]] = {
    "length": {
        "meter": Unit("meter", "Meter", "m", 1.0, "length"),
        "kilometer": Unit("kilometer", "Kilometer", "km", 1000.0, "length"),
        "centimeter": Unit("centimeter", "Centimeter", "cm", 0.01, "length"),
        "millimeter": Unit("millimeter", "Millimeter", "mm", 0.001, "length"),
        "foot": Unit("foot", "Foot", "ft", 0.3048, "length"),
        "inch": Unit("inch", "Inch", "in", 0.0254, "length"),
        "yard": Unit("yard", "Yard", "yd", 0.9144, "length"),
        "mile": Unit("mile", "Mile", "mi", 1609.344, "length"),
    },
    "weight": {
        "gram": Unit("gram", "Gram", "g", 1.0, "weight"),
        "kilogram": Unit("kilogram", "Kilogram", "kg", 1000.0, "weight"),
        "milligram": Unit("milligram", "Milligram", "mg", 0.001, "weight"),
        "pound": Unit("pound", "Pound", "lb", 453.59237, "weight"),
        "ounce": Unit("ounce", "Ounce", "oz", 28.349523125, "weight"),
    },
    "area": {
        "square_meter": Unit("square_meter", "Square Meter", "m²", 1.0, "area"),
        "square_kilometer": Unit("square_kilometer", "Square Kilometer", "km²", 1_000_000.0, "area"),
        "square_centimeter": Unit("square_centimeter", "Square Centimeter", "cm²", 0.0001, "area"),
        "square_millimeter": Unit("square_millimeter", "Square Millimeter", "mm²", 0.000001, "area"),
        "square_foot": Unit("square_foot", "Square Foot", "ft²", 0.09290304, "area"),
        "square_inch": Unit("square_inch", "Square Inch", "in²", 0.00064516, "area"),
        "square_yard": Unit("square_yard", "Square Yard", "yd²", 0.83612736, "area"),
        "acre": Unit("acre", "Acre", "ac", 4046.8564224, "area"),
        "hectare": Unit("hectare", "Hectare", "ha", 10000.0, "area"),
    },
}


CATEGORY_CONFIGS: Dict[str, CategoryConfig] = {
    "length": CategoryConfig(
        label="Length",
        ordered_unit_keys=[
            "meter",
            "kilometer",
            "centimeter",
            "millimeter",
            "foot",
            "inch",
            "yard",
            "mile",
        ],
        default_from_unit="meter",
        default_to_unit="kilometer",
        allow_negative=False,
    ),
    "weight": CategoryConfig(
        label="Weight",
        ordered_unit_keys=[
            "gram",
            "kilogram",
            "milligram",
            "pound",
            "ounce",
        ],
        default_from_unit="gram",
        default_to_unit="kilogram",
        allow_negative=False,
    ),
    "area": CategoryConfig(
        label="Area",
        ordered_unit_keys=[
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
        default_from_unit="square_meter",
        default_to_unit="square_kilometer",
        allow_negative=False,
    ),
}


class ConversionError(ValueError):
    pass


def _get_category_config(category: str) -> CategoryConfig:
    if category not in CATEGORY_CONFIGS or category not in UNITS:
        raise ConversionError(f"Unknown category: {category}")
    return CATEGORY_CONFIGS[category]


def get_categories() -> List[str]:
    return list(CATEGORY_CONFIGS.keys())


def get_category_label(category: str) -> str:
    return _get_category_config(category).label


def get_units(category: str) -> List[Unit]:
    config = _get_category_config(category)
    category_units = UNITS[category]
    return [category_units[unit_key] for unit_key in config.ordered_unit_keys]


def parse_value(raw_value: str | int | float | None) -> float | None:
    if raw_value is None:
        return None
    if isinstance(raw_value, (int, float)):
        value = float(raw_value)
    else:
        text = raw_value.strip()
        if text == "":
            return None
        try:
            value = float(text)
        except ValueError as exc:
            raise ConversionError("Input must be numeric") from exc
    if value != value or value in (float("inf"), float("-inf")):
        raise ConversionError("Input must be a finite number")
    return value


def convert(category: str, value: str | int | float | None, from_unit: str, to_unit: str) -> float | None:
    numeric_value = parse_value(value)
    if numeric_value is None:
        return None

    config = _get_category_config(category)
    category_units = UNITS[category]

    if numeric_value < 0 and not config.allow_negative:
        raise ConversionError(f"Negative values are not allowed for category '{category}'")

    if from_unit not in category_units:
        raise ConversionError(f"Unknown from-unit '{from_unit}' for category '{category}'")
    if to_unit not in category_units:
        raise ConversionError(f"Unknown to-unit '{to_unit}' for category '{category}'")

    from_factor = category_units[from_unit].factor
    to_factor = category_units[to_unit].factor
    base_value = numeric_value * from_factor
    return base_value / to_factor


def format_value(value: float | None, precision: int = 6) -> str:
    if value is None:
        return ""
    formatted = f"{value:.{precision}f}".rstrip("0").rstrip(".")
    return formatted if formatted else "0"


class UnitConverter:
    def __init__(self) -> None:
        self.category = "length"
        self.input_value = ""
        self.from_unit = CATEGORY_CONFIGS["length"].default_from_unit
        self.to_unit = CATEGORY_CONFIGS["length"].default_to_unit

    def set_category(self, category: str) -> None:
        config = _get_category_config(category)
        self.category = category
        self.from_unit = config.default_from_unit
        self.to_unit = config.default_to_unit
        self.input_value = ""

    def set_input(self, value: str) -> None:
        self.input_value = value

    def swap_units(self) -> None:
        self.from_unit, self.to_unit = self.to_unit, self.from_unit

    def clear(self) -> None:
        self.input_value = ""

    def get_output(self) -> str:
        result = convert(self.category, self.input_value, self.from_unit, self.to_unit)
        return format_value(result)

    def get_available_units(self) -> List[Unit]:
        return get_units(self.category)
