# -*- coding: utf-8 -*-
"""
@File    :   list_directory.py
@Author  :   qfding
@Date    :   2026-05-30
@Desc    :   This file contains the definition of the ListDirectory class.
"""
import os

from tools.utils import path_utils


class ListDirectory:
    """Tool Functions: read a file and return its content."""
    DEFINITION = {
        "type": "function",
        "function": {
            "name": "list_directory",
            "description": "Lists all files and folders inside a directory. "
                           "Use this to explore the codebase and find file names before using read_file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "dirpath": {
                        "type": "string",
                        "description": "Directory path relative to artifacts/ (e.g., 'src' or 'tests'). "
                                       "Leave empty '' to list the root directory."
                    }
                },
                "required": ["dirpath"]
            }
        }
    }

    def __init__(self, args={}):
        self.args = args
        self.dirpath = args.get("dirpath", "")

    # must be defined
    def process(self):
        print(f"function calling ListDirectory {self.args}")
        """Lists files and folders in the given directory within artifacts/."""
        # If dirpath is empty, default to the root of artifacts/
        safe_path = path_utils.get_safe_path(self.dirpath)
        if not safe_path:
            return f"Path is None!!!"
        if not os.path.exists(safe_path):
            return f"Error: Directory {safe_path} does not exist."
        if not os.path.isdir(safe_path):
            return f"Error: {safe_path} is a file, not a directory."

        try:
            items = os.listdir(safe_path)
            if not items:
                return f"Directory '{self.dirpath}' is empty."
            return f"Contents of '{self.dirpath}':\n" + "\n".join(f"- {item}" for item in items)
        except Exception as e:
            return f"Error reading directory: {str(e)}"
