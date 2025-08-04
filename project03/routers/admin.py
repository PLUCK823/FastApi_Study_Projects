from fastapi import Depends, Path, APIRouter
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import List, Annotated, Optional

from sqlalchemy.testing.suite.test_reflection import users
from starlette.exceptions import HTTPException
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from .auth import get_current_user
from ..database import SessionLocal
from ..model import TodoList

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/", status_code=HTTP_200_OK)
async def get_all_todos(user: user_dependency, db: db_dependency):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(TodoList).all()


@router.get("/{todo_id}", status_code=HTTP_200_OK)
async def get_todo_by_id(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication Failed")
    todo = db.query(TodoList).filter(TodoList.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Not Found!")
    return todo
