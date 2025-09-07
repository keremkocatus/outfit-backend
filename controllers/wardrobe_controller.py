from fastapi import APIRouter, File, Form, Request, UploadFile, HTTPException
import core.routes as routes
from registery.registery import get_job_status
from services.error_service import mark_job_failed
from services.wardrobe_service import handle_enhance_webhook, handle_rembg_webhook, process_wardrobe_image

wardrobe_router = APIRouter()

@wardrobe_router.post(routes.WARDROBE_PROCESS)
async def wardrobe_process(
    user_id: str = Form(...),
    clothe_image: UploadFile = File(...),
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
        job_id = await process_wardrobe_image(
            user_id=user_id,
            clothe_image=clothe_image,
            category=category,
            is_long_top=is_long_top,
            is_enhance=is_enhance,
        )

        return {"job_id": job_id}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in chain process: {e}"
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
            pass

            return {"status": "failed"}
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
            pass
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
        return get_job_status(job_id, ["enhance_status", "rembg_status", "caption_status"], "removed_bg_image_url")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching job status for {job_id}: {e}"
        )