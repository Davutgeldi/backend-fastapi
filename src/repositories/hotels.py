from repositories.base import BaseRepository
from src.models.hotels import HotelsOrm


class HotelRepository(BaseRepository):
    model = HotelsOrm