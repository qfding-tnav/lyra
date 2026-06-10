# -*- coding: utf-8 -*-
"""
@File    :   label_constants.py
@Author  :   qfding
@Date    :   2026-05-30
@Desc    :   list all constants variables for label
"""

# Planning
PLAN_APPROVED = "status:plan-approved"
PLAN_REJECTED = "status:plan-rejected"

# Generation
GENERATION_PENDING = "status:generation-pending"
GENERATION_COMPLETE = "status:generation-complete"

# Test Generation
TEST_GENERATION_PENDING = "status:test-generation-pending"
TEST_GENERATION_COMPLETE = "status:test-generation-complete"

# Test Runner
TEST_RUNNER_PENDING = "status:test-runner-pending"
TEST_RUNNER_COMPLETE = "status:test-runner-complete"

# Evaluation
EVALUATION_PENDING = "status:evaluation-pending"
EVALUATION_PASSED = "status:evaluation-passed"
EVALUATION_FAILED = "status:evaluation-failed"

# Workflow
NEEDS_HUMAN_REVIEW = "status:needs-human-review"
READY_FOR_MERGE = "status:ready-for-merge"
READY_FOR_PR = "status:ready-for-pr"
