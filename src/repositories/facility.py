from sqlalchemy import select, delete, insert

from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesOrm
from src.models.facilities import RoomsFacilitiesOrm
from src.schemas.facility import RoomsFacility
from src.repositories.mappers.mappers import FacilityDataMapper


class FacilityRepository(BaseRepository):
    model = FacilitiesOrm
    mapper = FacilityDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomsFacility

    async def set_room_facilities(self, room_id: int, facilities_ids: list[int]) -> None:
        get_current_facilities_ids = select(self.model.facility_id).filter_by(room_id=room_id)
        res = await self.session.execute(get_current_facilities_ids)
        current_facilities_ids: list[int] = res.scalars().all()
        ids_to_delete = list(set(current_facilities_ids) - set(facilities_ids))
        ids_to_insert = list(set(facilities_ids) - set(current_facilities_ids))

        if ids_to_delete:
            delete_m2m_facilities = delete(self.model).filter(
                self.model.room_id == room_id, self.model.facility_id.in_(ids_to_delete)
            )
            await self.session.execute(delete_m2m_facilities)

        if ids_to_insert:
            insert_m2m_facilities = insert(self.model).values(
                [{"room_id": room_id, "facility_id": f_id} for f_id in ids_to_insert]
            )
            await self.session.execute(insert_m2m_facilities)
