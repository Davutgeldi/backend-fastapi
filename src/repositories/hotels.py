from sqlalchemy import select, func

from repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel


class HotelRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_all(
            self, 
            city,
            name, 
            limit, 
            offset
        ) -> list[Hotel]:
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
        print(query.compile(compile_kwargs={'literal_binds': True}))
        result = await self.session.execute(query)

        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
    