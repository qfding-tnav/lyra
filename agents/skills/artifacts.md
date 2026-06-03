---
name: Strict Sandboxing and Structure Boundary
description: Enforces a strict security boundary for the artifacts/ directory while ensuring the agent builds correct,
  project-specific directory structures.
type: constraint
---

You are operating within a secure, sandboxed environment. Your absolute primary security directive is to **strictly
confine all file operations (read, write, list) to the `artifacts/{project_name}` directory.**

**Pathing and Security Rules:**

* **The Sandbox Root:** Every single file path you interact with MUST begin with `artifacts/`.
* **No Traversal:** **Never** use directory traversal (e.g., `../` or `../../`) in your tool calls to attempt to escape
  the sandbox.
* **No Absolute Paths:** **Never** use absolute system paths (e.g., `/usr/bin/`, `C:\`, `/home/`).

**Project Directory Structure Rules:**
While all files must live inside the sandbox, you must **not** dump files into the root `artifacts/` directory unless it
is a configuration file (like `artifacts/{project_name}/requirements.txt` or `artifacts/{project_name}/package.json`).

You must organize files into standard subdirectories according to the project's language and the Planner's instructions:

* **Python Projects:** Source code should go in `artifacts/{project_name}/src/`, `artifacts/{project_name}/scripts/`, or
  a dedicated package folder.
* **Web Projects:** Components should go in `artifacts/{project_name}/src/components/`, pages in
  `artifacts/{project_name}/src/pages/`, etc.

**How to apply:**

* **DO:** `create_file(filepath="artifacts/{project_name}/src/app.py", content="...")` *(Correct: Sandboxed and
  correctly structured)*
* **DO:** `read_file(filepath="artifacts/{project_name}/src/components/Button.tsx")`
* **DO NOT:** `create_file(filepath="app.py", content="...")` *(Fails: Missing artifacts/ prefix)*
* **DO NOT:** `create_file(filepath="artifacts/app.py", content="...")` *(Avoid: Do not place raw source code in the
  root directory)*
* **DO NOT:** `read_file(filepath="../config/settings.json")` *(Fails: Directory traversal is strictly blocked)*
