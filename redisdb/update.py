from redisdb.connection import redis_client
from redisdb.index import create_indexes, delete_indexes
from redisdb.base_ops import hgetall
from redisdb.utils import sanitize_value


async def update_record_field(
    namespace: str,
    record_id: str,
    field: str,
    new_value,
    index_keys: list[str],
    ttl: int = 1800
):
    redis_key = f"{namespace}:{record_id}"

    # 1) Eski record'ı komple çek (restore edilmiş)
    old_job = await hgetall(redis_key)

    if field not in old_job:
        raise ValueError(f"Field '{field}' does not exist in record '{record_id}'")

    # 2) Eski index’i sil (ama sadece indexable ise)
    if field in index_keys:
        await delete_indexes(namespace, old_job, index_keys=[field])

    # 3) Yeni değeri sanitize edip yaz
    sanitized = sanitize_value(new_value)
    await redis_client.hset(redis_key, field, sanitized)

    # 4) Yeni index oluştur (indexable ise)
    new_record = {field: sanitized}
    if field in index_keys:
        await create_indexes(namespace, record_id, new_record, [field], ttl)

    # 5) TTL yenile
    if ttl:
        await redis_client.expire(redis_key, ttl)
