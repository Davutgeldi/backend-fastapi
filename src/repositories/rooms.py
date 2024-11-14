from sqlalchemy import select

from repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room


class RoomRepository(BaseRepository):
    model = RoomsOrm
    schema = Room


    async def get_by_id(self, hotel_id: int):
        query = select(self.model).filter_by(hotel_id=hotel_id)
        result = await self.session.execute(query)
        obj = result.scalars().all()
        return [self.schema.model_validate(model, from_attributes=True) for model in obj]
