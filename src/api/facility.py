from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.schemas.facility import FacilityAdd


router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("")
async def get_facilities(db:DBDep):
    return await db.facility.get_all()

@router.post("")
async def add_facilitity(db: DBDep, facility_data: FacilityAdd = Body()):
    facility = await db.facility.add(facility_data)
    await db.commit()
    return {"status": "Succesfully posted", "data": facility_data}