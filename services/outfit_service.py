import numpy as np
from fastapi import HTTPException
from fastapi.concurrency import run_in_threadpool
from core import config
from db.client import get_supabase_client
from db.insert import insert_to_db
from utils.image_utils import extract_embedding, load_image_from_url, normalize_embedding, prepare_image, resize_image  
from utils.db_utils import check_outfits_missing 

BATCH_SIZE = 32

async def process_outfit(user_id: str, outfit_ids: list[str], image_urls: list[str]):
    try:
        results = []

        # 1. DB’de olmayan outfit_id ↔ image_url çiftlerini al
        supabase = await get_supabase_client()
        to_process = await check_outfits_missing(outfit_ids, image_urls, supabase)

        if not to_process:
            return {"status": "success", "inserted": 0, "skipped": len(outfit_ids)}

        # 2. Batch halinde işleme
        for i in range(0, len(to_process), BATCH_SIZE):
            batch = to_process[i:i + BATCH_SIZE]
            batch_imgs, meta_data = [], []

            # Download + Resize + Preprocess
            for o_id, img_url in batch:
                img = await run_in_threadpool(load_image_from_url, img_url)
                resized = await run_in_threadpool(resize_image, img, (224, 224))
                arr = await run_in_threadpool(prepare_image, resized)
                batch_imgs.append(arr)
                meta_data.append({
                    "user_id": user_id,
                    "image_url": img_url,
                    "outfit_id": o_id
                })

            # Batch stack → (N,224,224,3)
            batch_input = np.vstack(batch_imgs)

            # Feature extraction 
            batch_embeddings = await run_in_threadpool(extract_embedding, batch_input)

            # Insert DB
            for meta, emb in zip(meta_data, batch_embeddings):
                emb_norm = normalize_embedding(emb)
                data = {
                    "vector": emb_norm.tolist(),
                    "outfit_id": meta["outfit_id"]
                }
                db_result = await insert_to_db(config.VECTOR_STORE, data)
                results.append(db_result)

        return {
            "status": "success",
            "inserted": len(results),
            "skipped": len(outfit_ids) - len(to_process)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in outfit service: {e}")
