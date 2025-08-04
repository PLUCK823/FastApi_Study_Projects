from datetime import timedelta, timezone, datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_409_CONFLICT

from ..database import SessionLocal
from ..model import Users

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

SECRET_KEY = "dbaf85d5b99d1203c592d4c9e3d63760abfa4f2198de8d7be41364999f6cd411"
ALGORITHM = "HS256"


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

bcrypt_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(Users).filter(Users.username == username).first()
    if (not user) or (not bcrypt_context.verify(password, user.hash_password)):
        return False
    return user


async def create_access_token(username: str, user_id: int, user_role: str, expires_delta: timedelta):
    encode = {"sub": username, "user_id": user_id, "user_role": user_role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        user_role: str = payload.get("user_role")
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="could not validate user")
    except JWTError:
        raise HTTPException(status_code=401, detail="could not validate user")

    return {"username": username, "user_id": user_id, "user_role": user_role}


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


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/", status_code=HTTP_201_CREATED)
async def create_user(db: db_dependency, user: CreateUser):
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


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Authenticate Failed")
    token = await create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}
