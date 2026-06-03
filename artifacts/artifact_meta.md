---
name: Artifact Metadata and Boundary Definition
description: Defines the core project information, directory structure standards,
  and strict sandboxing boundaries for agent-generated artifacts.
type: project_metadata
---

# Artifact Metadata & Execution Boundary (artifact_metd.md)

This file serves as the absolute source of truth for all agents (Planner, Generator, Evaluator, Healer) operating within
this framework. It defines the project parameters, structural guidelines, and immutable security boundaries required
when generating or modifying code.

## 1. Project Information

* **Project Name:** unitConverter
* **Target Language:** Python (Default)
* **Objective:** Ensure all agent-driven file operations are strictly confined, correctly structured, and aligned with
  standard software development practices.

---

## 2. Strict Sandboxing Boundaries

To maintain system integrity and prevent malicious or accidental overwrites of the core framework, agents are restricted
to the `artifacts/` sandbox.

* **The Absolute Boundary:** Every single read, write, list, or delete operation MUST target paths starting with
  `artifacts/{project_name}/`.
* **Framework Protection:** You must **never** attempt to modify the framework's core files (e.g., directories like
  `.github/`, `agents/`, `config/`, or root files like `README.md` and `requirements.txt`).
* **No Path Traversal:** The use of `../` or `../../` to escape the sandbox is strictly prohibited.
* **No Absolute Paths:** Do not use OS-level absolute paths (e.g., `/home/user/`, `C:\`). Always use paths relative to
  the current working directory, starting with the sandbox prefix.

---

## 3. Standardized Directory Structure

When a Planner or Generator agent begins constructing a new project, they must adhere to the following directory layout
inside the designated artifact folder:

```text
artifacts/{project_name}/
├── artifact_meta.md         # A copy of this metadata specific to the project
├── README.md                # Project-specific documentation
├── requirements.txt         # Project-specific dependencies
├── src/                     # Core application source code
│   ├── __init__.py
│   └── main.py              # Application entry point
├── tests/                   # Isolated test suite
│   ├── __init__.py
│   └── test_main.py
└── docs/                    # Additional generated documentation
```

### Sub-directory Rules

* **Root Sandbox:** Only configuration files (e.g., `requirements.txt`, `.gitignore`) and primary documentation (
  `README.md`) are permitted at the root of `artifacts/{project_name}/`.
* **`src/`:** All functional programming logic and modules must be organized here.
* **`tests/`:** All unit and integration tests must be isolated in this folder and mirror the structure of the `src/`
  directory.

---

## 4. Operational Directives

**✅ DO:**

* Extract the `{project_name}` and `{language}` context directly from the active user prompt or planning document before
  creating files.
* Verify your planned file paths begin with `artifacts/{project_name}/` before executing a tool call.
* Ensure generated test files are correctly referencing the code in the `src/` directory.

**❌ DO NOT:**

* Overwrite or read files inside `agents/tools/` or `agents/skills/`.
* Dump loose Python scripts directly into the `artifacts/` directory without nesting them in their respective
  `{project_name}/src/` folder.
* Ignore language-specific conventions (e.g., failing to include `__init__.py` files in Python directories).
