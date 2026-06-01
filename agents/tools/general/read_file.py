# -*- coding: utf-8 -*-
"""
@File    :   read_file.py
@Author  :   qfding
@Date    :   2026-05-30
@Desc    :   This file contains the definition of the ReadFile class.
"""
import os

from tools.utils import path_utils


class ReadFile:
    """Tool Functions: read a file and return its content."""
    DEFINITION = {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads the content of a file. Use this to check existing code before editing.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "Path relative to artifacts/ (e.g., 'src/main.py')"}
                },
                "required": ["filepath"]
            }
        }
    }

    def __init__(self, args={}):
        self.args = args
        self.filepath = args.get("filepath", "")

    # must be defined
    def process(self):
        print(f"function calling ReadFile {self.args}")
        """Reads the content of an existing file."""
        safe_path = path_utils.get_safe_path(self.filepath)

        if not os.path.exists(safe_path):
            return (f"Error: File '{self.filepath}' does not exist. "
                    f"Try using list_directory to see what files are available.")

        # NEW: Check if the AI accidentally passed a folder
        if os.path.isdir(safe_path):
            return (f"Error: '{self.filepath}' is a directory, not a file. "
                    f"You cannot read a directory. Please use the 'list_directory' tool instead.")

        try:
            with open(safe_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"
