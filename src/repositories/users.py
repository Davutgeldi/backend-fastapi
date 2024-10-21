from sqlalchemy import select
from pydantic import EmailStr

from src.repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.schemas.users import User, UserHashedPassword


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = User

    async def get_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserHashedPassword.model_validate(model, from_attributes=True)