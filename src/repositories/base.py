from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel

class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session
    
    async def get_all(self, model, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_id(self, hotel_id: int):
        query = select(self.model).filter_by(id=hotel_id)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()
        
    async def add(self, data: BaseModel):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model) 
        result = await self.session.execute(add_data_stmt)
        return result.scalars().one()
    
    async def edit(self, data: BaseModel, is_patch: bool = False, **filter_by) -> None:
        edit_stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump(exclude_unset=is_patch))
        await self.session.execute(edit_stmt)

    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)
