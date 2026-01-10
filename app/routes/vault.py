from fastapi import APIRouter, HTTPException
from app.db.supabase import supabase
from pydantic import BaseModel
from typing import List
from datetime import datetime

router = APIRouter(prefix="/vault", tags=["Vault"])

class Secret(BaseModel):
    id: str
    key: str
    value: str # In production this should be write-only or encrypted
    environment: str
    lastUpdated: datetime

class SecretCreate(BaseModel):
    key: str
    value: str
    environment: str

@router.get("/", response_model=List[Secret])
def get_secrets():
    try:
        response = supabase.table("secrets").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error fetching secrets: {e}")
        return []

@router.post("/", response_model=Secret)
def create_secret(secret: SecretCreate):
    try:
        # TODO: Encrypt value before storing
        response = supabase.table("secrets").insert(secret.dict()).execute()
        if response.data:
            return response.data[0]
        raise HTTPException(status_code=400, detail="Could not create secret")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
