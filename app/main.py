from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.routers import auth_router, peticion_router

app = FastAPI(title="Monte Sion API")

origins = os.getenv("CORS_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in origins if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router, prefix="/auth", tags=["auth"])
app.include_router(peticion_router.router, prefix="/peticiones", tags=["peticiones"])

@app.get("/")
def root():
    return {"mensaje": "Bienvenido a la API de Monte Sion"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Monte Sion API"}