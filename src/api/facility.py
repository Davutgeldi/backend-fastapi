from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facility import FacilityAdd
from src.tasks.tasks import test_task


router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("")
@cache(expire=10)
async def get_facilities(db:DBDep):
    return await db.facility.get_all()
    
    
@router.post("")
async def add_facilitity(db: DBDep, facility_data: FacilityAdd = Body()):
    facility = await db.facility.add(facility_data)
    await db.commit()

    test_task.delay()

    return {"status": "Succesfully posted", "data": facility_data}