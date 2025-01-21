from pydantic import BaseModel, Field


class AuthRequest(BaseModel):
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")
