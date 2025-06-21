from src.database import async_session_maker_null_pool
from src.schemas.hotels import HotelAdd
from src.utils.db_manager import DBManager
from src.config import settings


async def test_hotel_add():
    first_hotel = HotelAdd(city="New York", name="Test Hotel")
    second_hotel = HotelAdd(city="Tejen", name="Selim")
    
    assert settings.DB_NAME == "test"
    assert settings.MODE == "TEST"


    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        new_hotel = await db.hotels.add(first_hotel)
        hotel = await db.hotels.add(second_hotel)
        await db.commit()
        print(f"{new_hotel=}")
