import asyncio
from fastapi import UploadFile, HTTPException
from core import config, routes
from db.insert import insert_job_record
from db.upload_image import upload_image
from models.prediction_models import build_enhance_prediction_input, build_rembg_prediction_input
from registery.registery import get_job_by_id, get_job_by_prediction_id, register_job, update_registry
from models.registery_models import create_wardrobe_record
from services.background_service import start_background_process
from services.caption_service import process_caption_for_job
from services.replicate_service import trigger_prediction
from utils.extrack_utils import extract_id
from services.error_service import mark_job_failed   


# Wardrobe enhance and rembg process
async def process_wardrobe_image(
    user_id: str,
    clothe_image: UploadFile,
    category: str,
    is_long_top: bool,
    is_enhance: bool,
):
    job_id = None 
    try:
        bucket = config.WARDROBE_BUCKET_NAME
        file_name = f"{category}.jpg"

        public_url, bucket_id = await upload_image(user_id, bucket, None, file_name, clothe_image)

        # Job kaydı
        job = create_wardrobe_record(public_url, user_id, bucket_id, category, is_long_top)
        job_id = await register_job(job)

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
        
        await update_registry(job_id, "wardrobe_item_id", extract_id(resp["response"].data))

        # Enhance veya Rembg tetikleme
        loop = asyncio.get_running_loop()
        if is_enhance:
            loop.create_task(trigger_prediction(
                job_id,
                model_id=config.ENHANCE_MODEL_ID,
                webhook_url=f"{config.APP_URL}{routes.WEBHOOK_ENHANCE}",
                prediction_input=build_enhance_prediction_input(category, job["image_url"]),
                prediction_id_name="enhance_prediction_id"
            ))
        else:
            # Start Caption
            loop.create_task(process_caption_for_job(job_id, job))

            # Start Rembg
            loop.create_task(trigger_prediction(
                job_id,
                model_id=config.REMBG_MODEL_ID,
                webhook_url=f"{config.APP_URL}{routes.WEBHOOK_FAST_REMBG}",
                prediction_input=build_rembg_prediction_input(job["image_url"]),
                prediction_id_name="rembg_prediction_id"
            ))

        return job_id

    except Exception as e:
        if job_id:
            await mark_job_failed(
                job_id=job_id,
                table_name=config.WARDROBE_TABLE_NAME,
                failed_fields=["enhance_status", "rembg_status", "caption_status"]
            )
        raise HTTPException(status_code=500, detail=f"Error in wardrobe process: {e}")


# Handle webhook event for enhancement prediction completion
async def handle_enhance_webhook(payload: dict) -> None:
    job_id = None
    try:
        status = payload.get("status")

        if status == "succeeded":
            prediction_id = payload.get("id")
            job_id, job = await get_job_by_prediction_id(prediction_id, "enhance_prediction_id")

            await start_background_process(
                payload, job_id, job,
                file_name="enhanced.png",
                status_field="enhance_status",
                url_field="enhanced_image_url",
                status_value="finished",
                bucket_name=config.WARDROBE_BUCKET_NAME,
                table_name=config.WARDROBE_TABLE_NAME
            )

            job = await get_job_by_id(job_id)

            loop = asyncio.get_running_loop()
            # Start Caption
            loop.create_task(process_caption_for_job(job_id, job))
            
            # Start Rembg
            loop.create_task(trigger_prediction(
                job_id,
                model_id=config.REMBG_MODEL_ID,
                webhook_url=f"{config.APP_URL}{routes.WEBHOOK_FAST_REMBG}",
                prediction_input=build_rembg_prediction_input(job["enhanced_image_url"]),
                prediction_id_name="rembg_prediction_id"
            ))

            return job_id, job
        else:
            prediction_id = payload.get("id")
            job_id, _ = await get_job_by_prediction_id(prediction_id, "enhance_prediction_id")
            if job_id:
                await mark_job_failed(job_id, config.WARDROBE_TABLE_NAME, ["enhance_status"])
    except Exception as e:
        if job_id:
            await mark_job_failed(job_id, config.WARDROBE_TABLE_NAME, ["enhance_status"])
        raise HTTPException(status_code=500, detail=f"Webhook processing failed enhance: {e}")
    

# Handle webhook event for fast prediction completion
async def handle_rembg_webhook(payload: dict):
    job_id = None
    try:
        prediction_id = payload["id"]
        job_id, job = await get_job_by_prediction_id(prediction_id, "rembg_prediction_id")

        loop = asyncio.get_running_loop()
        loop.create_task(start_background_process(
                            payload, job_id, job,
                            file_name="rembg.png",
                            status_field="rembg_status",
                            url_field="removed_bg_image_url",
                            status_value="finished",
                            bucket_name=config.WARDROBE_BUCKET_NAME,
                            table_name=config.WARDROBE_TABLE_NAME
                        ))

        return job_id
    except Exception as e:
        if job_id:
            await mark_job_failed(job_id, config.WARDROBE_TABLE_NAME, ["rembg_status"])
        raise HTTPException(status_code=500, detail=f"Webhook processing failed rembg: {e}")
