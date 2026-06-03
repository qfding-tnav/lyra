"""Application entry point for unitConverter."""

from __future__ import annotations

import sys

from src.area_converter import convert_area



def convert_area_value(value, from_unit: str, to_unit: str) -> float:
    """Top-level API for area conversion."""
    return convert_area(value, from_unit, to_unit)



def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)

    if len(args) != 3:
        print("Usage: python -m src.main <value> <from_unit> <to_unit>")
        return 1

    raw_value, from_unit, to_unit = args

    try:
        result = convert_area_value(float(raw_value), from_unit, to_unit)
    except (TypeError, ValueError) as exc:
        print(f"Error: {exc}")
        return 1

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
