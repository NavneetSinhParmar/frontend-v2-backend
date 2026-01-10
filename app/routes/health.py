from fastapi import APIRouter
from app.db.supabase import supabase

router = APIRouter(prefix="/api")

@router.get("/health")
def health_check():
    try:
        # Simple query to check DB connection
        supabase.table("clients").select("count", count="exact", head=True).execute()
        return {
            "status": "ok",
            "message": "API and Database are healthy",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "warning",
            "message": "API is up but Database is unreachable",
            "database": "disconnected",
            "error": str(e)
        }
