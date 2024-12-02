from pydantic import BaseModel

from datetime import date, datetime


class BookingsAdd(BaseModel):
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: float


class Bookings(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    created_at: datetime
    price: float
    

class BookingsAddRequest(BaseModel):
    date_from: date
    date_to: date
    room_id: int


