from datetime import date

from fastapi import APIRouter, Body, HTTPException, Query

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest
from src.schemas.facility import RoomsFacilitiesAdd


router = APIRouter(prefix="/hotels", tags=["Rooms"])


@router.get("/rooms/all")
async def get_rooms(db: DBDep):
    return await db.rooms.get_all()


@router.get("/{hotel_id}/rooms")
async def get_rooms_by_id(
    db: DBDep, 
    hotel_id: int, 
    date_from: date = Query(example="2024-07-05"), 
    date_to: date = Query(example="2024-07-01"),
):
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if not hotel:
        raise HTTPException(status_code=401, detail="Hotel doesn't exists")
    return await db.rooms.get_filterd_by_time(date_from=date_from, date_to=date_to, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms")
async def add_hotel_room(hotel_id: int, db: DBDep, room_data: RoomAddRequest = Body()
    ):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel doesn't exists")
    room = await db.rooms.add(_room_data)
    
    rooms_facilities_data = [RoomsFacilitiesAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_id]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()

    return {"status": "Succesfully posted", "data": room}


@router.put("/{hotel_id}/room/{room_id}")
async def update_room(hotel_id: int, room_id: int, room_data: RoomAddRequest, db: DBDep):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel doesn't exists")
    await db.rooms.edit(_room_data, id=room_id)
    await db.commit()
    return {"status": "Succesfully modified"}


@router.patch("/{hotel_id}/room/{room_id}")
async def edit_room(hotel_id: int, room_id: int, room_data: RoomPatchRequest, db: DBDep):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel doesn't exists")
    await db.rooms.edit(_room_data, is_patch=True, hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "Succesfully modified"}


@router.delete("/{hotel_id}/room/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel doesn't exists")
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "Succesfully deleted"}