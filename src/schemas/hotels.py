from pydantic import BaseModel


class Hotel(BaseModel):
    city: str
    name: str


class HotelPATCH(BaseModel):
    city: str | None = None
    name: str | None = None