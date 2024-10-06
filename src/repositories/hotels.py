from sqlalchemy import select, func

from repositories.base import BaseRepository
from src.models.hotels import HotelsOrm


class HotelRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
            self, 
            city,
            name, 
            limit, 
            offset
        ):
        query = select(HotelsOrm)
        if city:
            query = query.filter(func.lower(HotelsOrm.city).contains(city.lower()))
        if name:
            query = query.filter(func.lower(HotelsOrm.name).contains(name.lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)

        return result.scalars().all()
    