# -*- coding: utf-8 -*-
"""
@File    :   load_skill_context.py
@Author  :   qfding
@Date    :   2026-06-12
@Desc    :   This file contains the definition of the LoadSkillContext class.
"""
import os
import sys
from pathlib import Path

ROOT_DIR = str(Path(__file__).resolve().parents[3])
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)


class LoadSkillContext:
    """Tool Functions: load_skill_context"""
    DEFINITION = {
        "type": "function",
        "function": {
            "name": "load_skill_context",
            "description": "Dynamically loads the full system prompt instructions, specialized role constraints, and execution commands for a specific skill from its markdown configuration file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "skill_id": {
                        "type": "string",
                        "description": "The unique identifier of the skill to load. Must strictly match the skill name (e.g., 'static_code_analysis', 'unit_tests_execution', 'type_checking', 'security_scan')."
                    }
                },
                "required": ["skill_id"]
            }
        }
    }

    def __init__(self, args={}):
        self.args = args
        self.skill_id = args.get("skill_id", "")
        self.skill_dirs = [os.path.join(ROOT_DIR, "agents", "skills", "tools"),
                           os.path.join(ROOT_DIR, "artifacts", ".lyra", "rules"),
                           os.path.join(ROOT_DIR, "artifacts", ".lyra", "custom_tools")]

    # must be defined
    def process(self):
        """Dynamically loads the full system prompt instructions and execution commands for a specific skill from its markdown configuration file."""
        print(f"function calling load_skill_context {self.args}")
        skill_path = Path(self.skill_id)
        if skill_path.suffix != ".md":
            skill_path = skill_path.with_suffix(".md")

        # 2. Iterate through all allowed skill directories
        for base_dir in self.skill_dirs:
            # Convert base_dir to a resolved, absolute Path object
            base_path = Path(base_dir).resolve()

            # Combine base and relative skill path, then resolve it
            target_path = (base_path / skill_path).resolve()

            # 3. Security Guard Check: Ensure the file doesn't escape the base directory
            # pathlib provides an elegant 'is_relative_to' method for boundary checks
            if not target_path.is_relative_to(base_path):
                print(f"Path traversal attempt blocked for '{self.skill_id}' in directory '{base_dir}'")
                continue

            # 4. Check if the file exists securely in this directory
            if target_path.is_file():
                try:
                    print(f"Skill match found: {target_path}")
                    return target_path.read_text(encoding="utf-8")
                except Exception as e:
                    return f"Failed to read skill {self.skill_id}"

        # 5. Fallback: Scan and report available skills if no match is found
        all_available_skills = []
        for base_dir in self.skill_dirs:
            base_path = Path(base_dir)
            if base_path.exists():
                # rglob("*.md") recursively finds all markdown files
                for file in base_path.rglob("*.md"):
                    rel_path = file.relative_to(base_path)
                    # Strip the extension to get the clean skill ID format
                    all_available_skills.append(str(rel_path.with_suffix("")))

        error_msg = (
            f"Skill configuration context matching '{self.skill_id}' could not be located in any registered directories.\n"
            f"Directories checked: {[str(Path(d).resolve()) for d in self.skill_dirs]}\n"
            f"Available skills across all directories: {sorted(list(set(all_available_skills)))}"
        )
        print(error_msg)
        return (f"Failed to read skill {self.skill_id}\n\n"
                f"Available skills across all directories: {sorted(list(set(all_available_skills)))}")


if __name__ == "__main__":
    load_skill_context = LoadSkillContext({"skill_id": "validation/static_code_analysis2"})
    result = load_skill_context.process()
    print("----", result)
