# !/usr/bin/env python
# coding=utf-8

import json
import sys
from pathlib import Path

ROOT_DIR = str(Path(__file__).resolve().parents[3])
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from agents.constants import agent_constants
from agents.tools.general.create_file import CreateFile
from agents.tools.general.delete_file import DeleteFile
from agents.tools.general.list_directory import ListDirectory
from agents.tools.general.read_file import ReadFile
from agents.tools.general.run_bash_cmd import RunBashCmd
from agents.tools.general.list_available_skills import ListAvailableSkills
from agents.tools.general.load_skill_context import LoadSkillContext


class FunctionCalling:
    # register function calling to set FUNCTION_CALLING_SET
    FC_GENERATOR_SET = {
        "create_file": CreateFile,
        "delete_file": DeleteFile,
        "read_file": ReadFile,
        "list_directory": ListDirectory,
        "run_bash_cmd": RunBashCmd,
        "load_skill_context": LoadSkillContext,
        "list_available_skills": ListAvailableSkills
    }
    FUNCTION_CALLING_SET = {
        agent_constants.AGENT_GENERATOR: FC_GENERATOR_SET
    }

    def __init__(self):
        pass

    @classmethod
    def call(cls, openai_function, toolset_name):
        function_set = cls._toolset(toolset_name)
        function_name = openai_function.name
        fcc = function_set.get(function_name, None)
        if not fcc:
            return ""
        function_args = json.loads(openai_function.arguments)
        return fcc(function_args).process()

    @classmethod
    def toolset(cls, toolset_name):
        """toolset schema for OpenAi functions"""
        return list(map(lambda px: px.DEFINITION,
                        cls._toolset(toolset_name).values()))

    @classmethod
    def toolset_new(cls, toolset_name):
        """New toolset schema for OpenAI functions"""
        tools = []
        for old_fc in cls._toolset(toolset_name).values():
            fc = {
                "type": "function",
            }
            fc.update(old_fc.DEFINITION.get("function", {}))
            tools.append(fc)
        return tools

    @classmethod
    def _toolset(cls, toolset_name):
        """toolset schema by toolset_name"""
        return cls.FUNCTION_CALLING_SET.get(toolset_name, {})
