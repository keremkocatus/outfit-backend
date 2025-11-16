from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from core import routes, rule_engine
from registery.registery import get_job_status
from services.review_service import process_review_image
from services.token_service import check_token

review_router = APIRouter()

@review_router.post(routes.REVIEW_OUTFIT)
async def review_process(
    user_id: str = Form(...),
    image: UploadFile = File(...),   
    roast_level: str = Form(...)
):
    try:
        if not await check_token(user_id=user_id, required_token_count=rule_engine.REVIEW_REQUIRED_TOKEN):
            raise HTTPException(
                status_code=402,
                detail={"Token not enough."}
            )
        
        job_id = await process_review_image(
            user_id=user_id,
            image=image,
            roast_level= roast_level
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
        return await get_job_status(job_id, ["status"], "result", rule_engine.REVIEW_TOKEN_CHNG_AMT)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching job status for {job_id}: {e}"
        )