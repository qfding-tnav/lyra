# unitConverter

A simple Python unit converter project with support for area conversions.

## Supported area units

- square meter (`square_meter`, `m2`)
- square centimeter (`square_centimeter`, `cm2`)
- square kilometer (`square_kilometer`, `km2`)
- square foot (`square_foot`, `ft2`)
- square inch (`square_inch`, `in2`)
- acre (`acre`)
- hectare (`hectare`)

## Usage

You can use the top-level API from `src/main.py`:

```python
from src.main import convert_area_value

result = convert_area_value(2, "square_meter", "square_centimeter")
print(result)  # 20000.0
```

You can also use the CLI:

```bash
python -m src.main 2 square_meter square_centimeter
```

Example:

- `1 square_kilometer` = `1000000.0 square_meter`
- `1 square_meter` = `10000.0 square_centimeter`
