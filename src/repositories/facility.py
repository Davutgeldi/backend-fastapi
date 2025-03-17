from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesOrm
from src.schemas.facility import Facility
from src.models.facilities import RoomsFacilitiesOrm
from src.schemas.facility import RoomsFacility


class FacilityRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomsFacility