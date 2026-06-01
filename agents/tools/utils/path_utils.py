# -*- coding: utf-8 -*-
"""
@File    :   path_utils.py
@Author  :   qfding
@Date    :   2026-05-31
@Desc    :   This file contains the definition of the path utility.
"""
import os

from constants import path_constants


def get_safe_path(target_path: str) -> str:
    """Helper to ensure paths correctly resolve inside the artifacts/ directory."""
    clean_path = target_path.strip().strip("/")
    if clean_path.startswith(f"{path_constants.ARTIFACTS_DIR}/"):
        clean_path = clean_path[len(f"{path_constants.ARTIFACTS_DIR}/"):]
    return os.path.join(path_constants.ARTIFACTS_DIR, clean_path)
