from fastapi import Depends, Path, APIRouter
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import List, Annotated, Optional

from starlette.exceptions import HTTPException
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from ..database import SessionLocal
from ..model import TodoList

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


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: Optional[str] = Field(max_length=255)
    priority: str = Field(min_length=1, max_length=10)
    completed: int = Field(default=0, ge=0, le=1)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Todo Title",
                "description": "Todo Description",
                "priority": "High",
                "completed": 0
            }
        }
    }


@router.get("/todos", status_code=HTTP_200_OK)
def get_all_todos(db: db_dependency):
    """
    获取所有待办事项列表

    Args:
        db (Session): 数据库会话对象

    Returns:
        List[TodoList]: 所有待办事项列表
    """
    return db.query(TodoList).all()


@router.get("/todos/{title}", status_code=HTTP_200_OK)
def get_todo_by_title(title: str, db: db_dependency):
    """
    根据标题获取特定待办事项

    Args:
        title (str): 待办事项标题
        db (Session): 数据库会话对象

    Returns:
        TodoList: 匹配的待办事项

    Raises:
        HTTPException: 当找不到指定标题的待办事项时抛出404异常
    """
    todo = db.query(TodoList).filter(TodoList.title == title).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.post("/todos/add_todo", status_code=HTTP_201_CREATED)
def add_todo(todo: TodoRequest, db: db_dependency):
    """
    添加新的待办事项

    Args:
        todo (TodoRequest): 待办事项请求数据
        db (Session): 数据库会话对象

    Returns:
        None: 无返回值，成功创建后返回201状态码
    """
    todo_model = TodoList(**todo.model_dump())
    db.add(todo_model)
    db.commit()


@router.put("/todos/update_todo/{todo_id}", status_code=HTTP_204_NO_CONTENT)
def update_todo(db: db_dependency, todo: TodoRequest, todo_id: int = Path(gt=0)):
    """
    根据ID更新待办事项

    Args:
        db (Session): 数据库会话对象
        todo (TodoRequest): 待办事项更新数据
        todo_id (int): 待办事项ID，必须大于0

    Returns:
        None: 无返回值，成功更新后返回204状态码

    Raises:
        HTTPException: 当找不到指定ID的待办事项时抛出404异常
    """
    todo_model = db.query(TodoList).filter(TodoList.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    # 更新现有记录的字段而不是创建新实例
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.completed = todo.completed

    db.add(todo_model)
    db.commit()


@router.delete("/todos/delete_todo/{todo_id}", status_code=HTTP_204_NO_CONTENT)
def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    """
    根据ID删除待办事项

    Args:
        db (Session): 数据库会话对象
        todo_id (int): 待办事项ID，必须大于0

    Returns:
        None: 无返回值，成功删除后返回204状态码

    Raises:
        HTTPException: 当找不到指定ID的待办事项时抛出404异常
    """
    todo_model = db.query(TodoList).filter(TodoList.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo_model)
    db.commit()
