from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room


class RoomRepository(BaseRepository):
    model = RoomsOrm
    schema = Room


