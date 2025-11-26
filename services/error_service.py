from db.update import update_in_db
from registery.registery import get_job_by_prediction_id, update_registry

async def mark_job_failed(
    job_id: str,
    table_name: str,
    failed_fields: list[str],
) -> None:
    """
    Genel hata işleme fonksiyonu.
    
    Args:
        job_id (str): Hatalı olan job'un ID'si
        table_name (str): Supabase tablosu
        failed_fields (list[str]): Failed yapılacak alanların listesi
        registry_updater (callable, optional): İlgili registry güncelleme fonksiyonu.
            Örn: update_registry, update_edit_registry, update_tryon_registry
    """
    # Supabase update dict oluştur
    update_data = {field: "failed" for field in failed_fields}

    # Registry de güncelle
    for field in failed_fields:
        await update_registry(job_id, field, "failed")

    # Supabase tablosunda update et
    resp = await update_in_db(table_name, update_data, "job_id", job_id)

async def prediction_failed(payload: dict, table_name: str, prediction_id_name: str, failed_fileds: list[str]):
    prediction_id = payload.get("id")
    job_id, _ = await get_job_by_prediction_id(prediction_id, prediction_id_name)

    await mark_job_failed(job_id, table_name, failed_fileds)