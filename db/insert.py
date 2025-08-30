from db.client import get_supabase_client
from registery.registery import get_job_by_id


async def insert_job_record(job_id: str, table_name: str, insert_keys: list[str]) -> dict | None:
    """
    job_id: registery'den job'u alır
    table_name: Supabase tablosu adı
    insert_keys: hangi alanlar insert edilecek (ör: ["image_url", "user_id", "category"])
    """
    try:
        supabase = await get_supabase_client()
        job = get_job_by_id(job_id)

        # sadece parametre olarak verilen keyleri al
        insert_data = {key: job.get(key) for key in insert_keys}
        insert_data["job_id"] = job_id  # job_id'yi hep ekleyelim

        response = (
            await supabase
            .from_(table_name)
            .insert(insert_data)
            .execute()
        )

        return {"status": "Job successfully inserted into database", "response": response}
    except Exception as error:
        print(f"Error in insert_job_record: {error}")
        return None
