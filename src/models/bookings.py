from datetime import date

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property

from src.database import BaseModel


class BookingsOrm(BaseModel):
    __tablename__ = "Booking"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("Rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"))
    date_from: Mapped[date]
    date_to: Mapped[date]
    price: Mapped[float]

    @hybrid_property
    def total_cost(self) -> int:
        return self.price * (self.date_to - self.date_from).days