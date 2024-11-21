from fastapi import APIRouter, HTTPException, Response


from src.api.dependencies import DBDep
from src.schemas.users import UserRequestAdd, UserAdd, UserLogin
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep


router = APIRouter(prefix="/auth", tags=["Authentication & Authorization"])


@router.post("/register")
async def register_user(
    data: UserRequestAdd,
    db: DBDep
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
    user = await db.users.add(new_user)
    await db.commit()

    return {"status":"OK"}


@router.post('/login')
async def login_user(
    data: UserLogin, 
    response: Response,
    db: DBDep
    ):
    user = await db.users.get_user_with_hashed_password(email=data.email)
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
    db: DBDep
):
    user = await db.users.get_one_or_none(id=user_id)
    return user
    
@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"status": "Logout completed"}