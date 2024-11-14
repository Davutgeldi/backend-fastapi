from fastapi import APIRouter, HTTPException, Response


from src.database import async_session
from src.schemas.users import UserRequestAdd, UserAdd, UserLogin
from src.repositories.users import UsersRepository
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep


router = APIRouter(prefix="/auth", tags=["Authentication & Authorization"])


@router.post("/register")
async def register_user(
    data: UserRequestAdd,
):
    hashed_password = AuthService().hash_password(data.password)
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
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect password")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}
    

@router.get("/me")
async def get_me(
    user_id: UserIdDep,
):
    async with async_session() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        return user
    
@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"status": "Logout completed"}