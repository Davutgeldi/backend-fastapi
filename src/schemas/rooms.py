from pydantic import BaseModel


class Room(BaseModel):
    name: str
    hotel_id: int
    description: str
    price: float
    quantity: int


class RoomAdd(BaseModel):
    name: str
    hotel_id: int
    description: str | None = None
    price: float
    quantity: int


class RoomPatch(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    quantity: int | None = None