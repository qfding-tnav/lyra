# -*- coding: utf-8 -*-
"""
@File    :   create_file.py
@Author  :   qfding
@Date    :   2026-05-30
@Desc    :   This file contains the definition of the CreateFile class.
"""
import os

from tools.utils import path_utils


class CreateFile:
    """Tool Functions: create_file"""
    DEFINITION = {
        "type": "function",
        "function": {
            "name": "create_file",
            "description": "Creates a new file or overwrites an existing one. Use this to write source code and tests.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "Path relative to artifacts/ (e.g., 'src/main.py')"},
                    "content": {"type": "string", "description": "The exact source code to write into the file."}
                },
                "required": ["filepath", "content"]
            }
        }
    }

    def __init__(self, args={}):
        self.args = args
        self.filepath = args.get("filepath", "")
        self.content = args.get("content", "")

    # must be defined
    def process(self):
        print(f"function calling CreateFile {self.args}")
        """Creates a file with the given content. Restricted to the artifacts/ directory."""
        safe_path = path_utils.get_safe_path(self.filepath)
        if not safe_path:
            return f"Path is None!!!"
        os.makedirs(os.path.dirname(safe_path), exist_ok=True)
        try:
            with open(safe_path, "w", encoding="utf-8") as f:
                f.write(self.content)
            return f"Success: Created {safe_path}"
        except Exception as e:
            return f"Error creating file: {str(e)}"
