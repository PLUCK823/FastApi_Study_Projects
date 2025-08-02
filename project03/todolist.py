from importlib import reload

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List, Annotated

from starlette.exceptions import HTTPException
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

import model
from model import TodoList
from schemas import TodoRequest
from database import SessionLocal, engine

app = FastAPI()

model.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/", status_code=HTTP_200_OK)
def get_all_todos(db: db_dependency):
    return db.query(TodoList).all()


@app.get("/{title}", status_code=HTTP_200_OK)
def get_todo_by_title(title: str, db: db_dependency):
    todo = db.query(TodoList).filter(TodoList.title == title).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.post("/add_todo", status_code=HTTP_201_CREATED)
def add_todo(todo: TodoRequest, db: db_dependency):
    todo_model = TodoList(**todo.model_dump())
    db.add(todo_model)
    db.commit()
