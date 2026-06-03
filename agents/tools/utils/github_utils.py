# -*- coding: utf-8 -*-
"""
@File    :   github_utils.py
@Author  :   qfding
@Date    :   2026-06-02
@Desc    :   This file contains the definition of the github_utils.
"""
from constants import agent_constants, section_constants


def get_approved_plan(issue):
    """Scans the issue to find the final approved plan from the Planner Agent."""
    comments = list(issue.get_comments())
    for comment in reversed(comments):
        if (agent_constants.PLANNER_SIGNATURE in comment.body and
                section_constants.PLAN_DRAFT_HEADER in comment.body):
            return comment.body
    return None


def get_latest_generator_summary(issue):
    """Scans the issue to find the latest generator from the Generator Agent."""
    comments = list(issue.get_comments())
    for comment in reversed(comments):
        if (agent_constants.GENERATOR_SIGNATURE in comment.body and
                section_constants.GENERATOR_EXEC_HEADER in comment.body):
            return comment.body
    return None
