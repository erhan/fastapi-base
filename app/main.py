from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse

from app.admin import admin_app
from app.api import api_app
from app.core.config import settings
from app.core.db import init_db
from app.schemas.base import Error, ResponseModel


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)


@admin_app.exception_handler(RequestValidationError)
@api_app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    error_messages = []
    for error in exc.errors():
        field_name = error["loc"][-1] if error["loc"] else "field"
        message = error["msg"].replace("String", field_name)
        error_messages.append(message)

    return JSONResponse(
        status_code=422,
        content=ResponseModel(
            status="Error",
            message=error_messages[0] if error_messages else "Validation error",
            errors=[{"code": Error.INVALID_REQUEST.code, "message": msg} for msg in error_messages],
        ).model_dump(),
    )


@admin_app.exception_handler(HTTPException)
@api_app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    if isinstance(exc.detail, dict) and "code" in exc.detail:
        return JSONResponse(
            status_code=exc.status_code,
            content=ResponseModel(
                status="Error",
                message=exc.detail["message"],
                errors=[exc.detail],
            ).model_dump(),
        )
    return JSONResponse(
        status_code=exc.status_code,
        content=ResponseModel(
            status="Error",
            message=str(exc.detail),
            errors=[{"code": Error.INTERNAL_ERROR.code, "message": str(exc.detail)}],
        ).model_dump(),
    )


@admin_app.exception_handler(Exception)
@api_app.exception_handler(Exception)
async def general_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content=ResponseModel(
            status="Error",
            message=str(exc),
            errors=[{"code": Error.INTERNAL_ERROR.code, "message": str(exc)}],
        ).model_dump(),
    )


app.mount("/api" + settings.API_VERSION, api_app)
app.mount("/admin" + settings.API_VERSION, admin_app)

router = APIRouter()


@router.get("/", response_class=PlainTextResponse)
def index():
    return PlainTextResponse(content="Hello, world!")


@router.get("/health", response_class=PlainTextResponse)
def health():
    return PlainTextResponse(content="OK")


app.include_router(router)
