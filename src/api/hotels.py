from fastapi import Query, Body, APIRouter

from schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from src.database import async_session
from src.database import engine
from src.repositories.hotels import HotelRepository 

router = APIRouter(prefix='/hotels', tags=['Hotels'])


@router.get('', summary='Get query', 
            description='<h2>Use it if u wanna take list of hotels</h2>'
            )
async def read_root(
    pagination: PaginationDep,
    id: str | None = Query(None, description='Hotels id'),
    city: str | None = Query(None, description='Hotels city'),
    name: str | None = Query(None, description='Hotels name')
    ):
    per_page = pagination.per_page or 5
    async with async_session() as session:
        return await HotelRepository(session).get_all( 
            city=city, 
            name=name, 
            limit=per_page, 
            offset=(pagination.page - 1) * per_page)


@router.get('/{hotel_id}')
async def get_hotel_id(hotel_id: int):
    async with async_session() as session:
        return await HotelRepository(session).get_id(hotel_id)


@router.post('')
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    '1': {'summary': 'Russia', 'value': {'city': 'Sochi', 'name': 'Balkan'}},
    '2': {'summary': 'USA', 'value': {'city': 'Florida', 'name': 'Miami Beach'}}
})):
    async with async_session() as session:
        hotel = await HotelRepository(session).add(hotel_data)
        await session.commit()
    return {'status': 'Successfully posted', 'data': hotel}


@router.put('/{hotel_id}')
async def put_hotel(hotel_id: int, hotel_data: Hotel):
    async with async_session() as session:
        await HotelRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {'status': 'Succesfully modified'}


@router.patch('/{hotel_id}') 
# Can add attribute summary and description, 
# change name of endpoint and give description 
async def patch_hotel(hotel_id: int, hotel_data: HotelPATCH):
    async with async_session() as session:
        await HotelRepository(session).edit(hotel_data, is_patch=True, id=hotel_id)
        await session.commit()
    return {'status': 'Successfully modified'}
            

@router.delete('/{hotel_id}')
async def delete_hotel(hotel_id: int):
    async with async_session() as session:
        await HotelRepository(session).delete(id=hotel_id)
        await session.commit()
    return {'status': 'OK'}