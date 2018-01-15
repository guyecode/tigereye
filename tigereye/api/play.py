# coding=utf-8
from flask import request

from tigereye.api import ApiView
from tigereye.models.seat import PlaySeat, SeatType
from tigereye.extensions.validator import Validator


class PlayView(ApiView):
    """排期相关操作API"""

    @Validator(pid=int)
    def seats(self):
        return PlaySeat.query.filter(
            PlaySeat.pid == request.params['pid'],
            PlaySeat.seat_type != SeatType.road.value).all()
