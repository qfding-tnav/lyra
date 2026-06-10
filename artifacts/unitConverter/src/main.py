"""Minimal entry point for manual length conversions."""

from __future__ import annotations

import argparse

from length_converter import (
    InvalidDimensionError,
    InvalidUnitError,
    InvalidValueError,
    convert_length,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convert values between length units.")
    parser.add_argument("value", type=float, help="Numeric value to convert")
    parser.add_argument("from_unit", help="Source length unit")
    parser.add_argument("to_unit", help="Target length unit")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        result = convert_length(args.value, args.from_unit, args.to_unit)
    except (InvalidValueError, InvalidUnitError, InvalidDimensionError) as exc:
        parser.exit(status=1, message=f"Error: {exc}\n")

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
