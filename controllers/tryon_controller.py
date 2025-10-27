from typing import Optional
from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from core import config
import core.routes as routes
from registery.registery import get_job_status
from services.token_service import check_token
from services.tryon_service import handle_tryon_webhook, process_tryon

try_on_router = APIRouter()

@try_on_router.post(routes.TRY_ON)
async def try_on_process(
    user_id: str = Form(...),
    model_image: UploadFile = File(...),
    garment_image: Optional[UploadFile] = File(None),  # dosya geldiyse
    garment_url: Optional[str] = Form(None),           # gardırop/URL geldiyse
    category: str = Form(...),
    is_long_top: str = Form(...)                       # mevcut tipini bozmadım
):
    try:
        if not await check_token(user_id=user_id, required_token_count=1):
            raise HTTPException(
                status_code=402,
                detail={"Token not enough."}
            )
        
        # --- Hangisi geldiyse onu kullan ---
        if garment_image is not None:
            job_id = await process_tryon(user_id=user_id, model_image=model_image, garment_image=garment_image, category=category, is_long_top=is_long_top)
        elif garment_url:
            job_id = await process_tryon(user_id=user_id, model_image=model_image, garment_image=garment_url, category=category, is_long_top=is_long_top)
        else:
            raise HTTPException(status_code=400, detail="Garment image or URL is required")

        return {"job_id": job_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in try on process: {e}")

@try_on_router.post(routes.WEBHOOK_TRY_ON)
async def replicate_enhance_webhook(request: Request):
    """
    Webhook endpoint for fashn tryon predictions (e.g. once 'succeeded').
    """
    try:
        payload = await request.json()
        _ = await handle_tryon_webhook(payload)

        return {"status": "Try on webhook received successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing try on webhook: {e}"
        )

@try_on_router.get(routes.TRY_ON_JOB_STATUS)
async def fetch_job_status(job_id: str):
    try:
        return await get_job_status(job_id, ["status"], "result_url")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching job status for {job_id}: {e}"
        )