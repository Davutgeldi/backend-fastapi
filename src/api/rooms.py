from fastapi import APIRouter, Body, HTTPException

from src.database import async_session
from src.repositories.rooms import RoomRepository
from src.repositories.hotels import HotelRepository
from src.schemas.rooms import RoomAdd, RoomPatch, Room


router = APIRouter(prefix="/hotels", tags=["Rooms"])


@router.get("/all/rooms")
async def get_rooms():
    async with async_session() as session:
        return await RoomRepository(session).get_all()


@router.get("/{hotel_id}/rooms")
async def get_rooms_by_id(hotel_id: int):
    async with async_session() as session:
        hotel = await HotelRepository(session).get_one_or_none(id=hotel_id)
        if not hotel:
            raise HTTPException(status_code=401, detail="Hotel doesn't exists")
        return await RoomRepository(session).get_by_id(hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms")
async def add_hotel_room(hotel_id: int, room_data: RoomAdd = Body(openapi_examples={
    "1": {
        "summary": "Example 1", "value": {
            "hotel_id": "1",
            "name": "VIP", 
            "description":"VIP room for special guess",
            "price": 30,
            "quantity": 5
        }},
    "2":{
        "summary": "Example 2", "value":{
            "hotel_id": "1",
            "name": "VIP", 
            "description":"VIP room for celebrities",
            "price": 120,
            "quantity": 2
        }
    }
})
    ):
    room_data.hotel_id = hotel_id
    async with async_session() as session:
        hotel = await HotelRepository(session).get_one_or_none(id=hotel_id)
        if not hotel:
            raise HTTPException(status_code=404, detail="Hotel doesn't exists")
        room = await RoomRepository(session).add(room_data)
        await session.commit()
    return {"status": "Succesfully posted", "data": room}


@router.put("/{hotel_id}/room/{room_id}")
async def update_room(hotel_id: int, room_id: int, room_data: Room):
    async with async_session() as session:
        hotel = await HotelRepository(session).get_one_or_none(id=hotel_id)
        if not hotel:
            raise HTTPException(status_code=404, detail="Hotel doesn't exists")
        await RoomRepository(session).edit(room_data, id=room_id)
        await session.commit()
    return {"status": "Succesfully modified"}


@router.patch("/{hotel_id}/room/{room_id}")
async def edit_room(hotel_id: int, room_id: int, room_data: RoomPatch):
    async with async_session() as session:
        hotel = await HotelRepository(session).get_one_or_none(id=hotel_id)
        if not hotel:
            raise HTTPException(status_code=404, detail="Hotel doesn't exists")
        await RoomRepository(session).edit(room_data, id=room_id, is_patch=True, hotel_id=hotel_id)
        await session.commit()
    return {"status": "Succesfully modified"}


@router.delete("/{hotel_id}/room")
async def delete_room(hotel_id: int):
    async with async_session() as session:
        hotel = await HotelRepository(session).get_one_or_none(id=hotel_id)
        if not hotel:
            raise HTTPException(status_code=404, detail="Hotel doesn't exists")
        await RoomRepository(session).delete(hotel_id=hotel_id)
        await session.commit()
    return {"status": "Succesfully deleted"}