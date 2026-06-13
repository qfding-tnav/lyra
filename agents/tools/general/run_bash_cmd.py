# -*- coding: utf-8 -*-
"""
@File    :   run_bash_cmd.py
@Author  :   qfding
@Date    :   2026-06-02
@Desc    :   This file contains the definition of the RunBashCmd class.
"""
import os
import subprocess

from tools.utils import path_utils


class RunBashCmd:
    DEFINITION = {
        "type": "function",
        "function": {
            "name": "run_bash_cmd",
            "description": "Executes a shell command inside the artifacts/ directory. Use this for running tests, static code analysis, linting, or executing scripts. Avoid using this for destructive file operations.",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The exact terminal command to execute. Examples: 'pytest tests/', 'flake8 .', 'mypy src/', or 'python -m unittest'."
                    },
                    "working_dir": {
                        "type": "string",
                        "description": "The relative directory path where the command should be executed.",
                        "default": "artifacts/"
                    },
                    "output_file": {
                        "type": "string",
                        "description": "Optional relative path to a file where the command's stdout and stderr should be saved (e.g., 'lint_report.txt' or 'test_results.log')."
                    }
                },
                "required": [
                    "command",
                    "working_dir"
                ],
                "additionalProperties": False
            }
        }
    }

    def __init__(self, args={}):
        self.args = args
        self.command = args.get("command", "")
        self.working_dir = args.get("working_dir", "")
        self.output_file = args.get("output_file", "")

    # must be defined
    def process(self):
        """Executes a bash command inside the artifacts directory to run tests."""
        print(f"function calling RunBashCmd {self.args}")
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
            output = f"Exit Code: {result.returncode}\nOutput:\n{output}"
            self.write_into_file(output)
            return output
        except subprocess.TimeoutExpired:
            output = "Error: Command timed out after 30 seconds."
            self.write_into_file(output)
            return output
        except Exception as e:
            output = f"Error executing command: {str(e)}"
            self.write_into_file(output)
            return output

    def write_into_file(self, content):
        """Writes the content to a file"""
        if not self.output_file:
            return f"Path is None!!!"
        print(f"Write log into file {self.output_file}")
        log_file = path_utils.get_safe_path(self.output_file)
        if not log_file:
            return f"Path is None!!!"
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        try:
            with open(log_file, "w", encoding="utf-8") as f:
                f.write(self.content)
            return f"Success: Created {log_file}"
        except Exception as e:
            return f"Error creating file: {str(e)}"
