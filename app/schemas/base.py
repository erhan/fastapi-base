from enum import Enum
from typing import Any, Generic, Optional, TypeVar

from fastapi import HTTPException
from pydantic import BaseModel


class Error(Enum):
    INTERNAL_ERROR = 500, "Internal server error", 500
    NOT_FOUND = 404, "Requested resource not found", 404
    INVALID_REQUEST = 400, "Invalid request", 400

    def __init__(self, code: int, message: str, status_code: int):
        self.code = code
        self.message = message
        self.status_code = status_code

    def exception(self, message: Optional[str] = None) -> None:
        raise HTTPException(
            status_code=self.status_code,
            detail={
                "code": self.code,
                "message": message or self.message,
            },
        )


T = TypeVar("T")


class ResponseModel(BaseModel, Generic[T]):
    status: str = "Success"
    message: str = "Successfully processed"
    data: T | None = None
    errors: list[dict[str, Any]] | None = None

    @classmethod
    def error(cls, error: Error, message: str | None = None) -> "ResponseModel":
        return cls(
            status="Error",
            message=message or error.message,
            errors=[
                {
                    "code": error.code,
                    "message": message or error.message,
                },
            ],
        )
