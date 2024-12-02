from pydantic import BaseModel

from datetime import date


class BookingsAdd(BaseModel):
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: float


class Bookings(BookingsAdd):
    id: int
    

class BookingsAddRequest(BaseModel):
    date_from: date
    date_to: date
    room_id: int


