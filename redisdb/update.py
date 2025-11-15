from redisdb.connection import redis_client
from redisdb.index import create_indexes, delete_indexes

async def update_record_field(
    namespace: str,
    record_id: str,
    field: str,
    new_value,
    index_keys: list[str],
    ttl: int = 1800
):
    """
    Generic update:
    1. Eski değeri oku
    2. Eğer field index ise eski index sil
    3. Hash içinde yeni değeri yaz
    4. Eğer field index ise yeni index oluştur
    5. TTL gerekiyorsa koru
    """

    redis_key = f"{namespace}:{record_id}"

    # 1) Eski değeri al
    old_value = await redis_client.hget(redis_key, field)

    if old_value is None:
        raise ValueError(f"Cannot update field '{field}' for record '{record_id}' — field does not exist.")

    # 2) Eğer bu field index'lenmişse → eski index'i sil
    if field in index_keys and old_value:
        await delete_indexes(namespace, field, old_value)

    # 3) Hash içinde yeni değeri yaz
    await redis_client.hset(redis_key, field, new_value)

    # 4) Eğer bu field index'lenmişse → yeni index ekle
    if field in index_keys and new_value:
        await create_indexes(namespace, field, new_value, record_id)

    # 5) TTL belirtilmişse job TTL'ı güncelle
    if ttl:
        await redis_client.expire(redis_key, ttl)
