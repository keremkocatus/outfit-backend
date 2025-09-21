import asyncio
from fastapi import UploadFile, HTTPException
from core import config, routes
from db.insert import insert_job_record
from db.upload_image import upload_image
from models.prediction_models import build_tryon_prediction_input
from registery.registery import get_job_by_prediction_id, register_job
from models.registery_models import create_tryon_record
from services.background_service import start_background_process
from services.fashn_service import trigger_fashn
from services.error_service import mark_job_failed, prediction_failed   


# Try-on process
async def process_tryon(
    user_id: str,
    model_image: UploadFile,
    garment_image: None,
    category: str,
    is_long_top: str
):
    job_id = None 
    try:
        bucket = config.TRY_ON_BUCKET

        model_url, bucket_id = await upload_image(user_id, bucket, None, "model.jpg", model_image)

        if garment_image is str:
            job = create_tryon_record(model_url, garment_image, user_id, category, is_long_top, bucket_id)
        else:
            garment_url, _ = await upload_image(user_id, bucket, bucket_id, "garment.jpg", garment_image)
            job = create_tryon_record(model_url, garment_url, user_id, category, is_long_top, bucket_id)
        
        # Job kaydı
        job_id = register_job(job)

        # DB'ye başlangıç kaydını ekle
        resp = await insert_job_record(
            job_id=job_id,
            table_name=config.TRY_ON_TABLE,
            insert_keys=[
                "photo_url",
                "user_id",
                "ai_job_id",
                "status",
                "clothing_url",
                "clothing_type",
                "is_long_top"
            ])

        # Try-on işlemini tetikleme
        loop = asyncio.get_running_loop()
        loop.create_task(trigger_fashn(
            job_id,
            input_json=build_tryon_prediction_input(config.TRY_ON_MODEL_ID, job["photo_url"], job["clothing_url"], False),
            fashn_url=routes.WEBHOOK_TRY_ON,
            prediction_id_name="ai_job_id"
        ))

        return job_id
    except Exception as e:
        if job_id:
            await mark_job_failed(job_id=job_id, table_name=config.TRY_ON_TABLE, failed_fields=["status"])
        raise HTTPException(status_code=500, detail=f"Error in try-on process: {e}")
   
# Handle webhook event for fashn try on
async def handle_tryon_webhook(payload: dict) -> None:
    try:
        status = payload.get("status")

        if status == "completed":
            prediction_id = payload.get("id")
            job_id, job = get_job_by_prediction_id(prediction_id, "ai_job_id")

            await start_background_process(payload, job_id, job, "try-on.jpg", "status", "result_url", "finished", config.TRY_ON_BUCKET ,config.TRY_ON_TABLE)
        else:
            await prediction_failed(payload, config.TRY_ON_TABLE, "ai_job_id", ["status"])
    except Exception as e:
        if job_id:
            await mark_job_failed(job_id, config.TRY_ON_TABLE, ["status"])
        raise HTTPException(status_code=500, detail=f"Webhook processing failed: {e}")
