import uuid

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

def update_registry(job_id: str, key: str, new_value):
    job = JOB_REGISTRY.get(job_id)
    if not job:
        raise ValueError(f"No job found with job ID: {job_id}")

    if key not in job:
        raise KeyError(f"Key '{key}' not found in the job with ID: {job_id}")

    job[key] = new_value

