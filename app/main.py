from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.health import router as health_router
from app.routes.clients import router as clients_router
from app.routes.projects import router as projects_router
from app.routes.environments import router as environments_router
from app.routes.monitoring import router as monitoring_router
from app.routes.stats import router as stats_router
from app.routes.ai import router as ai_router
from app.routes.servers import router as servers_router
from app.routes.settings import router as settings_router
from app.routes.vault import router as vault_router

app = FastAPI(title="DragonOps Backend")

# CORS for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://frontend-v2-xi-flax.vercel.app",
        "http://localhost:3000",
        "http://localhost:5173",
        "*" # Allow all for development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(clients_router, prefix="/api")
app.include_router(projects_router, prefix="/api")
app.include_router(environments_router, prefix="/api")
app.include_router(monitoring_router, prefix="/api")
app.include_router(stats_router, prefix="/api")
app.include_router(ai_router, prefix="/api")
app.include_router(servers_router, prefix="/api")
app.include_router(settings_router, prefix="/api")
app.include_router(vault_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "DragonOps Backend is running successfully"}
