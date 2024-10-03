from fastapi import Query, Body, APIRouter

from sqlalchemy import insert, select, func

from schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from src.database import async_session
from src.models.hotels import HotelsOrm
from src.database import engine
from src.repositories.hotels import HotelRepository 

router = APIRouter(prefix='/hotels', tags=['Hotels'])


@router.get('', summary='Get query', 
            description='<h2>use it if u wanna take list of hotels</h2>'
            )
async def read_root(
    pagination: PaginationDep,
    id: str | None = Query(None, description='Hotels id'),
    city: str | None = Query(None, description='Hotels city'),
    name: str | None = Query(None, description='Hotels name')
    ):
    async with async_session() as session:
        return await HotelRepository(session).get_all(HotelsOrm)
    # per_page = pagination.per_page or 3
    # async with async_session() as session:
    #     query = select(HotelsOrm)
    #     if city:
    #         query = query.filter(func.lower(HotelsOrm.city).contains(city.lower()))
    #     if name: 
    #         query = query.filter(func.lower(HotelsOrm.name).contains(name.lower()))
    #     query = (
    #         query
    #         .limit(per_page)
    #         .offset(offset = (pagination.page - 1) * per_page)
    #     )
    #     print(query.compile(compile_kwargs={'literal_binds': True}))
    #     result = await session.execute(query)
    #     hotels = result.scalars().all()
    #     return hotels
    # if pagination.page and pagination.per_page:    
    #     return hotels[(pagination.page - 1) * pagination.per_page:][:pagination.per_page]
    


@router.delete('/{hotel_id}')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}


@router.post('')
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    '1': {'summary': 'Russia', 'value': {'city': 'Sochi', 'name': 'Balkan'}},
    '2': {'summary': 'USA', 'value': {'city': 'Florida', 'name': 'Miami Beach'}}
})):
    async with async_session() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        # Debug, sql statement
        #print(add_hotel_stmt.compile(compile_kwargs={engine, 'literal_binds': True}))
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {'status': 'Successfully posted'}


@router.put('/{hotel_id}')
def put_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['city'] = hotel_data.city
            hotel['name'] = hotel_data.name
    return {'status': 'Succesfully modified'}


@router.patch('/{hotel_id}') 
# Can add attribute summary and description, 
# change name of endpoint and give description 
def patch_hotel(hotel_id: int, hotel_data: HotelPATCH):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['city'] = hotel_data.city if hotel_data.city != None else hotel['city']
            hotel['name'] = hotel_data.name if hotel_data.name != None else hotel['name']
    return {'status': 'Successfully modified'}
            