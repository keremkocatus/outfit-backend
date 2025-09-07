import uuid

from fastapi import HTTPException

JOB_REGISTRY: dict[str, dict] = {}

# Register a new background-removal job and return its identifier
def register_job(job_record: dict) -> str:
    job_id = str(uuid.uuid4())
    JOB_REGISTRY[job_id] = job_record

    return job_id

def get_job_by_id(job_id):
    return JOB_REGISTRY.get(job_id)

def get_job_id_by_job(job: dict):
    for jid, record in JOB_REGISTRY.items():
        if record is job or record == job:
            return jid
    raise ValueError("No job found matching the provided job dict")

def get_job_by_prediction_id(prediction_id: str, prediction_name: str) -> tuple[str, dict]:
    for job_id, job in JOB_REGISTRY.items():
        if job.get(prediction_name) == prediction_id:
            return job_id, job

    raise ValueError(f"No job found with prediction ID: {prediction_id}")

def update_registry(job_id: str, key: str, new_value):
    job = JOB_REGISTRY.get(job_id)
    if not job:
        raise ValueError(f"No job found with job ID: {job_id}")

    if key not in job:
        raise KeyError(f"Key '{key}' not found in the job with ID: {job_id}")

    job[key] = new_value

def get_job_status(job_id: str, status_names: list[str], result_key: str):
    job = JOB_REGISTRY.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} bulunamadı")

    # Job bitti mi? (Tüm status alanları "finished" mi?)
    if all(job.get(status) == "finished" for status in status_names):
        result_url = job.get(result_key)
        del JOB_REGISTRY[job_id]

        return {
            "job_id": job_id,
            "status": "finished",
            "result_url": result_url,
        }

    # Job fail oldu mu? (Herhangi bir status alanı "failed" ise)
    if any(job.get(status) == "failed" for status in status_names):
        # DB'den son halini almak istiyorsan buraya get_job_by_id(job_id) eklenebilir
        del JOB_REGISTRY[job_id]

        return {
            "job_id": job_id,
            "status": "failed",
        }

    # Aksi halde iş devam ediyor
    return {
        "job_id": job_id,
        "status": "processing"
    }
