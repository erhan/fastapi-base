from fastapi import FastAPI

from app.admin.v1.endpoints import router as admin_router
from app.core.config import settings

admin_app = FastAPI(title=settings.PROJECT_NAME + " Admin API", version=settings.ADMIN_API_VERSION)


admin_app.include_router(admin_router)
