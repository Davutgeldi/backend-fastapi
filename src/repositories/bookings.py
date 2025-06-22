from datetime import date

from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.schemas.bookings import BookingsAdd
from src.repositories.utils import rooms_id_for_booking
from src.repositories.mappers.mappers import BookingsDataMapper
from src.exceptions import AllRoomsAreBookedException


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingsDataMapper

    async def get_bookings_with_today_checkin(self):
        query = select(BookingsOrm).filter(BookingsOrm.date_from == date.today())
        res = await self.session.execute(query)

        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add_booking(self, data: BookingsAdd, hotel_id: int):
        rooms_id_to_get = rooms_id_for_booking(
            date_from=data.date_from,
            date_to=data.date_to,
            hotel_id=hotel_id,
        )
        rooms_id_to_book_res = await self.session.execute(rooms_id_to_get)
        rooms_id_to_book = rooms_id_to_book_res.scalars().all()

        if data.room_id in rooms_id_to_book:
            new_booking = await self.add(data)
            return new_booking

        raise AllRoomsAreBookedException


