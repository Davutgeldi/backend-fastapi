from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room, RoomsWithRels
from src.repositories.utils import rooms_id_for_booking


class RoomRepository(BaseRepository):
    model = RoomsOrm
    schema = Room


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
        return [RoomsWithRels.model_validate(model, from_attributes=True) for model in result.scalars().all()]


    async def get_one_room(
            self, 
            hotel_id: int, 
            room_id: int, 
    ):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(
                self.model.id==room_id, 
                self.model.hotel_id==hotel_id, 
            )
        )
        result = await self.session.execute(query)
        return RoomsWithRels.model_validate(result.scalars().first(), from_attributes=True)
