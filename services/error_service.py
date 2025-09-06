from db.update import update_in_db
from registery.registery import update_registry

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
        update_registry(job_id, field, "failed")

    # Supabase tablosunda update et
    resp = await update_in_db(table_name, update_data, "job_id", job_id)
