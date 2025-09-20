import os
from dotenv import load_dotenv
from core import routes

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REPLICATE_API_KEY = os.getenv("REPLICATE_API_TOKEN")
FASHN_API_KEY = os.getenv("FASHN_API_KEY")

# Supabase Config
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# Model ID's
REMBG_MODEL_ID = "a029dff38972b5fda4ec5d75d7d1cd25aeff621d2cf4946a41055d7db66b80bc"
ENHANCE_MODEL_ID = "google/nano-banana"
EDIT_MODEL_ID = "google/nano-banana"

# Tables & Buckets
WARDROBE_BUCKET_NAME = "deneme"
WARDROBE_TABLE_NAME = "wardrobe"
CLOTHES_DETAIL_TABLE = "clothes_detail"

ERROR_LOG_TABLE = "error_log"

EDIT_BUCKET_NAME = "edit"
EDIT_TABLE_NAME = "edit_deneme"

REVIEW_TABLE = "review_deneme"
REVIEW_BUCKET = "review"

TRY_ON_BUCKET = "try-on-images"
TRY_ON_TABLE = "try_ons"

