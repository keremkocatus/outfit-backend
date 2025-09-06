import json
from openai import AsyncOpenAI
from utils.caption_tools.caption_process_utils import clean_ai_context, clean_brief_caption
from utils.caption_tools.caption_utils import get_caption_message, get_caption_tool_schema
from core import config

# Initialize OpenAI client
client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)

# ---- Caption generation via OpenAI tool call ----
async def generate_structured_caption(image_url: str) -> dict | None:
    try:
        tools = get_caption_tool_schema()
        messages = get_caption_message(image_url)

        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools,
            tool_choice={
                "type": "function",
                "function": {"name": "submit_cloth_caption"},
            },
        )

        assistant_msg = response.choices[0].message
        if assistant_msg.tool_calls:
            call = assistant_msg.tool_calls[0]
            args = json.loads(call.function.arguments)

            # Clean captions before returning
            args["ai_context"] = clean_ai_context(args["ai_context"])
            args["brief_caption"] = clean_brief_caption(args["brief_caption"])
            return args

        return None
    except Exception as error:
        print(f"Error in generate_structured_caption: {error}")
        return None

