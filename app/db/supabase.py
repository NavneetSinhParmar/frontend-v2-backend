from supabase import create_client, Client
from app.core.config import get_settings

settings = get_settings()

def get_supabase_client() -> Client:
    # In a real scenario, we might want to handle missing keys gracefully or error out
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        print("Warning: SUPABASE_URL or SUPABASE_KEY not set.")
    
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

supabase = get_supabase_client()
