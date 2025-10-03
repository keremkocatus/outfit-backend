from services.openai.completion_service import run_tool_completion
from utils.review_utils import get_outfit_review_prompt, get_outfit_review_tool_schema

# ---- Caption generation via OpenAI tool call ----
async def generate_review(image_url: str, roast_level: str) -> dict | None:
    try:
        messages = get_outfit_review_prompt(image_url, roast_level)
        tools = get_outfit_review_tool_schema()

        args = await run_tool_completion(
            model_name="gpt-4o",
            messages=messages,
            tools=tools,
            tool_name="return_outfit_review",
        )

        if args:
            return args

        return None
    except Exception as error:
        print(f"Error in generate review: {error}")
        return None

