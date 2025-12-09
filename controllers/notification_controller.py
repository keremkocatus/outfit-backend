from fastapi import APIRouter, Form, HTTPException
from services.notification_service import save_user_token
import core.routes as routes

notification_router = APIRouter()

@notification_router.post(routes.NOTIFICATION_PUSH_TOKEN)
async def push_user_token(
    user_id: str = Form(...),
    token: str = Form(...)
):
    try:
        await save_user_token(user_id=user_id, token=token)
        return {"status": "success", "message": "Token saved"}

    except Exception as e:
        print(f"[ERROR][push_user_token] Token kaydedilirken hata oluştu: {e}")
        raise HTTPException(
            status_code=500,
            detail="Kullanıcı token kaydedilirken bir hata oluştu."
        )
