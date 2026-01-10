from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

# Enums could be useful but strings are easier for rapid prototyping

class Server(BaseModel):
    id: str
    name: str
    type: str  # EC2, RDS, S3, etc.
    status: str
    cpu: str
    memory: str
    region: str
    privateIp: str

class Monitor(BaseModel):
    id: str
    name: str
    url: str
    status: str
    responseTime: float
    uptime: float
    lastCheck: datetime
    incidents: int
    downtimeToday: str

class EnvironmentResources(BaseModel):
    cpu: str
    memory: str
    storage: str

class Environment(BaseModel):
    id: str
    name: str
    projectId: str
    # client: str  # Could be name or ID? Keep simple for now
    status: str
    health: str
    url: str
    lastDeployment: datetime
    version: str
    resources: EnvironmentResources
    services: List[str] = []
    uptime: float
    servers: List[Server] = []

class Project(BaseModel):
    id: str
    name: str
    clientId: str
    description: str
    status: str
    progress: int
    environments: List[Environment] = []
    team: List[str] = []
    lastDeployment: datetime
    repository: str
    technology: List[str] = []
    createdAt: datetime

class Client(BaseModel):
    id: str
    name: str
    description: str
    projectCount: int
    environmentCount: int
    status: str
    lastActivity: datetime
    projects: List[Project] = []
    # environments: List[Environment] = [] # This might be redundant if projects have environments

class ClientCreate(BaseModel):
    name: str
    description: str
    status: str = "active"

class ProjectCreate(BaseModel):
    name: str
    clientId: str
    description: str
    repository: str
    technology: List[str] = []

class EnvironmentCreate(BaseModel):
    name: str
    projectId: str
    url: str
    version: str
    resources: EnvironmentResources

class ServerCreate(BaseModel):
    name: str
    type: str
    region: str
    privateIp: str
    environmentId: Optional[str] = None # Linking to environment if needed
