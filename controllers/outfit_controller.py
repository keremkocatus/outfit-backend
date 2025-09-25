from fastapi import APIRouter, Form, HTTPException
import core.routes as routes
from services.outfit_service import process_outfit
from typing import List

outfit_router = APIRouter()

@outfit_router.post(routes.OUTFIT_PROCESS)
async def outfit_process(
    user_id: str = Form(...),
    outfit_ids: List[str] = Form(...),
    outfit_urls: List[str] = Form(...)
):
    try:
        resp = await process_outfit(
            user_id=user_id,
            outfit_ids=outfit_ids,
            image_urls=outfit_urls
        )

        return resp
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in outfit controller: {e}"
        )