
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
        "wardrobe_id": None,
        "user_id": user_id,
        "bucket_id": bucket_id,
        "image_url": image_url,
        "category": category,
        "is_long_top": is_long_top,
        "rembg_url": None,
        "enhance_url": None,
    }

    return record