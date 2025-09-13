from utils.prompt_utils import get_enhance_prompt

def build_enhance_prediction_input(category: str, image_url: str) -> dict:
    return {
        "prompt": get_enhance_prompt(category),
        "image_input": [image_url],
        "output_format": "jpg",
    }

def build_rembg_prediction_input(image_url: str) -> dict:
    return {
        "image": image_url,
        "format": "png",
        "reverse": False,
        "threshold": -20,
        "background_type": "rgba",
    }
