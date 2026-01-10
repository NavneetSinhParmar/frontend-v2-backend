from fastapi import APIRouter, HTTPException
from app.db.supabase import supabase
from app.schemas.models import Client, ClientCreate
from typing import List

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.get("/", response_model=List[Client])
def get_clients():
    try:
        response = supabase.table("clients").select("*, projects(*)").execute()
        # Note: simpler structure might be needed depending on how 'projects' are returned
        # Supabase returns related data if foreign keys are set up.
        return response.data
    except Exception as e:
        # For now, return empty list or handle error
        print(f"Error fetching clients: {e}")
        return []

@router.post("/", response_model=Client)
def create_client(client: ClientCreate):
    try:
        response = supabase.table("clients").insert(client.dict()).execute()
        if response.data:
            return response.data[0]
        raise HTTPException(status_code=400, detail="Could not create client")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{client_id}", response_model=Client)
def get_client(client_id: str):
    response = supabase.table("clients").select("*, projects(*)").eq("id", client_id).execute()
    if response.data:
        return response.data[0]
    raise HTTPException(status_code=404, detail="Client not found")
