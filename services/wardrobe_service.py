import asyncio
from fastapi import UploadFile, HTTPException
from core import config, routes
from db.insert import insert_job_record
from db.upload_image import upload_image
from models.prediction_models import build_enhance_prediction_input, build_rembg_prediction_input
from registery.registery import get_job_by_prediction_id, register_job, update_registry
from models.registery_models import create_wardrobe_record
from services.background_service import start_enhance_background_process
from services.replicate_service import trigger_prediction
from utils.extrack_utils import extract_id


async def process_wardrobe_image(
    user_id: str,
    clothe_image: UploadFile,
    category: str,
    is_long_top: bool,
    is_enhance: bool,
):
    try:
        # Upload işlemi (supabase)
        bucket = config.WARDROBE_BUCKET_NAME
        file_name = f"{category}.jpg"

        public_url, bucket_id = await upload_image(user_id, bucket, None, file_name, clothe_image)

        # Job kaydı
        job = create_wardrobe_record(public_url, user_id, bucket_id, category, is_long_top)
        job_id = register_job(job)

        # DB'ye başlangıç kaydını ekle
        resp = await insert_job_record(
            job_id=job_id, 
            table_name=config.WARDROBE_TABLE_NAME, 
            insert_keys=[
                "image_url",
                "user_id",
                "category",
                "is_long_top",
                "job_id",
                "enhance_status",
                "rembg_status"
            ])
        
        update_registry(job_id, "wardrobe_id", extract_id(resp["response"].data))

        # Enhance veya Rembg tetikleme
        loop = asyncio.get_running_loop()
        if is_enhance:
            loop.create_task(trigger_prediction(
                job_id,
                model_id=config.ENHANCE_MODEL_ID, 
                webhook_url=routes.WEBHOOK_ENHANCE, 
                prediction_input=build_enhance_prediction_input(category, job["image_url"]), 
                prediction_id_name="enhance_prediction_id")
                )
        else:
            loop.create_task(trigger_prediction(
                job_id,
                model_id=config.REMBG_MODEL_ID,
                webhook_url=routes.WEBHOOK_FAST_REMBG,
                prediction_input=build_rembg_prediction_input(job["image_url"]),
                prediction_id_name="rembg_prediction_id"
            ))

        # Servis sonucu dönüyor
        return {"job_id": job_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in wardrobe process: {e}")


# Handle webhook event for enhancement prediction completion
async def handle_enhance_webhook(payload: dict) -> None:
    job_id = None
    try:
        status = payload.get("status")

        if status == "succeeded":
            prediction_id = payload.get("id")
            job_id, job = get_job_by_prediction_id(prediction_id, "enhance_prediction_id")

            await start_enhance_background_process(payload, job_id, job)

            loop = asyncio.get_running_loop()

            loop.create_task(trigger_prediction(
                job_id,
                model_id=config.REMBG_MODEL_ID,
                webhook_url=routes.WEBHOOK_FAST_REMBG,
                prediction_input=build_rembg_prediction_input(job["image_url"]),
                prediction_id_name="rembg_prediction_id"
            ))

            return job_id, job
        else:
            await mark_job_failed(job_id)
    except Exception as e:
        if job_id:
            await mark_job_failed(job_id)
        raise HTTPException(status_code=500, detail=f"Webhook processing failed: {e}")