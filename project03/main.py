from fastapi import FastAPI

from . import model
from .database import engine
from .routers import auth, todos

app = FastAPI()

model.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(todos.router)