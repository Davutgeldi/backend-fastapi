from datetime import date

from sqlalchemy import select, func

from src.models.rooms import RoomsOrm
from src.models.bookings import BookingsOrm


def rooms_id_for_booking(
    date_from: date,
    date_to: date,
    hotel_id: int | None = None,
):
    rooms_count = (
        select(BookingsOrm.room_id, func.count("*").label("rooms_booked"))
        .select_from(BookingsOrm)
        .filter(
            BookingsOrm.date_from <= date_to,
            BookingsOrm.date_to >= date_from,
        )
        .group_by(BookingsOrm.room_id)
        .cte(name="rooms_count")
    )

    free_rooms_table = (
        select(
            RoomsOrm.id.label("room_id"),
            (RoomsOrm.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_free"),
        )
        .select_from(RoomsOrm)
        .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
        .cte(name="free_rooms_table")
    )

    rooms_id_for_hotel = select(RoomsOrm.id).select_from(RoomsOrm)
    if hotel_id is not None:
        rooms_id_for_hotel = rooms_id_for_hotel.filter_by(hotel_id=hotel_id)

    rooms_id_for_hotel = rooms_id_for_hotel.subquery(name="rooms_id_for_hotel")

    get_rooms_id = (
        select(free_rooms_table.c.room_id)
        .select_from(free_rooms_table)
        .filter(
            free_rooms_table.c.rooms_free > 0,
            free_rooms_table.c.room_id.in_(rooms_id_for_hotel),
        )
    )

    return get_rooms_id
