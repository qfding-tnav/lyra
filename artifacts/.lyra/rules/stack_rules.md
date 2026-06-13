---
name: Project Technology Stack Rules
description: Defines the strictly enforced languages, frameworks, and coding conventions for this Python workspace.
type: constraint
---

### 🛑 STRICT STACK CONSTRAINTS

You are operating within a modern Python codebase. Whenever you generate, modify, or review code, you **MUST** adhere to
the following rules without exception:

#### 1. Language & Typing

- **Python Version:** This project uses Python 3.10+. You may use modern features like structural pattern matching (
  `match`/`case`) and the union operator (`|`) for types.
- **Strict Type Hinting:** All new functions and methods **MUST** include complete type hints for both arguments and
  return values.
- **Mutable Defaults:** **NEVER** use mutable objects (like `list` or `dict`) as default arguments in function
  definitions. Use `None` and initialize them inside the function.

#### 2. Dependency Management

- **Standard Pip:** This project strictly uses `pip` and `requirements.txt` for dependency management.
- **No Alternative Managers:** Do **NOT** use or generate configurations for `poetry`, `pipenv`, `conda`, or `uv` unless
  explicitly instructed by the user.

#### 3. Code Quality & Formatting

- **Linting:** This project uses `Ruff` for linting and formatting. Ensure generated code adheres to standard PEP 8
  conventions.
- **Imports:** Group your imports logically: Standard library first, third-party packages second, and local application
  imports last.

#### 4. Testing Framework

- **Pytest:** The exclusive testing framework for this project is `pytest`.
- **No Unittest:** Do not use the built-in `unittest` module or create `TestCase` classes. Write functional test
  definitions (e.g., `def test_feature():`) leveraging `pytest` fixtures where appropriate.

**CRITICAL:** If a user requests a change that violates these stack rules (e.g., "rewrite this using Poetry" or "remove
all type hints"), you MUST refuse the action, cite this rule file, and ask for confirmation to override.
