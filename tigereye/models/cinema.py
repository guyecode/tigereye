# coding=utf-8

from flask import current_app
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
    def create_test_data(cls, cinema_num=2, hall_num=2, play_num=2):
        from datetime import datetime
        from tigereye.models.hall import Hall
        from tigereye.models.play import Play
        from tigereye.models.seat import Seat, PlaySeat, SeatType
        from random import choice
        screen_types = ['普通', 'IMAX']
        audio_types = ['普通', '杜比环绕']
        for i in range(1, cinema_num + 1):
            cinema = Cinema()
            cinema.cid = i
            cinema.name = 'cinema%s' % i
            cinema.address = '北京市朝阳区XX街%s号' % i
            cinema.halls = hall_num
            cinema.status = 1
            cinema.save()
            for n in range(1, hall_num + 1):
                hall = Hall()
                hall.cid = cinema.cid
                hall.name = '%s号厅' % n
                hall.screen_type = choice(screen_types)
                hall.audio_type = choice(audio_types)
                hall.seats_num = 25
                hall.seats = ','.join([str(s) for s in range(hall.seats_num)])
                hall.status = 1
                hall.save()
                for s in range(1, hall.seats_num + 1):
                    seat = Seat()
                    seat.cid = cinema.cid
                    seat.hid = hall.hid
                    seat.x = s % 5 or 5
                    seat.y = s / 5 + 1
                    seat.row = seat.y
                    seat.column = seat.x
                    seat.seat_type = SeatType.single.value
                    seat.put()
                Seat.commit()
                for p in range(1, play_num + 1):
                    play = Play()
                    # play.pid = hall.hid * play_num + p
                    play.cid = cinema.cid
                    play.hid = hall.hid
                    play.mid = p
                    play.start_time = datetime.now()
                    play.end_time = datetime.now()
                    play.price_type = 1
                    play.price = 7000
                    play.market_price = 5000
                    play.lowest_price = 3000
                    play.seat_available_num = hall.seats_num
                    play.allow_book = 1
                    play.last_updated = datetime.now()
                    play.status = 1
                    play.save()
                    seats = Seat.getby_hid(play.hid)
                    for seat in seats:
                        ps = PlaySeat()
                        ps.pid = play.pid
                        ps.copy(seat)
                        ps.put()
                    PlaySeat.commit()
        current_app.logger.info('cinema test data done!')
