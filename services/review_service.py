import asyncio
from fastapi import UploadFile, HTTPException
from core import config
from db.insert import insert_job_record
from db.update import update_in_db
from db.upload_image import upload_image
from registery.registery import get_job_by_id, register_job, update_registry
from models.registery_models import create_review_record
from services.openai.generate_review import generate_review 
from services.error_service import mark_job_failed   


# Wardrobe enhance and rembg process
async def process_review_image(
    user_id: str,
    image: UploadFile,
    roast_level: str,
):
    job_id = None 
    try:
        bucket = config.REVIEW_BUCKET
        file_name = "review.jpg"

        public_url, bucket_id = await upload_image(user_id, bucket, None, file_name, image)

        # Job kaydı
        job = create_review_record(public_url, user_id, bucket_id, roast_level)
        job_id = register_job(job)

        # DB'ye başlangıç kaydını ekle
        resp = await insert_job_record(
            job_id=job_id,
            table_name=config.REVIEW_TABLE,
            insert_keys=[
                "image_url",
                "user_id",
                "job_id",
                "status",
                "roast_level"
            ])

        # Review işlemini tetikleme
        loop = asyncio.get_running_loop()
        loop.create_task(start_review_generation(
            job_id=job_id,
            image_url=job["image_url"],
            roast_level=roast_level
        ))

        return job_id
    except Exception as e:
        if job_id:
            await mark_job_failed(
                job_id=job_id,
                table_name=config.REVIEW_TABLE,
                failed_fields=["status"]
            )
        raise HTTPException(status_code=500, detail=f"Error in review image process: {e}")


async def start_review_generation(
    job_id: str,
    image_url: str,
    roast_level: str
): 
    try:
        review_result = await generate_review(image_url, roast_level)
        
        job = get_job_by_id(job_id)
        
        # DB güncelle
        update_data = {
            "result": review_result,
            "status": "finished"
        }
        resp = await update_in_db(
            config.REVIEW_TABLE,
            update_data,
            "image_url",
            job["image_url"]
        )
        
        # registry güncelle
        update_registry(job_id, "status", "finished")
        update_registry(job_id, "result", review_result)

        return {"status": 200, "response": resp}
    except Exception as e:
        if job_id:
            await mark_job_failed(
                job_id=job_id,
                table_name=config.REVIEW_TABLE,
                failed_fields=["status"]
            )
        raise HTTPException(status_code=500, detail=f"Error in start review generation: {e}")
    
    
    
    
    

