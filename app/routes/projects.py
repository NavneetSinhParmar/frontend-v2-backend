from fastapi import APIRouter, HTTPException
from app.db.supabase import supabase
from app.schemas.models import Project, ProjectCreate
from typing import List

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("/", response_model=List[Project])
def get_projects():
    try:
        response = supabase.table("projects").select("*, environments(*)").execute()
        return response.data
    except Exception as e:
        print(f"Error fetching projects: {e}")
        return []

@router.post("/", response_model=Project)
def create_project(project: ProjectCreate):
    try:
        response = supabase.table("projects").insert(project.dict()).execute()
        if response.data:
            return response.data[0]
        raise HTTPException(status_code=400, detail="Could not create project")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{project_id}", response_model=Project)
def get_project(project_id: str):
    response = supabase.table("projects").select("*, environments(*)").eq("id", project_id).execute()
    if response.data:
        return response.data[0]
    raise HTTPException(status_code=404, detail="Project not found")
