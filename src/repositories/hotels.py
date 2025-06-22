from datetime import date

from sqlalchemy import select, func

from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel
from src.models.rooms import RoomsOrm
from src.repositories.utils import rooms_id_for_booking
from src.repositories.mappers.mappers import HotelDataMapper


class HotelRepository(BaseRepository):
    model = HotelsOrm
    mapper = HotelDataMapper

    async def get_filtered_by_time(
        self,
        date_from: date,
        date_to: date,
        city: str,
        name: str,
        limit: int,
        offset: int,
    ) -> list[Hotel]:
        rooms_id_to_get = rooms_id_for_booking(date_from=date_from, date_to=date_to)
        hotels_id_to_get = (
            select(RoomsOrm.hotel_id).select_from(RoomsOrm).filter(RoomsOrm.id.in_(rooms_id_to_get))
        )

        query = select(HotelsOrm).filter(HotelsOrm.id.in_(hotels_id_to_get))
        if city:
            query = query.filter(func.lower(HotelsOrm.city).contains(city.lower()))
        if name:
            query = query.filter(func.lower(HotelsOrm.name).contains(name.lower()))
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)

        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]
