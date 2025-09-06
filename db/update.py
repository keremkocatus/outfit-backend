from db.client import get_supabase_client

async def update_in_db(table: str, updated_data: dict, unique_key, unique_value):
    try:
        supabase = await get_supabase_client()
        response = await supabase.from_(table).update(updated_data).eq(unique_key, unique_value).execute()

        return {"status": "Data successfully updated in database", "response": response}
    except Exception as error:
        print(f"Error in insert_to_db: {error}")