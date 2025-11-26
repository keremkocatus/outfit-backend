from typing import List
from fastapi import APIRouter, File, Form, Request, UploadFile, HTTPException
from core import config, rule_engine
import core.routes as routes
from registery.registery import get_job_status
from services.error_service import prediction_failed
from services.token_service import check_token
from services.wardrobe_service import handle_enhance_webhook, handle_rembg_webhook, process_wardrobe_image

wardrobe_router = APIRouter()

@wardrobe_router.post(routes.WARDROBE_PROCESS)
async def wardrobe_process(
    user_id: str = Form(...),
    clothe_images: List[UploadFile] = File(...),   # birden fazla dosya
    category: str = Form(...),
    is_long_top: bool = Form(False),
    is_enhance: bool = Form(False),
):
    """
    1) Supabase'a upload & job kaydı
    2) Eğer is_enhance:
         - önce enhance tetiklenir
         - tamamlandıktan sonra rembg başlatılır
       Aksi halde direkt rembg.
    """
    try:
        if not await check_token(user_id=user_id, required_token_count=rule_engine.WARDROBE_REQUIRED_TOKEN):
            raise HTTPException(
                status_code=402,
                detail={"Token not enough."}
            )
            
        job_ids = []

        # UploadFile listesi üzerinden dön
        if clothe_images:
            for image in clothe_images:
                job_id = await process_wardrobe_image(
                    user_id=user_id,
                    clothe_image=image,
                    category=category,
                    is_long_top=is_long_top,
                    is_enhance=is_enhance,
                )
                job_ids.append(job_id)
        else:
            return {"status": "There is no image!"}

        return {"job_ids": job_ids}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in wardrobe controller: {e}"
        )

@wardrobe_router.post(routes.WEBHOOK_ENHANCE)
async def replicate_enhance_webhook(request: Request):
    """
    Webhook endpoint for replicate enhance predictions (e.g. once 'succeeded').
    """
    try:
        payload = await request.json()
        status = payload.get("status")

        if status == "succeeded":
            _, _ = await handle_enhance_webhook(payload)

            return {"status": "Enhance webhook received successfully, and rembg started"}
        else:
            await prediction_failed(payload, config.WARDROBE_TABLE_NAME, "enhance_prediction_id", ["enhance_status"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing enhance webhook: {e}"
        )

@wardrobe_router.post(routes.WEBHOOK_FAST_REMBG)
async def replicate_fast_webhook(request: Request):
    try:
        payload = await request.json()
        status = payload.get("status")

        if status == "succeeded":
            _ = await handle_rembg_webhook(payload)
            
            return {"status": "Webhook rembg received successfully"}
        else:
            await prediction_failed(payload, config.WARDROBE_TABLE_NAME, "rembg_prediction_id", ["rembg_status"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing fast webhook: {e}"
        )
        
@wardrobe_router.get(routes.WARDROBE_JOB_STATUS)
async def fetch_job_status(job_id: str):
    try:
        return await get_job_status(job_id, ["enhance_status", "rembg_status", "caption_status"], "removed_bg_image_url", rule_engine.WARDROBE_TOKEN_CHNG_AMT)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching job status for {job_id}: {e}"
        )