import os
from dotenv import load_dotenv
from utils.db_utils import table_name

# Load environment variables
load_dotenv()

# APP URL
APP_URL = os.getenv("APP_URL")

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REPLICATE_API_KEY = os.getenv("REPLICATE_API_TOKEN")
FASHN_API_KEY = os.getenv("FASHN_API_KEY")
FASHN_URL = os.getenv("FASHN_URL")

# Supabase Config
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# Redis URL
REDIS_URL = os.getenv("REDIS_URL")

# Model ID's
REMBG_MODEL_ID = "a029dff38972b5fda4ec5d75d7d1cd25aeff621d2cf4946a41055d7db66b80bc"
ENHANCE_MODEL_ID = "google/nano-banana"
EDIT_MODEL_ID = "google/nano-banana"
TRY_ON_MODEL_ID = "tryon-v1.6"
TRY_ON_BANANA_ID = "google/nano-banana"

# Tables & Buckets
SCHEMA = os.getenv("SCHEMA")

WARDROBE_BUCKET_NAME = "deneme"
WARDROBE_TABLE_NAME = table_name("ai_wardrobe", SCHEMA)

CLOTHES_DETAIL_TABLE = table_name("ai_clothes_detail", SCHEMA)

EDIT_BUCKET_NAME = "edit"
EDIT_TABLE_NAME = table_name("ai_edit", SCHEMA)

REVIEW_TABLE = table_name("ai_review", SCHEMA)
REVIEW_BUCKET = "review"

TRY_ON_BUCKET = "try-on-images"
TRY_ON_TABLE = table_name("ai_try_ons", SCHEMA)

VECTOR_STORE = "comm_vector_store"
