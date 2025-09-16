
def create_wardrobe_record(
    image_url: str,
    user_id: str,
    bucket_id: str,
    category: str,
    is_long_top: bool = False,
):
    record = {
        "enhance_status": "processing",
        "rembg_status": "processing",
        "caption_status": "processing",
        "enhance_prediction_id": None,
        "rembg_prediction_id": None,
        "wardrobe_item_id": None,
        "user_id": user_id,
        "bucket_id": bucket_id,
        "image_url": image_url,
        "category": category,
        "is_long_top": is_long_top,
        "removed_bg_image_url": None,
        "enhanced_image_url": None,
    }

    return record

def create_edit_record(
    image_url: str,
    user_id: str,
    bucket_id: str,
    prompt: str
):
    record = {
        "status": "processing",
        "prediction_id": None,
        "user_id": user_id,
        "bucket_id": bucket_id,
        "image_url": image_url,
        "prompt": prompt,
        "edited_image_url": None,
    }

    return record

def create_review_record(
    image_url: str,
    user_id: str,
    bucket_id: str,
    roast_level: str
):
    record = {
        "status": "processing",
        "prediction_id": None,
        "user_id": user_id,
        "bucket_id": bucket_id,
        "image_url": image_url,
        "roast_level": roast_level,
        "result": None,
    }

    return record