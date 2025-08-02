from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_409_CONFLICT

from ..database import SessionLocal
from ..model import Users

router = APIRouter()


def get_db():
    """
    创建数据库会话并提供依赖注入

    Yields:
        Session: 数据库会话对象
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class CreateUser(BaseModel):
    username: str = Field(min_length=6)
    password: str = Field(min_length=6)
    email: str = Field(min_length=3, max_length=50)
    first_name: str
    last_name: str
    role: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "new_username",
                "password": "new_password",
                "email": "new_email",
                "first_name": "new_first_name",
                "last_name": "new_last_name",
                "role": "new_role"
            }
        }
    }


@router.post("/auth", status_code=HTTP_201_CREATED)
def create_user(db: db_dependency, user: CreateUser):
    if db.query(Users).filter(Users.username == user.username).first() and db.query(Users).filter(
            Users.email == user.email).first():
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail="User already exists")
    new_user = Users(username=user.username,
                     hash_password=user.password,
                     email=user.email,
                     first_name=user.first_name,
                     last_name=user.last_name,
                     role=user.role)
    db.add(new_user)
    db.commit()
