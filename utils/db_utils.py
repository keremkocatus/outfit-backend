import re

def clean_url(response_url: str):
    if response_url.endswith("?"):
        return response_url[:-1]
    return response_url


def build_storage_path(user_id: str, bucket_id: str, filename: str) -> str:
    return f"{user_id}/{bucket_id}/{filename}"


def extract_public_url(response: dict | str) -> str:
    if isinstance(response, str):
        return clean_url(response)
    return clean_url(response.get("publicURL") or response.get("public_url"))


def extract_bucket_id(image_url: str) -> str:
    """
    Supabase image_url'den UUID olan klasör adını çıkarır.
    Örnek URL:
    https://.../public/deneme/<user_id>/<bucket_id>/<filename>.jpg
    """
    cleaned_url = clean_url(image_url)

    # Regex ile UUID (bucket id) yakala
    match = re.search(r"/([0-9a-fA-F\-]{36})/", cleaned_url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Bucket ID (UUID) not found in the URL.")
    
def table_name(name: str, schema: str) -> str:
    """
    Eğer schema 'prod' ise tablo adı aynı kalır.
    Eğer schema 'test' ise:
      - prefix (ai_, core_, comm_, feat_ vs.) kaldırılır
      - 'test_' ile başlatılır
    """
    if schema == "prod":
        return name

    if schema == "test":
        if "_" in name:
            # ilk '_' işaretinden sonrasını al
            base = name.split("_", 1)[1]
        else:
            base = name
        return f"test_{base}"

    # fallback (başka schema gelirse olduğu gibi dönsün)
    return name

async def check_outfits_missing(outfit_ids: list[str], image_urls: list[str], supabase) -> list[tuple[str, str]]:
    """
    Verilen outfit_id ve image_url listelerini kontrol eder.
    comm_vector_store'da olmayanları (missing) outfit_id ↔ image_url eşleşmiş halde döner.

    Args:
        outfit_ids (list[str]): outfit_id listesi
        image_urls (list[str]): image_url listesi (aynı sırada)

    Returns:
        list[tuple[str, str]]: işleme girecek (outfit_id, image_url) çiftleri
    """
    response = await supabase.rpc(
        "check_outfits_exist",
        {"outfit_ids": outfit_ids}
    ).execute()

    if not response.data:
        return list(zip(outfit_ids, image_urls))  # hiçbiri yoksa hepsi işlenecek

    # DB'de olmayanları al
    missing_ids = {row["outfit_id"] for row in response.data if not row["is_exist"]}

    # outfit_id ↔ image_url eşleştirmesi
    filtered = [
        (o_id, url)
        for o_id, url in zip(outfit_ids, image_urls)
        if o_id in missing_ids
    ]

    return filtered


