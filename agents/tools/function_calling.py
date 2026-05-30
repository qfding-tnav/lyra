# !/usr/bin/env python
# coding=utf-8
import json


class FunctionCalling:
    # register function calling to set FUNCTION_CALLING_SET
    FUNCTION_CALLING_SET = {
    }

    def __init__(self):
        pass

    @classmethod
    def call(cls, openai_function, context=None):
        function_set = cls.FUNCTION_CALLING_SET
        function_name = openai_function.name
        fcc = function_set.get(function_name, None)
        if not fcc:
            return ""
        function_args = json.loads(openai_function.arguments)
        if context:
            function_args["_context"] = context
        return fcc(function_args).process()

    @classmethod
    def toolset(cls, name):
        """toolset schema for OpenAi functions"""
        return list(map(lambda px: px.DEFINITION,
                        cls.FUNCTION_CALLING_SET.values()))

    @classmethod
    def toolset_new(cls):
        """New toolset schema for OpenAI functions"""
        tools = []
        for old_fc in cls.FUNCTION_CALLING_SET.values():
            fc = {
                "type": "function",
            }
            fc.update(old_fc.DEFINITION.get("function", {}))
            tools.append(fc)
        return tools
