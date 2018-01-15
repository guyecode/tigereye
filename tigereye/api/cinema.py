# coding=utf-8
from flask import request

from tigereye.api import ApiView
from tigereye.models.cinema import Cinema
from tigereye.models.hall import Hall
from tigereye.models.play import Play
from tigereye.models.movie import Movie
from tigereye.models.seat import Seat
from tigereye.extensions.validator import Validator
from tigereye.helper.code import Code


class CinemaView(ApiView):
    def all(self):
        return Cinema.query.all()

    @Validator(cid=int)
    def get(self):
        cid = request.params['cid']
        cinema = Cinema.get(cid)
        return cinema

    @Validator(cid=int)
    def halls(self):
        cid = request.params['cid']
        cinema = Cinema.get(cid)
        if not cinema:
            return Code.cinema_does_not_exist, {'cid': cid}
        cinema.halls = Hall.query.filter_by(cid=cid).all()
        return cinema

    @Validator(cid=int)
    def plays(self):
        cid = request.params['cid']
        cinema = Cinema.get(cid)
        if not cinema:
            return Code.cinema_does_not_exist, {'cid': cid}
        cinema.plays = Play.query.filter_by(cid=cid).all()
        if not cinema:
            return Code.cinema_does_not_exist, {'cid': cid}
        for play in cinema.plays:
            play.movies = Movie.get(play.mid)
        return cinema

    @Validator(hid=int)
    def seats(self):
        hid = request.params['hid']
        hall = Hall.query.get(hid)
        if not hall:
            return Code.hall_does_not_exist, {'hid': hid}
        hall.seats = Seat.query.filter_by(hid=hid).all()
        return hall
