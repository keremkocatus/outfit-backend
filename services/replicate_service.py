import replicate
from core import config
from registery.registery import update_registry


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
        await update_registry(job_id, prediction_id_name, prediction.id)

    except Exception as e:
        print(f"[trigger_prediction] Unexpected error for job_id: {job_id}, error: {e}")
        


