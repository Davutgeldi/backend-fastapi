from fastapi import Query, Body, APIRouter

from schemas.hotels import HotelAdd, HotelPatch
from src.api.dependencies import PaginationDep, DBDep


router = APIRouter(prefix='/hotels', tags=['Hotels'])


@router.get("", summary="Get query", 
            description="<h2>Use it if u wanna take list of hotels</h2>"
            )
async def read_root(
    pagination: PaginationDep,
    db: DBDep,
    city: str | None = Query(None, description='Hotels city'),
    name: str | None = Query(None, description='Hotels name')
    ):
    per_page = pagination.per_page or 5
    return await db.hotels.get_all( 
        city=city, 
        name=name, 
        limit=per_page, 
        offset=(pagination.page - 1) * per_page)


@router.get("/{hotel_id}")
async def get_hotel_id(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("")
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(openapi_examples={
    '1': {'summary': 'Hotel from Russia', 'value': {'city': 'Sochi', 'name': 'Balkan'}},
    '2': {'summary': 'Hotel from USA', 'value': {'city': 'Florida', 'name': 'Miami Beach'}}
})):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "Successfully posted", "data": hotel}


@router.put("/{hotel_id}")
async def update_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "Succesfully modified"}


@router.patch('/{hotel_id}') 
# Can add attribute summary and description, 
# change name of endpoint and give description 
async def edit_hotel(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    await db.hotels.edit(hotel_data, is_patch=True, id=hotel_id)
    await db.commit()
    return {'status': 'Successfully modified'}
            

@router.delete('/{hotel_id}')
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "Succesfully deleted"}