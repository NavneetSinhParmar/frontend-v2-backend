from fastapi import APIRouter
from app.db.supabase import supabase

router = APIRouter(prefix="/stats", tags=["Stats"])

@router.get("/dashboard")
def get_dashboard_stats():
    try:
        clients_count = supabase.table("clients").select("*", count="exact", head=True).execute().count
        projects_count = supabase.table("projects").select("*", count="exact", head=True).execute().count
        servers_count = supabase.table("servers").select("*", count="exact", head=True).execute().count
        
        # Determine system health based on monitors or general status
        # For mock/simulation, we can assume:
        health_score = 98 # 98% healthy
        
        return {
            "clients": clients_count,
            "projects": projects_count,
            "servers": servers_count,
            "health": health_score,
            "recent_activity": [] # TODO: activity log table
        }
    except Exception as e:
        print(f"Error fetching stats: {e}")
        return {
            "clients": 0,
            "projects": 0,
            "servers": 0,
            "health": 100,
            "recent_activity": []
        }
