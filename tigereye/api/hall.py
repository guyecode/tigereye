# coding=utf-8
from flask import request

from tigereye.api import ApiView
from tigereye.models.hall import Hall
from tigereye.models.seat import Seat, SeatType
from tigereye.extensions.validator import Validator
from tigereye.helper.code import Code


class HallView(ApiView):
    """座位相关操作API"""

    @Validator(hid=int)
    def seats(self):
        hid = request.params['hid']
        hall = Hall.get(hid)
        if not hall:
            return Code.hall_does_not_exist, {'hid': hid}
        hall.seats = Seat.query.filter(
            Seat.hid == hid, Seat.seat_type != SeatType.road.value).all()
        return hall
