# unitConverter

A small Python utility for converting length values between units using [Pint](https://pint.readthedocs.io/).

## Setup

```bash
pip install -r requirements.txt
```

## What it does

The project provides a `convert_length(value, from_unit, to_unit)` function backed by Pint's unit registry. It validates input and converts between supported length units such as meters, centimeters, kilometers, inches, feet, and miles.

## Usage

### As a Python function

```python
from src.length_converter import convert_length

result = convert_length(5, "meter", "centimeter")
print(result)  # 500.0
```

### From the command line

```bash
python src/main.py 3 mile kilometer
```

## Example conversions

- `convert_length(1, "meter", "centimeter")` -> `100.0`
- `convert_length(2.5, "kilometer", "meter")` -> `2500.0`
- `convert_length(12, "inch", "foot")` -> `1.0`
- `convert_length(3, "mile", "kilometer")` -> approximately `4.828032`

## Invalid input handling

The converter raises clear exceptions for:

- non-numeric values,
- empty or missing unit strings,
- unsupported or misspelled unit names,
- non-length units such as mass or time units.

Negative values and zero are accepted and converted normally because they are valid numeric lengths for the purpose of unit conversion.
