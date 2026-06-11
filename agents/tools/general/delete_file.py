# -*- coding: utf-8 -*-
"""
@File    :   delete_file.py
@Author  :   qfding
@Date    :   2026-06-09
@Desc    :   This file contains the definition of the CreateFile class.
"""
import os

from tools.utils import path_utils


class DeleteFile:
    """Tool Functions: delete_file"""
    DELETE_DEFINITION = {
        "type": "function",
        "function": {
            "name": "delete_file",
            "description": "Deletes an existing file. Use this to remove unnecessary files or clean up before a git commit.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Path relative to artifacts/ of the file to delete (e.g., 'src/old_main.py')"
                    }
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
        print(f"function calling DeleteFile {self.args}")
        """Delete a file with the given path. Restricted to the artifacts/ directory."""
        safe_path = path_utils.get_safe_path(self.filepath)
        if not safe_path:
            return f"Path is None!!!"
        if not os.path.exists(safe_path):
            return f"Error: File '{safe_path}' does not exist."

        if os.path.isdir(safe_path):
            return f"Error: '{safe_path}' is a directory. Please use a directory deletion tool instead."

        try:
            os.remove(safe_path)
            return f"Success: File '{safe_path}' was successfully deleted."
        except Exception as e:
            return f"Error deleting file: {str(e)}"
