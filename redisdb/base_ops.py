import json
from redisdb.connection import redis_client


async def set_dict(key: str, record: dict, ttl: int):
    """
    Dict'i JSON string olarak Redis'e SETEX ile yazar.
    None/bool/dict/list gibi tüm tipler JSON içinde güvenle taşınır.
    """
    try:
        json_str = json.dumps(record, ensure_ascii=False)
    except Exception as e:
        raise ValueError(f"Record JSON'a dönüştürülemedi: {e}")

    await redis_client.setex(key, ttl, json_str)



async def get_dict(key: str) -> dict:
    """
    Redis GET → JSON parse → dict olarak döner.
    Key yoksa boş dict döner.
    """
    data = await redis_client.get(key)

    if not data:
        return {}

    try:
        return json.loads(data)
    except Exception:
        # Bozuk JSON varsa ham veri döndür
        return {"raw": data}
