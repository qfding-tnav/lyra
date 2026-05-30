# Artifact Management & Sandboxing Rules

As the Generator Agent, you are operating within a secure, sandboxed environment. Your primary directive when writing,
modifying, or deleting files is to **strictly confine all operations to the `artifacts/` directory.**

## 1. The Core Mandate

* **Absolutely NO file modifications are permitted outside of the `artifacts/` folder.**
* You must never attempt to read, write, or modify the framework's internal code (e.g., the `agents/`, `.github/`, or
  `config/` directories).
* All generated source code, unit tests, configuration files, and documentation must be saved inside `artifacts/`.

## 2. Directory Structure Constraints

When creating new files, you must organize them into the following subdirectories within `artifacts/`:

* **`artifacts/src/`**: All primary application source code goes here (e.g., `artifacts/src/main.py`,
  `artifacts/src/database.py`).
* **`artifacts/tests/`**: All unit and integration tests go here. Test files must mirror the source files (e.g.,
  `artifacts/tests/test_main.py`).
* **`artifacts/docs/`**: Any generated documentation, diagrams, or readmes for the output code go here.
* **`artifacts/data/`**: Any mock data (JSON, CSV) required by the application or tests goes here.

## 3. Pathing and Security Rules

* **Always use relative paths** starting with `artifacts/`.
* **Never use directory traversal** (e.g., `../` or `../../`) in your tool calls.
* **Never use absolute system paths** (e.g., `/usr/bin/`, `C:\`, `~/`).

## 4. Tool Usage Examples

**✅ CORRECT TOOL USAGE:**

* `create_file(filepath="artifacts/src/app.py", content="...")`
* `read_file(filepath="artifacts/tests/test_app.py")`

**❌ INCORRECT TOOL USAGE (DO NOT DO THIS):**

* `create_file(filepath="app.py", content="...")` *(Fails: Missing artifacts/ prefix)*
* `create_file(filepath="src/app.py", content="...")` *(Fails: Missing artifacts/ prefix)*
* `create_file(filepath="../app.py", content="...")` *(Fails: Directory traversal is blocked)*
