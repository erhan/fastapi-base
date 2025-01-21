from fastapi import FastAPI

from app.api.v1.endpoints import router as api_router
from app.core.config import settings

api_app = FastAPI(title=settings.PROJECT_NAME + " API", description=settings.PROJECT_NAME + " API", version=settings.VERSION)


api_app.include_router(api_router)
