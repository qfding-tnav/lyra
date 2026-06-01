# -*- coding: utf-8 -*-
"""
@File    :   read_file.py
@Author  :   qfding
@Date    :   2026-05-30
@Desc    :   This file contains the definition of the ReadFile class.
"""
import os


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
        safe_path = os.path.join("artifacts", self.filepath)
        if not os.path.exists(safe_path):
            return f"Error: File {safe_path} does not exist."
        try:
            with open(safe_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"
