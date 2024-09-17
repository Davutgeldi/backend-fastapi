from fastapi import Query, Body, APIRouter


router = APIRouter(prefix='/hotels', tags=['Hotels'])


hotels = [
    {'id': 1, 'city': 'Ashgabat', 'name': 'Garagum'},
    {'id': 2, 'city':'Dashoguz', 'name': 'Mizan'}
]


@router.get('')
def read_root(
    id: str | None = Query(None, description='Hotels id'),
    title: str | None = Query(None, description='Hotels name')
    ):
    get_hotel = []
    for hotel in hotels:
        if id and hotel[id] != id:
            continue
        if title and hotel[title] != title:
            continue
        get_hotel.append(hotel)
    return get_hotel


@router.delete('/{hotel_id}')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}


@router.post('')
def create_hotel(title: str = Body(embed=True)):
    global hotels
    hotels.append(
        {
            'id': hotels[-1]['id'] + 1,
            'title': title
        }
    )
    return {'status': 'Successfully posted'}


@router.put('/{hotel_id}')
def put_hotel(
    hotel_id: int,
    city: str = Body(description='Hotels city'), 
    name: str = Body(description='Hotels name')
    ):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['city'] = city
            hotel['name'] = name
    return {'status': 'Succesfully modified'}


@router.patch('/{hotel_id}') 
# Can add attribute summary and description, 
# change name of endpoint and give description 
def patch_hotel(
    hotel_id: int,
    city: str | None = Body(None, description='Hotels City'),
    name: str | None = Body(None, description='Hotels Name')
    ):
    global hotels
    for hotel in hotels:
        if hotel['id'] == hotel_id:
            hotel['city'] = city if city != None else hotel['city']
            hotel['name'] = name if name != None else hotel['name']
    return {'status': 'Successfully modified'}
            