from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingsAddRequest, BookingsAdd


router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("")
async def get_all_bookings(db: DBDep):
   return await db.bookings.get_all()


@router.get("/me")
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
   return await db.bookings.get_filtered(user_id=user_id)


@router.post("")
async def get_bookings(
    db: DBDep, 
    bookings_data: BookingsAddRequest, 
    user_id: UserIdDep
    ):
   room = await db.rooms.get_one_or_none(id=bookings_data.room_id)
   if not room:
      raise HTTPException(status_code=404, detail="Room not found")
   room_price = room.price
   _booking_data = BookingsAdd(
      user_id=user_id,
      price=room_price,
      **bookings_data.model_dump()
   )
   booking = await db.bookings.add(_booking_data)
   await db.commit()
   return {"status": "Succesfully posted", "data": booking}

