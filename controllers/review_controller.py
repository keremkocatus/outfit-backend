from fastapi import APIRouter, File, Form, UploadFile, HTTPException
import core.routes as routes
from registery.registery import get_job_status
from services.review_service import process_review_image

review_router = APIRouter()

@review_router.post(routes.REVIEW_OUTFIT)
async def review_process(
    user_id: str = Form(...),
    image: UploadFile = File(...),   
    roast_level: str = Form(...)
):
    try:
        job_id = await process_review_image(
            user_id=user_id,
            image=image,
            roast_level=roast_level
        )

        return {"job_id": job_id}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in review image process: {e}"
        )

@review_router.get(routes.REVIEW_JOB_STATUS)
async def fetch_job_status(job_id: str):
    try:
        return get_job_status(job_id, ["status"], "result")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching job status for {job_id}: {e}"
        )