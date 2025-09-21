from core import config

# Dev Ortam Url'i
APP_URL = "https://41af2f2dfeb3.ngrok-free.app"

# Test Ortam Url'i
#APP_URL = "https://outfit-test-python.up.railway.app"

# Canlı Ortam Url'i
#APP_URL = "https://outfit-prod-python.up.railway.app"

# Endpoints
WARDROBE_PROCESS = "/wardrobe/process"
WARDROBE_JOB_STATUS = "/wardrobe/job-status/{job_id}"

LATE_ENHANCE = "/replicate/late-enhance"
LATE_ENHANCE_JOB_STATUS = "/late-enhance/job-status/{job_id}/{is_enhance}"

IMAGE_EDIT = "/replicate/image-edit"
EDIT_JOB_STATUS = "/edit/job-status/{job_id}"

REVIEW_OUTFIT = "/review/start"
REVIEW_JOB_STATUS = "/review/job-status/{job_id}"

TRY_ON = "/fashn/try-on"
TRY_ON_JOB_STATUS = "/fashn/job-status/{job_id}"

# Webhooks
WEBHOOK_FAST_REMBG = "/webhook/replicate/fast-rembg"
WEBHOOK_ENHANCE = "/webhook/replicate-enhance"
WEBHOOK_LATE_ENHANCE = "/webhook/late-enhance"
WEBHOOK_IMAGE_EDIT = "/webhook/image-edit"
WEBHOOK_TRY_ON = f"{config.FASHN_URL}?webhook_url={APP_URL}/webhook/fashn/tryon"