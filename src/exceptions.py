from datetime import date

from fastapi import HTTPException


class BaseExceptions(Exception):
    detail = "Not found error"

    def __init__(self, detail, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(BaseException):
    detail = "Object not found"


class AllRoomsAreBookedException(BaseException):
    detail = "Rooms like that are already booked"


class ObjectAlreadyExistsException(BaseException):
    detail = "Object already exists"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(status_code=422, detail="Invalid date, change date to please")


class BookingException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class HotelNotFoundHttpException(BookingException):
    status_code = 404
    detail = "Hotel not found"


class RoomNotFoundHttpException(BookingException):
    status_code = 404
    detail = "Room not found"