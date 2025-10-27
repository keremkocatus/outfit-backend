import numpy as np
from PIL import Image
from io import BytesIO
import requests

# --- Image helpers ---
def load_image_from_url(url: str) -> Image.Image:
    resp = requests.get(url)
    resp.raise_for_status()
    return Image.open(BytesIO(resp.content))

def resize_image(image: Image.Image, size: tuple = (224, 224)) -> Image.Image:
    return image.resize(size, Image.Resampling.LANCZOS)

def normalize_embedding(emb: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(emb)
    if norm == 0:
        return emb
    return emb / norm

def get_image_from_url(url: str):
    try:
        resp = requests.get(url)
        img = Image.open(BytesIO(resp.content))

        buf = BytesIO()
        img.save(buf, format="PNG", quality=95, optimize=True)

        return buf.getvalue()
    except Exception as e:
        print(f"Error in get_image_from_url: {e}")
        raise
