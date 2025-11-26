import uuid
from fastapi import UploadFile
from db.client import get_supabase_client
from utils.db_utils import build_storage_path, extract_public_url


async def upload_image(user_id: str, bucket: str, bucket_id: str | None, file_name: str, image_file: bytes | UploadFile) -> tuple[str, str] | None:
    try:
        supabase = await get_supabase_client()
        
        if isinstance(image_file, bytes):
            image_data = image_file
        else:
            image_data = await image_file.read()

        if bucket_id is None:
            bucket_id = str(uuid.uuid4())
            
        storage_path = build_storage_path(user_id, bucket_id, file_name)

        await supabase.storage.from_(bucket).upload(
            path=storage_path,
            file=image_data,
            file_options={"cache-control": "3600", "upsert": "true"},
        )

        public_url_response = await supabase.storage.from_(bucket).get_public_url(storage_path)
        public_url = extract_public_url(public_url_response)

        return public_url, bucket_id
    except Exception as error:
        print(f"Error in upload_image: {error}")
        return None, None