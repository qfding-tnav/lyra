import openai

from tools.function_calling import FunctionCalling


class OpenAiClient:
    """llm Client"""
    OPENAI_MODELS_54 = "gpt-5.4"

    def __init__(self, api_key, ai_model=""):
        self.client = openai.OpenAI(api_key=api_key)
        self.ai_model = ai_model or self.OPENAI_MODELS_54

    def __call_openai(self, prompt, system_prompt=[], toolset_name=""):
        # get toolset by toolset_name
        tools = FunctionCalling.toolset_new(toolset_name)
        messages = []
        for s_p in system_prompt:
            messages.append({"role": "system", "content": s_p})
        content_parts = [{
            "type": "input_text",
            "text": str(prompt)
        }]
        messages.append({"role": "user", "content": content_parts})

        while True:  # add loop limitation
            ai_params = {
                "model": self.ai_model,
                "input": messages,
                "stream": False
            }
            if tools:
                ai_params["tools"] = tools
                ai_params["tool_choice"] = "auto"
            response = self.client.responses.create(**ai_params)

            # collect tool outputs to send back
            tool_outputs = []
            function_calls = []
            assistant_messages = []
            for item in response.output:
                if item.type == "function_call":
                    function_calls.append(item)
                    assistant_messages.append({
                        "type": "function_call",
                        "call_id": item.call_id,
                        "name": item.name,
                        "arguments": item.arguments
                    })

            # No function call → final answer
            if not function_calls:
                return response, ""

            # Handle ALL function calls in this round
            for function in function_calls:
                tool_outputs.append({
                    "type": "function_call_output",
                    "call_id": function.call_id,
                    "output": FunctionCalling.call(function, toolset_name)
                })

            # Append tool results and continue loop
            messages += assistant_messages
            messages += tool_outputs
        return None,

    def call(self, prompt, system_prompt=[], toolset_name=""):
        """Call openai to get the response
        tool = [tool_1,tool_2]
        """
        return self.__call_openai(prompt, system_prompt, toolset_name)
