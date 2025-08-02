from sqlalchemy import Column, Integer, String
from database import Base


class TodoList(Base):
    __tablename__ = "todolist"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(String(255))
    priority = Column(String(255))
    completed = Column(Integer, default=0)
    
    def __repr__(self):
        return f"<TodoList(id={self.id}, title='{self.title}')>"