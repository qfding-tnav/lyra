# !/usr/bin/env python
# coding=utf-8
import json

from constants import agent_constants
from tools.general.create_file import CreateFile
from tools.general.delete_file import DeleteFile
from tools.general.list_directory import ListDirectory
from tools.general.read_file import ReadFile
from tools.general.run_bash_cmd import RunBashCmd


class FunctionCalling:
    # register function calling to set FUNCTION_CALLING_SET
    FC_GENERATOR_SET = {
        "create_file": CreateFile,
        "delete_file": DeleteFile,
        "read_file": ReadFile,
        "list_directory": ListDirectory,
        "run_bash_cmd": RunBashCmd
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
