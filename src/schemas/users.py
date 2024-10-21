from pydantic import BaseModel, EmailStr


class UserRequestAdd(BaseModel):
    first_name: str
    last_name: str
    patronymic: str | None = None
    phone: str | None = None
    email: EmailStr
    password: str


class UserAdd(BaseModel):
    first_name: str
    last_name: str
    patronymic: str | None = None
    phone: str | None = None
    email: EmailStr
    hashed_password: str


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    patronymic: str | None = None 
    email: EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserHashedPassword(User):
    hashed_password: str

