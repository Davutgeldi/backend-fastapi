from pydantic import BaseModel, ConfigDict


class HotelAdd(BaseModel):
    city: str
    name: str


class Hotel(HotelAdd):
    id: int

    # Can use this if we don't wanna duplicate code, but prefer to write it in BaseRepository
    # model_config = ConfigDict(from_attributes=True)


class HotelPatch(BaseModel):
    city: str | None = None
    name: str | None = None