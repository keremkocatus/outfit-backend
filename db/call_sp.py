from db.client import get_supabase_client

async def call_rpc(function_name: str, params: dict = None):
    try:
        supabase = await get_supabase_client()
        response = supabase.rpc(function_name, params or {}).execute()
        return response.data
    except Exception as error:
        print(f"Error in call_rpc: {error}")
        return None
