from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.health import router as health_router

app = FastAPI(title="Frontend V2 Backend")

# CORS for Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://frontend-v2-xi-flax.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)

@app.get("/")
def root():
    return {"message": "Backend is running successfully"}
