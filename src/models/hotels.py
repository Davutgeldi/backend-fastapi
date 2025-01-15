from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from src.database import BaseModel


class HotelsOrm(BaseModel):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(String(50))
    name: Mapped[str]