from db.update import update_in_db
from core import config
from datetime import datetime

async def save_user_token(user_id: str, token: str):
    try:
        data = {"expo_push_token": token,
                "updated_at": datetime.now()}
        
        await update_in_db(
                table=config.USERS_DEVICES,
                updated_data=data,
                unique_key="user_id",
                unique_value=user_id)
        
    except Exception as e:
        print(f"[ERROR][save_user_token] Kullanıcı ({user_id}) için token kaydedilemedi: {e}")
        raise
