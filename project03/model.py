from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255))
    hash_password = Column(String(255))
    email = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    is_active = Column(Integer, default=1)
    role = Column(String(255))

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"


class TodoList(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(String(255))
    priority = Column(Integer)
    completed = Column(Integer, default=0)
    owner_id = Column(Integer, ForeignKey("users.id"))

    def __repr__(self):
        return f"<TodoList(id={self.id}, title='{self.title}')>"
