from fastapi.concurrency import run_in_threadpool
from db.update import update_in_db
from db.upload_image import upload_image
from registery.registery import update_registry
from utils.image_utils import get_image_from_url
from core import config


async def start_enhance_background_process(prediction: dict, job_id: str, job: dict[str, str]):
    try:
        img = await run_in_threadpool(get_image_from_url,prediction["output"])
        result_url, _ = await upload_image(job["user_id"], config.WARDROBE_BUCKET_NAME, job["bucket_id"],"enhanced.png", img)
        
        update_registry(job_id, "enhance_status", "finished")
        update_registry(job_id, "enhanced_image_url", result_url)

        update_data = {
            "enhanced_image_url": result_url,
            "enhance_status": "finished"
        }

        resp = await update_in_db(config.WARDROBE_TABLE_NAME, update_data, "image_url", job["image_url"])

        return {"status": 200, "response": resp}
    except Exception as error:
        print(f"Error in start_enhance_background_process for job {job_id}: {error}")

async def start_rembg_background_process(prediction: dict, job_id: str, job: dict[str, str]):
    try:
        img = await run_in_threadpool(get_image_from_url,prediction["output"])
        result_url, _ = await  upload_image(job["user_id"], config.WARDROBE_BUCKET_NAME, job["bucket_id"], "rembg.png", img)

        update_registry(job_id, "rembg_status", "finished")
        update_registry(job_id, "removed_bg_image_url", result_url)

        update_data = {
            "removed_bg_image_url": result_url,
            "rembg_status": "finished"
        }

        resp = await update_in_db(config.WARDROBE_TABLE_NAME, update_data, "image_url", job["image_url"])

        return {"status": 200, "response": resp}
    except Exception as error:
        print(f"Error in start_fast_background_process for job {job_id}: {error}")