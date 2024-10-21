from fastapi import APIRouter, HTTPException, Response

import jwt
from passlib.context import CryptContext 

from datetime import timedelta, timezone, datetime

from src.database import async_session
from src.schemas.users import UserRequestAdd, UserAdd, UserLogin
from src.repositories.users import UsersRepository


router = APIRouter(prefix="/auth", tags=["Authentication & Authorization"])


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/register")
async def register_user(
    data: UserRequestAdd,
):
    hashed_password = pwd_context.hash(data.password)
    new_user = UserAdd(
        first_name=data.first_name, 
        last_name=data.last_name,
        patronymic=data.patronymic,
        phone=data.phone,
        email=data.email,
        hashed_password=hashed_password 
        )
    async with async_session() as session:
        user = await UsersRepository(session).add(new_user)
        await session.commit()
    return {"status":"OK"}


@router.post('/login')
async def login_user(
    data: UserLogin, 
    response: Response,
    ):
    async with async_session() as session:
        user = await UsersRepository(session).get_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="User with that email doesn't exists")
        if not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect password")
        access_token = create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}