from pydantic import BaseModel


class RoomAdd(BaseModel):
    name: str
    hotel_id: int
    description: str | None = None
    price: float
    quantity: int


class Room(RoomAdd):
   id: int


class RoomAddRequest(BaseModel):
    name: str
    description: str | None = None
    price: float
    quantity: int
    facilities_idsf: list[int] = []


class RoomPatch(BaseModel):
    name: str | None = None
    hotel_id: int | None = None
    description: str | None = None
    price: float | None = None
    quantity: int | None = None


class RoomPatchRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    quantity: int | None = None
    facilities_ids: list[int] = []
