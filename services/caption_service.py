from core import config
from db.insert import insert_to_db
from db.update import update_in_db
from registery.registery import get_job_id_by_job, update_registry
from services.openai.generate_caption import generate_structured_caption
from utils.caption_tools.hex_utils import convert_colors_to_hex_format

async def process_caption_for_job(job: dict) -> dict | str:
    """
    Generates an AI-based outfit caption for the given job,
    stores it in Supabase and updates related registries.

    Args:
        job (dict): A job dict containing wardrobe_id, user_id, image_url, etc.

    Returns:
        dict: Generated caption object (structured)
        str: "Error generating caption" in case of failure
    """
    try:
        # 1. Generate caption using OpenAI
        caption_data = await generate_structured_caption(job["image_url"])

        # 2. Save to clothes detail table
        await insert_clothes_detail(
            wardrobe_id=job["wardrobe_id"],
            user_id=job["user_id"],
            caption=caption_data
        )

        # 3. Update registry
        job_id = get_job_id_by_job(job)
        update_registry(job_id, "caption_status", "finished")

        # 4. Update Supabase wardrobe entry
        updated_data = {"caption": caption_data["ai_context"],
                "caption_status": "finished"}
        
        resp = await update_in_db(config.WARDROBE_TABLE_NAME, updated_data, "image_url", job["image_url"])

        return caption_data

    except Exception as e:
        print(f"[Caption Service] Error: {e}")
        return "Error generating caption"


async def insert_clothes_detail(wardrobe_item_id: str, user_id: str, caption_data: dict) -> dict:
    """
    Insert structured clothing details into clothes_detail table
    """
    try:
        # Convert color names to hex format
        color_names = caption_data.get("colors", [])
        colors_with_hex = convert_colors_to_hex_format(color_names)

        detail_record = {
            "wardrobe_item_id": wardrobe_item_id,
            "user_id": user_id,
            "name": caption_data.get("brief_caption", "Clothing Item"),
            "category": caption_data.get("category", "Unknown"),
            "material": caption_data.get("material", "Cotton"),
            "style": caption_data.get("style", "Casual"),
            "colors": colors_with_hex,
            "seasons": caption_data.get("seasons", []),
            "notes": caption_data.get("ai_context", "Add a note..."),
        }

        resp = await insert_to_db(config.CLOTHES_DETAIL_TABLE, detail_record)

        return {"status": "Clothes detail successfully inserted"}
    except Exception as error:
        print(f"Error in insert_clothes_detail: {error}")
        return None
