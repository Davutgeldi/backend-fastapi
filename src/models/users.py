from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer

from src.database import BaseModel


class UsersOrm(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    patronymic: Mapped[str] = mapped_column(String(30), nullable=True)
    email: Mapped[str] = mapped_column(String(30), unique=True)
    phone: Mapped[int] = mapped_column(String(15), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(200))