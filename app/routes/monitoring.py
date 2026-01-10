from fastapi import APIRouter, HTTPException
from app.db.supabase import supabase
from app.schemas.models import Monitor
from typing import List

router = APIRouter(prefix="/monitoring", tags=["Monitoring"])

@router.get("/", response_model=List[Monitor])
def get_monitors():
    try:
        response = supabase.table("monitors").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error fetching monitors: {e}")
        return []
