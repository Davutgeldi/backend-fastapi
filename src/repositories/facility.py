from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesOrm
from src.schemas.facility import Facility


class FacilityRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility