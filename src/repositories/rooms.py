from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.repositories.utils import rooms_id_for_booking
from src.repositories.mappers.mappers import RoomDataMapper, RoomDataWithRelsMapper


class RoomRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper

    async def get_filtered_by_time(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):
        rooms_id_to_get = rooms_id_for_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_id_to_get))
        )
        result = await self.session.execute(query)
        return [
            RoomDataWithRelsMapper.map_to_domain_entity(model) for model in result.scalars().all()
        ]

    async def get_one_room(
        self,
        hotel_id: int,
        room_id: int,
    ):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(
                self.model.id == room_id,
                self.model.hotel_id == hotel_id,
            )
        )
        result = await self.session.execute(query)
        room = result.scalars().first()
        return RoomDataWithRelsMapper.map_to_domain_entity(room)
