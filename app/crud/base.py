from typing import Any, Generic, Optional, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.constants import Status
from app.schemas.base import Error

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> ModelType:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_or_error(self, db: Session, id: Any) -> ModelType:
        obj = db.query(self.model).filter(self.model.id == id).first()
        if not obj:
            raise Error.NOT_FOUND.exception(f"{self.model.__name__} not found")
        return obj

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        status: Optional[Status] = None,
    ) -> list[ModelType]:
        query = db.query(self.model)
        if status is not None:
            query = query.filter(self.model.status == status)
        return query.offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: CreateSchemaType, **kwargs) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, **kwargs)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, dict[str, Any]],
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        if obj:
            obj.status = Status.PASSIVE
            db.add(obj)
            db.commit()
            db.refresh(obj)
        return obj

    def hard_delete(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def restore(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        if obj and obj.status == Status.PASSIVE:
            obj.status = Status.ACTIVE
            db.add(obj)
            db.commit()
            db.refresh(obj)
        return obj
