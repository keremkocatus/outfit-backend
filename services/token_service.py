from db.call_sp import call_rpc

async def check_token(user_id: str, required_token_count: int = 1) -> bool:
    """Kullanıcının belirtilen sayıda token'a sahip olup olmadığını kontrol eder."""
    
    params = {"user_id": user_id}
    user_token = await call_rpc("get_user_token", params)

    if isinstance(user_token, int):
        return user_token >= required_token_count
    
    return False

async def update_token(user_id: str, change_amt: int = -1) -> int | None:
    """Bir kullanıcının token sayısını atomik olarak günceller ve yeni değeri döndürür."""

    params = {
        "p_user_id": user_id,
        "amount_to_change": change_amt
    }
    
    new_token_value = await call_rpc("modify_user_token", params)

    if isinstance(new_token_value, int):
        return new_token_value

    return None