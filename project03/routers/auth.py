from datetime import timedelta, timezone, datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_409_CONFLICT

from ..database import SessionLocal
from ..model import Users

router = APIRouter()

SECRET_KEY = "dbaf85d5b99d1203c592d4c9e3d63760abfa4f2198de8d7be41364999f6cd411"
ALGOTITHM = "HS256"


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

bcrypt_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")


def authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(Users).filter(Users.username == username).first()
    if (not user) or (not bcrypt_context.verify(password, user.hash_password)):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGOTITHM)


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


@router.post("/auth/create_user", status_code=HTTP_201_CREATED)
def create_user(db: db_dependency, user: CreateUser):
    if db.query(Users).filter(Users.username == user.username).first() and db.query(Users).filter(
            Users.email == user.email).first():
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail="User already exists")
    new_user = Users(username=user.username,
                     hash_password=bcrypt_context.hash(user.password),
                     email=user.email,
                     first_name=user.first_name,
                     last_name=user.last_name,
                     role=user.role)
    db.add(new_user)
    db.commit()


@router.post("/token")
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return "Authenticate Failed"
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return token
