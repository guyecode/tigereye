# coding=utf-8
import time
import random
import math
from datetime import datetime
from flask import current_app
from faker import Faker
from tigereye.extensions import db
from tigereye.models import Model


class Cinema(db.Model, Model):

    cid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    address = db.Column(db.String(128), nullable=False)
    halls = db.Column(db.Integer, default=0, nullable=False)
    handle_fee = db.Column(db.Integer, default=0, nullable=False)  # 手续费
    buy_limit = db.Column(db.Integer, default=0, nullable=False)  # 单次最多能购买多少张票
    status = db.Column(db.Integer,
                       server_default='0',
                       nullable=False,
                       index=True)

    @classmethod
    def create_test_data(cls, cinema_num=10, hall_num=10, play_num=10):
        HALL_SEATS_NUM = 25
        start_time = time.time()
        from tigereye.models.hall import Hall
        from tigereye.models.movie import Movie
        from tigereye.models.play import Play
        from tigereye.models.seat import Seat, PlaySeat
        from tigereye.models.order import Order
        f = Faker('zh_CN')
        screen_types = ['普通', 'IMAX']
        audio_types = ['普通', '杜比环绕']
        cinemas = []
        for i in range(1, cinema_num + 1):
            cinema = Cinema()
            cinema.cid = i
            cinema.name = '%s影城' % f.name()
            cinema.address = f.address()
            cinema.status = 1
            cinema.put()
            cinemas.append(cinema)
        Cinema.commit()

        halls = []
        plays = []
        seats = []
        for cinema in cinemas:
            for n in range(1, hall_num + 1):
                hall = Hall()
                hall.cid = cinema.cid
                hall.name = '%s号厅' % n
                hall.screen_type = random.choice(screen_types)
                hall.audio_type = random.choice(audio_types)
                hall.seats_num = HALL_SEATS_NUM
                hall.status = 1
                hall.put()
                halls.append(hall)
            Hall.commit()

        for hall in halls:
            hall.seats = []
            for s in range(1, hall.seats_num + 1):
                seat = Seat()
                seat.cid = cinema.cid
                seat.hid = hall.hid
                seat.x = s % 5 or 5
                seat.y = math.ceil(s / 5)
                seat.row = seat.x
                seat.column = seat.y
                seat.seat_type = 1
                seat.put()
                hall.seats.append(seat)
            Seat.commit()

            for p in range(1, play_num + 1):
                play = Play()
                play.cid = cinema.cid
                play.hid = hall.hid
                play.mid = p
                play.start_time = datetime.now()
                play.duration = 3600
                play.price_type = 1
                play.price = 7000
                play.market_price = 5000
                play.lowest_price = 3000
                play.status = 1
                play.put()
                play.hall = hall
                plays.append(play)
            Play.commit()

        for play in plays:
            for seat in play.hall.seats:
                ps = PlaySeat()
                ps.pid = play.pid
                ps.copy(seat)
                ps.put()
            PlaySeat.commit()
        current_app.logger.info('create test data done! cost %.2f seconds' % (time.time() - start_time))
