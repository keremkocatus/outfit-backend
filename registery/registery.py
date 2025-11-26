import uuid
from fastapi import HTTPException
from redisdb.connection import redis_client
from redisdb.index import create_indexes, delete_indexes, get_id_from_index
from redisdb.update import update_record_field
from redisdb.base_ops import set_dict, get_dict
from services.token_service import update_token

TTL = 1800

INDEX_KEYS = [
    "ai_job_id",
    "prediction_id",
    "rembg_prediction_id",
    "enhance_prediction_id",
]

async def register_job(job_record: dict) -> str:
    job_id = str(uuid.uuid4())

    await set_dict(f"job:{job_id}", job_record, TTL)
    await create_indexes("job", job_id, job_record, INDEX_KEYS, TTL)

    return job_id

async def get_job_by_id(job_id):
    return await get_dict(f"job:{job_id}")

async def get_job_by_prediction_id(prediction_id: str, prediction_name: str) -> tuple[str, dict]:
    job_id = await get_id_from_index("job", prediction_name, prediction_id)

    if not job_id:
        raise ValueError(f"No job found with prediction ID: {prediction_id}")
    
    job = await get_dict(f"job:{job_id}")

    if not job:
        raise ValueError(f"Job record missing for prediction ID: {prediction_id}")
    
    return job_id, job


async def update_registry(job_id: str, key: str, new_value):
    try:
        await update_record_field("job", job_id, key, new_value, INDEX_KEYS, TTL)
    except Exception as e:
        raise 

async def get_job_status(job_id: str, status_names: list[str], result_key: str, token_change_amt: int = -1):
    job = await get_dict(f"job:{job_id}")
    if not job:
        raise HTTPException(status_code=404, detail=f"Job_id: {job_id} bulunamadı")
    
    timeout_counter = job.get("timeout_counter")
    if timeout_counter == 15:
        return {
            "job_id": job_id,
            "status": "failed",
        }
    else:
        await update_record_field("job", job_id, "timeout_counter", timeout_counter+1)
        
    # Job bitti mi? (Tüm status alanları "finished" mi?)
    if all(job.get(status) == "finished" for status in status_names):
        result_url = job.get(result_key)
        new_token_balance = await update_token(user_id=job.get("user_id"), change_amt=token_change_amt)

        await redis_client.delete(f"job:{job_id}")
        await delete_indexes("job", job, INDEX_KEYS)

        return {
            "job_id": job_id,
            "status": "finished",
            "result_url": result_url,
            "token_balance": new_token_balance
        }

    # Job fail oldu mu? (Herhangi bir status alanı "failed" ise)
    if any(job.get(status) == "failed" for status in status_names):
        
        await redis_client.delete(f"job:{job_id}")
        await delete_indexes("job", job, INDEX_KEYS)

        return {
            "job_id": job_id,
            "status": "failed",
        }

    return {
        "job_id": job_id,
        "status": "processing"
    }
