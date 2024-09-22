from fastapi import Query, Body, APIRouter

from schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep

router = APIRouter(prefix='/hotels', tags=['Hotels'])


hotels = [
    {'id': 1, 'city': 'Ashgabat', 'name': 'Garagum'},
    {'id': 2, 'city':'Dashoguz', 'name': 'Mizan'},
    {'id': 3, 'city':'Lebap', 'name': 'Yelken'},
    {'id': 4, 'city':'Anev', 'name': 'Watancy'},
    {'id': 5, 'city':'Mary', 'name': 'Gami'},
    {'id': 6, 'city':'Balkan', 'name': 'Hazar'},
    {'id': 7, 'city':'Cheleken', 'name': 'Archabil'},
]


@router.get('', summary='Get query', 
            description='<h2>use it if u wanna take list of hotels</h2>'
            )
def read_root(
    pagination: PaginationDep,
    id: str | None = Query(None, description='Hotels id'),
    title: str | None = Query(None, description='Hotels name'),
    ):
    if pagination.page and pagination.per_page:    
        return hotels[(pagination.page - 1) * pagination.per_page:][:pagination.per_page]
    return hotels


@router.delete('/{hotel_id}')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}


@router.post('')
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    '1': {'summary': 'Russia', 'value': {'city': 'Sochi', 'name': 'Balkan'}},
    '2': {'summary': 'USA', 'value': {'city': 'Florida', 'name': 'Miami Beach'}}
})):
    global hotels
    hotels.append(
        {
            'id': hotels[-1]['id'] + 1,
            'title': hotel_data.city,
            'name': hotel_data.name
        }
    )
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
            