from fastapi import APIRouter

from app.schemas.base import ResponseModel
from app.schemas.request import AuthRequest
from app.schemas.response import AuthResponse

router = APIRouter()


@router.post("/login", response_model=ResponseModel[AuthResponse])
async def login(_: AuthRequest):
    return ResponseModel(message="Transaction initialized", data=AuthResponse(token=""))
