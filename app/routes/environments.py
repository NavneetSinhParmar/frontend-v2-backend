from fastapi import APIRouter, HTTPException
from app.db.supabase import supabase
from app.schemas.models import Environment, EnvironmentCreate
from typing import List

router = APIRouter(prefix="/environments", tags=["Environments"])

@router.get("/", response_model=List[Environment])
def get_environments():
    try:
        response = supabase.table("environments").select("*, servers(*)").execute()
        return response.data
    except Exception as e:
        print(f"Error fetching environments: {e}")
        return []

@router.post("/", response_model=Environment)
def create_environment(env: EnvironmentCreate):
    try:
        response = supabase.table("environments").insert(env.dict()).execute()
        if response.data:
            return response.data[0]
        raise HTTPException(status_code=400, detail="Could not create environment")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
