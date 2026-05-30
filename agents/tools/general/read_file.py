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

    def __init__(self):
        """Initialization method of the class."""
        pass

    def _protected_method(self):
        """Protected method, starts with a single underscore."""
        pass

    def __private_method(self):
        """Private method, starts with double underscores for name mangling."""
        pass

    def public_method(self, param1):
        """
        Description of the public method.
        
        Args:
            param1 (type): Description of the parameter.
            
        Returns:
            return_type: Description of the return value.
        """
        pass

    def read_file(filepath: str) -> str:
        """Reads the content of an existing file."""
        safe_path = os.path.join("artifacts", filepath)
        if not os.path.exists(safe_path):
            return f"Error: File {safe_path} does not exist."
        try:
            with open(safe_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"
