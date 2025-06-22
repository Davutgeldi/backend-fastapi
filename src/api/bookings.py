from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingsAddRequest, BookingsAdd
from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("")
async def get_all_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("")
async def add_bookings(db: DBDep, bookings_data: BookingsAddRequest, user_id: UserIdDep):
    try:
        room = await db.rooms.get_one(id=bookings_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Room not found")

    room_price = room.price
    hotel = await db.hotels.get_one(id=room.hotel_id)
    _booking_data = BookingsAdd(user_id=user_id, price=room_price, **bookings_data.model_dump())
    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    except AllRoomsAreBookedException as ex:
        raise HTTPException(status_code=409, detail=AllRoomsAreBookedException.detail)
    await db.commit()
    return {"status": "Succesfully posted", "data": booking}
