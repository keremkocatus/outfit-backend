from redisdb.connection import redis_client
from redisdb.utils import restore_record, sanitize_value


async def hset_dict(key: str, record: dict, ttl: int):
    """
    mapping kullanmadan, dict'i güvenli bir şekilde Redis'e HSET eden generic fonksiyon.

    Tüm değerler tek tek yazılır -> Redis asyncio sürümlerinde garanti çalışır.
    None değerler otomatik sanitize edilir.
    """
    for field, value in record.items():
        sanitized = sanitize_value(value)
        await redis_client.hset(key, field, sanitized)
    
    await redis_client.expire(key, ttl)


async def hgetall(key: str) -> dict:
    """
    Redis hgetall yapar ve dönen değeri restore ederek gerçek Python tiplerine çevirir.

    Örn:
    "null"  -> None
    "true"  -> True
    "false" -> False
    """
    raw = await redis_client.hgetall(key)

    if not raw:
        return {}

    return restore_record(raw)