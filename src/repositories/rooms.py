from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room, RoomsWithRelationships
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
        return [RoomsWithRelationships.model_validate(model, from_attributes=True) for model in result.scalars().all()]
    

    async def get_one_or_none(
            self,
            hotel_id: int,
            room_id: int,
    ):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(
                self.model.hotel_id==hotel_id, 
                self.model.id==room_id, 
                )
        )
        result = await self.session.execute(query)
        room = result.scalars().one_or_none()
        return RoomsWithRelationships.model_validate(room, from_attributes=True) if room else {"status": "Room doesn't exists"}

