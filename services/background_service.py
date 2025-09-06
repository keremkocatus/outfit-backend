from fastapi.concurrency import run_in_threadpool
from db.upload_image import upload_image
from utils.image_utils import get_image_from_url
from core import config


async def start_enhance_background_process(prediction: dict, job_id: str, job: dict[str, str]):
    try:
        img = await run_in_threadpool(get_image_from_url,prediction["output"])
        result_url, _ = await upload_image(job["user_id"], config.WARDROBE_BUCKET_NAME, job["bucket_id"],"enhanced.png", img)
        
        job["enhance_status"] = "finished"
        job["enhance_url"] = result_url

    except Exception as error:
        print(f"Error in start_enhance_background_process for job {job_id}: {error}")
        raise