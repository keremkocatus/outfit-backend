import replicate
from fastapi import HTTPException

from core import config
from registery.registery import get_job_by_id, update_registry
from utils.prompt_utils import get_enhance_prompt

replicate_client = replicate.Client(api_token=config.REPLICATE_API_KEY)

# Submit an asynchronous enhancement prediction request to Replicate
async def trigger_prediction(job_id: str, model_id: str, webhook_url: str, prediction_input: dict, prediction_id_name: str) -> None:
    try:
        prediction = await replicate_client.predictions.async_create(
            version=model_id,
            input=prediction_input,
            webhook=webhook_url,
            webhook_events_filter=["completed"],
        )

        # Prediction başarılı, registry güncelle
        update_registry(job_id, f"{prediction_id_name}", prediction.id)

    except Exception as e:
        print(f"[trigger_prediction] Unexpected error for job_id: {job_id}, error: {e}")
        


