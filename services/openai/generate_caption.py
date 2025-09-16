from openai import AsyncOpenAI
from services.openai.completion_service import run_tool_completion
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

        args = await run_tool_completion(
            model_name="gpt-4o",
            messages=messages,
            tools=tools,
            tool_name="submit_cloth_caption",
        )

        # Clean captions before returning
        if args:
            args["ai_context"] = clean_ai_context(args["ai_context"])
            args["brief_caption"] = clean_brief_caption(args["brief_caption"])
            
            return args

        return None
    except Exception as error:
        print(f"Error in generate_structured_caption: {error}")
        return None

