import httpx
from fastapi import HTTPException
from core import config
from db.update import update_in_db
from registery.registery import update_registry
from services.error_service import mark_job_failed

async def trigger_fashn(job_id: str, input_json: dict, fashn_url: str, prediction_id_name: str) -> None:
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as client:
            response = await client.post(
                fashn_url,
                headers={
                    "Authorization": f"Bearer {config.FASHN_API_KEY}",
                    "Content-Type": "application/json"
                },
                json=input_json
            )

        data = response.json()

        # Prediction başarılı, registry güncelle
        update_registry(job_id, prediction_id_name, data.get("id"))
        await update_in_db(config.TRY_ON_TABLE, {"ai_job_id": data.get("id")}, "job_id", job_id)

    except Exception as e:
        await mark_job_failed(job_id, config.TRY_ON_TABLE, ["status"])
        raise HTTPException(status_code=500, detail=f"Error in trigger fashn: {e}")
