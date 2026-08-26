from fastapi import APIRouter

from app.api.v1.endpoints import health, auth, url_analysis

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(url_analysis.router, tags=["analysis"])