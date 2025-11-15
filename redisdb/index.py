from redisdb.connection import redis_client

async def create_indexes(namespace: str, record_id: str, record: dict, index_keys: list[str], ttl: int):
    """
    Verilen record içindeki ilgili index_keys alanlarını tarar,
    değer varsa index oluşturur.

    Örn:
    namespace = "job"
    record_id = "123"
    index_keys = ["prediction_id", "enhance_prediction_id"]

    Oluşacak index key:
    job_index:prediction_id:<value> -> 123
    job_index:enhance_prediction_id:<value> -> 123
    """
    for key in index_keys:
        value = record.get(key)
        if value:
            index_key = f"{namespace}_index:{key}:{value}"
            await redis_client.set(index_key, record_id)
            await redis_client.expire(index_key, ttl)


async def delete_indexes(namespace: str, record_id: str, record: dict, index_keys: list[str]):
    """
    Verilen record içindeki indexlenmiş alanların indexlerini siler.
    """
    for key in index_keys:
        value = record.get(key)
        if value:
            await redis_client.delete(f"{namespace}_index:{key}:{value}")


async def get_id_from_index(namespace: str, key: str, value: str) -> str | None:
    """
    Örn: job_index:prediction_id:<value> -> job_id
    """
    if not value:
        return None

    return await redis_client.get(f"{namespace}_index:{key}:{value}")
