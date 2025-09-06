from fastapi import APIRouter, File, Form, Request, UploadFile, HTTPException
import core.routes as routes
from services.wardrobe_service import handle_enhance_webhook, process_wardrobe_image

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
            job_id, job = await handle_enhance_webhook(payload)

            loop = asyncio.get_running_loop()
            loop.create_task(chain_remove_background(job_id))

            return {"status": "Enhance webhook received successfully, and rembg started"}
        else:
            await mark_job_failed(job_id)

            return {"status": "failed"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing enhance webhook: {e}"
        )

@wardrobe_router.get(routes.WARDROBE_JOB_STATUS)
async def fetch_job_status(job_id: str, is_enhance: bool):
    try:
        return get_job_status(job_id, is_enhance)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching job status for {job_id}: {e}"
        )