from fastapi import APIRouter, Body, HTTPException

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest


router = APIRouter(prefix="/hotels", tags=["Rooms"])


@router.get("/rooms/all")
async def get_rooms(db: DBDep):
    return await db.rooms.get_all()


@router.get("/{hotel_id}/rooms")
async def get_rooms_by_id(hotel_id: int, db: DBDep):
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if not hotel:
        raise HTTPException(status_code=401, detail="Hotel doesn't exists")
    return await db.rooms.get_filtered(hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms")
async def add_hotel_room(hotel_id: int, db: DBDep, room_data: RoomAddRequest = Body(openapi_examples={
    "1": {
        "summary": "Example 1", "value": {
            "name": "VIP", 
            "description":"VIP room for special guess",
            "price": 30,
            "quantity": 5
        }},
    "2":{
        "summary": "Example 2", "value":{
            "name": "VIP", 
            "description":"VIP room for celebrities",
            "price": 120,
            "quantity": 2
        }
    }
})
    ):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel doesn't exists")
    room = await db.rooms.add(_room_data)
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