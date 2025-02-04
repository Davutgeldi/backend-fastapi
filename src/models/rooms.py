from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey

from src.database import BaseModel


class RoomsOrm(BaseModel):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    price: Mapped[float]
    quantity: Mapped[int]