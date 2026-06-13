---
name: Unit Test Execution Tool
description: Executes the pytest unit test suite for the current Python workspace and dictates the exact workflow for handling test results and tracebacks.
type: tool
---

### 🛠️ EXECUTE UNIT TESTS

When you need to verify your code changes or the user asks you to "run tests," you must follow this exact operational
procedure:

#### Step 1: Pre-flight Dependency Check

Before running any tests, verify that the environment has the necessary testing libraries.

- Check if `pytest` is installed or listed in `requirements.txt`.
- If dependencies are missing or if this is a fresh workspace, run: `pip install -r requirements.txt`

#### Step 2: Execution Command

To run the full test suite, use the terminal execution tool with the following standard command:

```bash
pytest -v

```

*Note: Test files in this repository are located inside the `/tests/` directory and follow the naming
convention `test_*.py`.*

#### Step 3: Handling the Output

Carefully analyze the terminal output from the `pytest` run:

* **If all tests PASS:** Report the success to the user and proceed to your next logical step. Do not modify any further
  code.
* **If tests FAIL:**

1. Do not immediately ask the user for help.
2. Read the specific error traceback provided by `pytest`.
3. Locate the failing `test_*.py` file and the corresponding source file in `/src/`.
4. Attempt to fix the bug in the source code. (Only modify the test file itself if you are certain the test logic is
   outdated relative to a deliberate business logic change).
5. Re-run the tests to verify your fix.

#### Step 4: Running Specific Tests (Efficiency Workflow)

To save execution time and token context, if you only modified one specific file, you should run `pytest` targeting just
that specific test file rather than the entire suite:

```bash
pytest tests/test_specific_feature.py -v

```
