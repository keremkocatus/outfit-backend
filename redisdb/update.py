from redisdb.index import create_indexes, delete_indexes
from redisdb.base_ops import get_dict, set_dict

async def update_record_field(
    namespace: str,
    record_id: str,
    field: str,
    new_value,
    index_keys: list[str] = [],
    ttl: int = 1800
):
    redis_key = f"{namespace}:{record_id}"

    # 1) Eski kayıt
    record = await get_dict(redis_key)

    if field not in record:
        raise ValueError(f"Field '{field}' does not exist in record '{record_id}'")

    # 2) Index sil (field indexable ise)
    if field in index_keys:
        await delete_indexes(namespace, record, [field])

    # 3) Kayıt dict içinde güncelle
    record[field] = new_value  

    # 4) JSON SETEX ile komple yeniden yaz
    await set_dict(redis_key, record, ttl)

    # 5) Yeni index oluştur
    if field in index_keys:
        await create_indexes(namespace, record_id, record, [field], ttl)

    return record
