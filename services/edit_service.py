import asyncio
from fastapi import UploadFile, HTTPException
from core import config, routes
from db.insert import insert_job_record
from db.upload_image import upload_image
from models.prediction_models import build_edit_prediction_input
from registery.registery import get_job_by_prediction_id, register_job
from models.registery_models import create_edit_record
from services.background_service import start_background_process
from services.replicate_service import trigger_prediction
from services.error_service import mark_job_failed   


# Wardrobe enhance and rembg process
async def process_edit_image(
    user_id: str,
    image: UploadFile,
    prompt: str,
):
    job_id = None 
    try:
        bucket = config.EDIT_BUCKET_NAME
        file_name = "original.jpg"

        public_url, bucket_id = await upload_image(user_id, bucket, None, file_name, image)

        # Job kaydı
        job = create_edit_record(public_url, user_id, bucket_id, prompt)
        job_id = register_job(job)

        # DB'ye başlangıç kaydını ekle
        resp = await insert_job_record(
            job_id=job_id,
            table_name=config.EDIT_TABLE_NAME,
            insert_keys=[
                "image_url",
                "user_id",
                "job_id",
                "status",
                "prompt"
            ])

        # Edit işlemini tetikleme
        loop = asyncio.get_running_loop()
        loop.create_task(trigger_prediction(
            job_id,
            model_id=config.EDIT_MODEL_ID,
            webhook_url=f"{config.APP_URL}{routes.WEBHOOK_IMAGE_EDIT}",
            prediction_input=build_edit_prediction_input(prompt, job["image_url"]),
            prediction_id_name="prediction_id"
        ))

        return job_id
    except Exception as e:
        if job_id:
            await mark_job_failed(
                job_id=job_id,
                table_name=config.EDIT_TABLE_NAME,
                failed_fields=["status"]
            )
        raise HTTPException(status_code=500, detail=f"Error in edit image process: {e}")


# Handle webhook event for enhancement prediction completion
async def handle_edit_webhook(payload: dict) -> None:
    job_id = None
    try:
        status = payload.get("status")

        if status == "succeeded":
            prediction_id = payload.get("id")
            job_id, job = get_job_by_prediction_id(prediction_id, "prediction_id")

            await start_background_process(payload, job_id, job, "edited.jpg", "status", "edited_image_url", "finished", config.EDIT_BUCKET_NAME ,config.EDIT_TABLE_NAME)

            return job_id, job
        else:
            prediction_id = payload.get("id")
            job_id, _ = get_job_by_prediction_id(prediction_id, "prediction_id")

            if job_id:
                await mark_job_failed(job_id, config.EDIT_TABLE_NAME, ["status"])
    except Exception as e:
        if job_id:
            await mark_job_failed(job_id, config.EDIT_TABLE_NAME, ["status"])
        raise HTTPException(status_code=500, detail=f"Webhook processing failed edit image: {e}")
    

