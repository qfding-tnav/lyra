# -*- coding: utf-8 -*-
"""
@File    :   skill_utils.py
@Author  :   qfding
@Date    :   2026-06-02
@Desc    :   This file contains the definition of the skill_utils class.
"""
import os


def load_skills(skills=[]):
    """Reads the skill file to understand the agent's capabilities."""
    combined_skills = []
    current_file_path = os.path.abspath(__file__)
    agents_dir = os.path.dirname(
        os.path.dirname(
            os.path.dirname(current_file_path)
        )
    )
    skills_dir = os.path.join(agents_dir, "skills")
    for skill in skills:
        skills_path = os.path.join(skills_dir, skill)
        try:
            with open(skills_path, "r", encoding="utf-8") as f:
                print(f"Successfully loaded skills from {skills_path}")
                combined_skills.append(f.read())
        except FileNotFoundError:
            print(f"Warning: Skills file not found at {skills_path}. Proceeding without skill context.")
    return "\n\n".join(combined_skills)
