from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routers import flood
from core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"🚀 IDRMS AI running on port 8001")
    print(f"📡 Django: {settings.DJANGO_API_URL}")
    yield
    print("🛑 Shutting down")

app = FastAPI(
    title="IDRMS AI Service",
    description="Flood Risk Prediction — Barangay Kauswagan, CDO",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(flood.router)

@app.get("/", tags=["Health"])
def root():
    return {
        "service":  "IDRMS AI",
        "status":   "running",
        "version":  "1.0.0",
        "endpoints": {
            "docs":    "/docs",
            "heatmap": "/ai/flood/heatmap",
            "summary": "/ai/flood/summary",
            "predict": "/ai/flood/predict",
        }
    }

@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "ok",
        "django": settings.DJANGO_API_URL
    }