from datetime import datetime
from typing import Any

import uuid_utils as uuid
from sqlalchemy import DateTime, Enum, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.core.constants import Status


class BaseModel(DeclarativeBase):
    __abstract__ = True

    id: Mapped[str] = mapped_column(
        String(36),
        unique=True,
        nullable=False,
        default=lambda: str(uuid.uuid7()),
        sort_order=-3,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        sort_order=-2,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        sort_order=-1,
    )

    status: Mapped[Status] = mapped_column(
        Enum(Status),
        nullable=False,
        default=Status.ACTIVE,
        sort_order=100,
    )

    def __repr__(self) -> str:
        attrs = []
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            attrs.append(f"{column.name}={value}")
        return f"{self.__class__.__name__}({', '.join(attrs)})"

    @property
    def dict(self) -> dict[str, Any]:
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
