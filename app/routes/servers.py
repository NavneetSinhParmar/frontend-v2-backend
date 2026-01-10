from fastapi import APIRouter, HTTPException
from app.db.supabase import supabase
from app.schemas.models import Server, ServerCreate
from typing import List

router = APIRouter(prefix="/servers", tags=["Servers"])

@router.get("/", response_model=List[Server])
def get_servers():
    try:
        response = supabase.table("servers").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error fetching servers: {e}")
        return []

@router.post("/{server_id}/action", response_model=Server)
def perform_server_action(server_id: str, action: str):
    # action can be reboot, start, stop
    # In a real app, this would communicate with AWS/Azure/GCP
    
    # Check if server exists
    response = supabase.table("servers").select("*").eq("id", server_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Server not found")
    
    server = response.data[0]
    
    # Update status based on action
    new_status = server['status']
    if action == 'start':
        new_status = 'running'
    elif action == 'stop':
        new_status = 'stopped'
    elif action == 'reboot':
        new_status = 'rebooting' 
        # In mock, maybe revert to running?
    
    update_response = supabase.table("servers").update({"status": new_status}).eq("id", server_id).execute()
    
    if update_response.data:
        return update_response.data[0]
        
    raise HTTPException(status_code=400, detail="Action failed")
