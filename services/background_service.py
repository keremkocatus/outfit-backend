from fastapi import HTTPException
from fastapi.concurrency import run_in_threadpool
from db.update import update_in_db
from db.upload_image import upload_image
from registery.registery import update_registry
from services.error_service import mark_job_failed
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
        if isinstance(prediction["output"], list):
            img = await run_in_threadpool(get_image_from_url, prediction["output"][0])
        else:
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
            "job_id",
            job_id
        )
        
        # registry güncelle
        update_registry(job_id, status_field, status_value)
        update_registry(job_id, url_field, result_url)

        return {"status": 200, "response": resp}

    except Exception as e:
        await mark_job_failed(job_id, table_name, [status_field])
        raise HTTPException(status_code=500, detail=f"Error in background process: {e}")


