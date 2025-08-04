from fastapi import Depends, Path, APIRouter
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import List, Annotated, Optional

from sqlalchemy.testing.suite.test_reflection import users
from starlette.exceptions import HTTPException
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from .auth import get_current_user
from ..database import SessionLocal
from ..model import TodoList, Users

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

bcrypt_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")


@router.get("/profile", status_code=HTTP_200_OK)
async def get_owner_profile(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(Users).filter(Users.id == user.get("user_id")).first()


@router.put("/update_password", status_code=HTTP_204_NO_CONTENT)
async def update_password(user: user_dependency, db: db_dependency, new_password: str):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    user_model = db.query(Users).filter(Users.id == user.get("user_id")).first()
    user_model.hash_password = bcrypt_context.hash(new_password)
    db.add(user_model)
    db.commit()
