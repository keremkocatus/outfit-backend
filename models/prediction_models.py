from utils.prompt_utils import get_enhance_prompt, get_tryon_input

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

def build_edit_prediction_input(prompt: str, image_url: str) -> dict:
    return {
        "prompt": prompt,
        "image_input": [image_url],
        "output_format": "jpg",
    }

def build_tryon_prediction_input(model_name: str, model_url: str, garment_url: str, segmentation_free: bool = False) -> dict:
    return {
            "model_name": model_name, 
            "inputs": {
            "model_image": model_url,
            "garment_image": garment_url,
            "segmentation_free": segmentation_free
            }
        }

def build_tryon_nano_banana_input(model_url: str, garment_url: str, category: str) -> dict:
    return {
        "prompt": get_tryon_input(category),
        "image_input": [model_url, garment_url],
        "output_format": "jpg",
    }