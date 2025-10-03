import numpy as np
from PIL import Image
from io import BytesIO
import requests
from tensorflow.keras.applications.mobilenet_v3 import preprocess_input # type: ignore
from tensorflow.keras.applications import MobileNetV3Small # type: ignore
from tensorflow.keras.models import Model # type: ignore
from sklearn.decomposition import PCA

# --- Image helpers ---
def load_image_from_url(url: str) -> Image.Image:
    resp = requests.get(url)
    resp.raise_for_status()
    return Image.open(BytesIO(resp.content))

def resize_image(image: Image.Image, size: tuple = (224, 224)) -> Image.Image:
    return image.resize(size, Image.Resampling.LANCZOS)

def prepare_image(img: Image.Image) -> np.ndarray:
    arr = np.array(img.convert("RGB"), dtype=np.float32)
    arr = np.expand_dims(arr, axis=0)  # (224,224,3) -> (1,224,224,3)
    arr = preprocess_input(arr)
    return arr

def normalize_embedding(emb: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(emb)
    if norm == 0:
        return emb
    return emb / norm

# --- Model setup ---
_base_model = MobileNetV3Small(
    weights="imagenet",
    include_top=False,
    pooling="max",
    alpha=0.75   # küçültüp hızlandırabilirsin (0.35–1.0 arası)
)
mobilenet_model = Model(inputs=_base_model.input, outputs=_base_model.output)

def extract_embedding(img_array: np.ndarray) -> np.ndarray:
    """
    Tek resim (1,224,224,3) veya batch (N,224,224,3) alır.
    """
    features = mobilenet_model.predict(img_array)
    return features  # (N,576) → MobileNetV3-Small output

# --- Dim reduction (opsiyonel) ---
def reduce_dim(features: np.ndarray, target_dim: int = 256) -> np.ndarray:
    pca = PCA(n_components=target_dim, random_state=42)
    return pca.fit_transform(features)

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
