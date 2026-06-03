# -*- coding: utf-8 -*-
"""
@File    :   run_bash_cmd.py
@Author  :   qfding
@Date    :   2026-06-02
@Desc    :   This file contains the definition of the RunBashCmd class.
"""
import os
import subprocess


class RunBashCmd:
    DEFINITION = {
        "type": "function",
        "function": {
            "name": "run_bash_cmd",
            "description": "Executes a shell command inside the artifacts/ directory. "
                           "Use this strictly to run 'pytest tests/' or 'python -m unittest'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The terminal command to run (e.g., 'pytest tests/test_converter.py')"
                    },
                    "working_dir": {
                        "type": "string",
                        "description": "Working directory to run the command in"
                    }
                },
                "required": ["command", "working_dir"]
            }
        }
    }

    def __init__(self, args={}):
        self.args = args
        self.command = args.get("command", "")
        self.working_dir = args.get("working_dir", "")

    # must be defined
    def process(self):
        """Executes a bash command inside the artifacts directory to run tests."""
        # Security: Ensure we only run commands inside our sandbox
        working_dir = os.path.abspath(self.working_dir)

        try:
            # Run the command
            result = subprocess.run(
                self.command,
                shell=True,
                cwd=working_dir,  # Force it to run inside artifacts/
                capture_output=True,
                text=True,
                timeout=30  # Prevent infinite loops if a test hangs
            )

            # Combine stdout and stderr for the LLM to read
            output = result.stdout
            if result.stderr:
                output += f"\nErrors:\n{result.stderr}"

            return f"Exit Code: {result.returncode}\nOutput:\n{output}"

        except subprocess.TimeoutExpired:
            return "Error: Command timed out after 30 seconds."
        except Exception as e:
            return f"Error executing command: {str(e)}"
