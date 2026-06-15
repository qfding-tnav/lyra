# -*- coding: utf-8 -*-
"""
@File    :   skill_utils.py
@Author  :   qfding
@Date    :   2026-06-02
@Desc    :   This file contains the definition of the skill_utils class.
"""
import os
import sys
from pathlib import Path

ROOT_DIR = str(Path(__file__).resolve().parents[3])
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)


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


def load_agent_role_skill(skill):
    """Reads the core skill file to understand the agent's capabilities."""
    core_skill = os.path.join(ROOT_DIR, "agents", "skills", "core", f"{skill}.md")
    if not os.path.exists(core_skill):
        print("File not found at " + core_skill)
        return ""
    try:
        with open(core_skill, "r", encoding="utf-8") as f:
            print(f"Successfully loaded skills from {core_skill}")
            return f.read()
    except FileNotFoundError:
        print(f"Warning: Skills file not found at {core_skill}. Proceeding without skill context.")
    return ""
