from pydantic import BaseModel

from src.schemas.facility import Facility


class RoomAdd(BaseModel):
    name: str
    hotel_id: int
    description: str | None = None
    price: float
    quantity: int


class Room(RoomAdd):
    id: int


class RoomsWithRels(Room):
    facilities: list[Facility]


class RoomAddRequest(BaseModel):
    name: str
    description: str | None = None
    price: float
    quantity: int
    facilities_ids: list[int] = []


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
