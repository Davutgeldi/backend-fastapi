from src.repositories.mappers.base import DataMapper
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room, RoomsWithRels
from src.models.users import UsersOrm
from src.schemas.users import User
from src.models.bookings import BookingsOrm
from src.schemas.bookings import Bookings
from src.models.facilities import FacilitiesOrm
from src.schemas.facility import Facility


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel


class RoomDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Room


class RoomDataWithRelsMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomsWithRels


class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User


class BookingsDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = Bookings


class FacilityDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = Facility
