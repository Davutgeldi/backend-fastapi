from datetime import date

from sqlalchemy import select, func

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room
from src.repositories.utils import rooms_id_for_booking


class RoomRepository(BaseRepository):
    model = RoomsOrm
    schema = Room


    async def get_filterd_by_time(
            self, 
            hotel_id: int, 
            date_from: date, 
            date_to: date,
    ):
        rooms_id_to_get = rooms_id_for_booking(date_from, date_to, hotel_id)
        return await self.get_filtered(RoomsOrm.id.in_(rooms_id_to_get))
