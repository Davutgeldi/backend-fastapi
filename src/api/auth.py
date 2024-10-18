from fastapi import APIRouter

from passlib.context import CryptContext 

from src.database import async_session
from src.schemas.users import UserRequestAdd, UserAdd 
from src.repositories.users import UsersRepository


router = APIRouter(prefix="/auth", tags=["Authentication & Authorization"])


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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