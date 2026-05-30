---
name: Strict Sandboxing and Artifact Management
description: Restricts all file generation, modification, and deletion exclusively to the artifacts/ directory to protect framework files.
type: constraint
---

You are operating within a secure, sandboxed environment. Your primary directive when writing, modifying, or deleting
files is to **strictly confine all operations to the `artifacts/` directory.**

**Why:** The framework's core logic (`agents/`, `config/`, `.github/`) must be protected from accidental overwrites or
malicious code generation. The human user expects all output to be neatly organized in the sandbox.

**Directory Structure Constraints:**
When creating new files, organize them into these subdirectories:

* `artifacts/src/`: All primary application source code.
* `artifacts/tests/`: All unit and integration tests (must mirror the source files).
* `artifacts/docs/`: Generated documentation, diagrams, or readmes.
* `artifacts/data/`: Mock data (JSON, CSV) required by the application.

**Pathing and Security Rules:**

* **Always** use relative paths starting with `artifacts/`.
* **Never** use directory traversal (e.g., `../` or `../../`) in your tool calls.
* **Never** use absolute system paths (e.g., `/usr/bin/`, `C:\`).

**How to apply:**

* **DO:** `create_file(filepath="artifacts/src/app.py", content="...")`
* **DO NOT:** `create_file(filepath="app.py", content="...")` *(Fails: Missing artifacts/ prefix)*
* **DO NOT:** `create_file(filepath="../app.py", content="...")` *(Fails: Directory traversal is blocked)*
