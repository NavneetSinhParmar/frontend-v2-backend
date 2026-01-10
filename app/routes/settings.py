from fastapi import APIRouter, HTTPException
from app.db.supabase import supabase
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/settings", tags=["Settings"])

class Setting(BaseModel):
    id: str
    key: str
    value: str
    description: str

class SettingUpdate(BaseModel):
    value: str

@router.get("/", response_model=List[Setting])
def get_settings():
    try:
        response = supabase.table("settings").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error fetching settings: {e}")
        return []

@router.put("/{setting_id}", response_model=Setting)
def update_setting(setting_id: str, setting: SettingUpdate):
    try:
        response = supabase.table("settings").update({"value": setting.value}).eq("id", setting_id).execute()
        if response.data:
            return response.data[0]
        raise HTTPException(status_code=404, detail="Setting not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
