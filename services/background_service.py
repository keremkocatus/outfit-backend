from fastapi.concurrency import run_in_threadpool
from db.update import update_in_db
from db.upload_image import upload_image
from registery.registery import update_registry
from utils.image_utils import get_image_from_url


async def start_background_process(
    prediction: dict,
    job_id: str,
    job: dict[str, str],
    file_name: str,
    status_field: str,
    url_field: str,
    status_value: str,
    bucket_name: str,
    table_name: str
):
    try:
        # resmi indir
        img = await run_in_threadpool(get_image_from_url, prediction["output"])

        # upload et
        result_url, _ = await upload_image(
            job["user_id"],
            bucket_name,
            job["bucket_id"],
            file_name,
            img
        )

        # DB güncelle
        update_data = {
            url_field: result_url,
            status_field: status_value
        }
        resp = await update_in_db(
            table_name,
            update_data,
            "image_url",
            job["image_url"]
        )
        
        # registry güncelle
        update_registry(job_id, status_field, status_value)
        update_registry(job_id, url_field, result_url)

        return {"status": 200, "response": resp}

    except Exception as error:
        print(f"Error in start_background_process for job {job_id}: {error}")
        return {"status": 500, "error": str(error)}

