# -*- coding: utf-8 -*-
"""
@File    :   list_available_skills.py
@Author  :   qfding
@Date    :   2026-06-12
@Desc    :   This file contains the definition of the ListAvailableSkills class.
"""
import json
import os
import sys
from pathlib import Path

import yaml

ROOT_DIR = str(Path(__file__).resolve().parents[3])
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)


class ListAvailableSkills:
    """Tool Functions: list_available_skills"""
    DEFINITION = {
        "type": "function",
        "function": {
            "name": "list_available_skills",
            "description": "Inspects the system registry and returns a comprehensive list of all currently installed skills, including their IDs and descriptions. Use this tool when the user asks what capabilities are available, or when you need to check which skill fits a specific task.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }

    def __init__(self, args={}):
        self.args = args
        self.skill_dirs = [os.path.join(ROOT_DIR, "agents", "skills"),
                           os.path.join(ROOT_DIR, "artifacts", "skills")]

    # must be defined
    def process(self):
        """Scans the skills directory, parses the YAML frontmatter of each file,
and returns a JSON string listing all available skill IDs and descriptions.
Returns:
    str: A JSON-formatted string summarizing the available skills.
    """
        available_skills = []
        for path in self.skill_dirs:
            if not os.path.exists(path):
                continue
            # os.walk recursively steps through all subfolders
            for root, _, files in os.walk(path):
                for filename in files:
                    if filename.endswith(".md"):
                        # Construct the full local path to read the file
                        full_filepath = os.path.join(root, filename)

                        # Create a clean, relative skill_id that includes subfolders (e.g., "qa/unit_tests")
                        relative_path = os.path.relpath(full_filepath, path)
                        skill_id = relative_path.replace(".md", "")

                        try:
                            with open(full_filepath, "r", encoding="utf-8") as file:
                                content = file.read()

                                if content.startswith("---"):
                                    frontmatter_str = content.split("---")[1]
                                    metadata = yaml.safe_load(frontmatter_str)

                                    available_skills.append({
                                        "skill_id": skill_id,
                                        "name": metadata.get("name", skill_id),
                                        "description": metadata.get("description", "No description provided.")
                                    })
                        except Exception:
                            # Marginally skip malformed files but preserve loop integrity
                            continue
        if not available_skills:
            return json.dumps({"error": f"Skills does not exist."}, indent=2)
        return json.dumps({"available_skills": available_skills}, indent=2)


if __name__ == "__main__":
    print(ListAvailableSkills().process())
