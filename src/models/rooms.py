from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, Text

from src.database import BaseModel


class RoomsOrm(BaseModel):
    __tablename__ = 'Rooms'

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('Hotels.id'))
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]