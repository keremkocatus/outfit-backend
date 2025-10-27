from fastapi import APIRouter, File, Form, Request, UploadFile, HTTPException
from core import config
import core.routes as routes
from registery.registery import get_job_status
from services.edit_service import process_edit_image, handle_edit_webhook
from services.error_service import prediction_failed
from services.token_service import check_token

edit_router = APIRouter()

@edit_router.post(routes.IMAGE_EDIT)
async def edit_process(
    user_id: str = Form(...),
    image: UploadFile = File(...),   
    prompt: str = Form(...)
):
    try:
        if not await check_token(user_id=user_id, required_token_count=1):
            return {"status": "failed", "detail": "Token not enough."}
        
        job_id = await process_edit_image(
            user_id=user_id,
            image=image,
            prompt=prompt
        )

        return {"job_id": job_id}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in edit image process: {e}"
        )

@edit_router.post(routes.WEBHOOK_IMAGE_EDIT)
async def replicate_edit_webhook(request: Request):
    """
    Webhook endpoint for replicate edit predictions (e.g. once 'succeeded').
    """
    try:
        payload = await request.json()
        status = payload.get("status")

        if status == "succeeded":
            _, _ = await handle_edit_webhook(payload)

            return {"status": "Edit webhook received successfully."}
        else:
            await prediction_failed(payload, config.EDIT_TABLE_NAME, "prediction_id", ["status"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing enhance webhook: {e}"
        )

@edit_router.get(routes.EDIT_JOB_STATUS)
async def fetch_job_status(job_id: str):
    try:
        return await get_job_status(job_id, ["status"], "edited_image_url")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching job status for {job_id}: {e}"
        )