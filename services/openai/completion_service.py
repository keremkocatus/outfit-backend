import json
from openai import AsyncOpenAI
from core import config

client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)

async def run_tool_completion(
    model_name: str,
    messages: list,
    tools: list,
    tool_name: str,
) -> dict | None:
    """
    Generic helper to run a tool-based OpenAI chat completion.
    - messages: Chat messages (system/user/image vs.)
    - tools: Tool schemas (list)
    - tool_name: Which tool to force the model to call
    """
    try:
        response = await client.chat.completions.create(
            model=model_name,
            messages=messages,
            tools=tools,
            tool_choice={"type": "function", "function": {"name": tool_name}},
        )

        assistant_msg = response.choices[0].message
        if assistant_msg.tool_calls:
            call = assistant_msg.tool_calls[0]
            return json.loads(call.function.arguments)
        return None
    except Exception as error:
        print(f"Error in run_tool_completion: {error}")
        return None
