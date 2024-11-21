from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Date

from src.database import BaseModel


class BookingsOrm(BaseModel):
    __tablename__ = "Booking"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("Rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"))
    date_from: Mapped[Date]
    date_to: Mapped[Date]
    price: Mapped[float]