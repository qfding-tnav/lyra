# -*- coding: utf-8 -*-
"""
@File    :   path_utils.py
@Author  :   qfding
@Date    :   2026-05-31
@Desc    :   This file contains the definition of the path utility.
"""

from pathlib import Path

from constants import path_constants


def get_safe_path(filepath: str) -> str:
    """
    Safely resolves a filepath and ensures it remains inside the base directory.
    """
    clean_path = filepath.strip().strip("/")
    if clean_path.startswith(f"{path_constants.ARTIFACTS_DIR}/"):
        clean_path = clean_path[len(f"{path_constants.ARTIFACTS_DIR}/"):]

    base_dir = path_constants.ARTIFACTS_DIR
    base_path = Path(base_dir).resolve()

    target_path = (base_path / clean_path).resolve()

    # Security Check: Does the resolved target path start with the resolved base path?
    # If not, the agent used "../" to try and escape the directory.
    if not str(target_path).startswith(str(base_path)):
        print(f"Security Violation: Agent attempted to access {target_path} outside of {base_path}")
        return ""

    return str(target_path)
