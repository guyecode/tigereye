# coding=utf-8
from datetime import datetime
from enum import Enum, unique
from sqlalchemy import text
from sqlalchemy.schema import Index
from tigereye.extensions import db
from tigereye.models import Model


@unique
class SeatStatus(Enum):
    """正常状态，可购买"""
    ok = 0
    """已锁定"""
    locked = 1
    """已售出"""
    sold = 2
    """已打票"""
    printed = 3
    """已预订"""
    booked = 9
    """维修中"""
    repair = 99


@unique
class SeatType(Enum):
    """过道"""
    road = 0
    """单人"""
    single = 1
    """双人"""
    couple = 2
    """保留座位"""
    reserve = 3
    """残疾专座"""
    for_disable = 4
    """VIP专座"""
    vip = 5
    """震动座椅"""
    shake = 6


class Seat(db.Model, Model):
    """影厅座位信息

    每一条记录对应一个座位
    """
    sid = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer, nullable=False)
    hid = db.Column(db.Integer, nullable=False)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    row = db.Column(db.String(8))
    column = db.Column(db.String(8))
    area = db.Column(db.String(16))
    love_seats = db.Column(db.String(32))
    seat_type = db.Column(db.String(16))
    status = db.Column(db.Integer, nullable=False, server_default='0')

    @classmethod
    def getby_hid(cls, hid):
        return cls.query.filter_by(hid=hid).all()


class PlaySeat(db.Model, Model):
    """排期座位"""
    psid = db.Column(db.Integer, primary_key=True)
    orderno = db.Column(db.String(32), index=True)
    sid = db.Column(db.Integer, nullable=False)
    pid = db.Column(db.Integer, nullable=False)
    cid = db.Column(db.Integer, nullable=False)
    hid = db.Column(db.Integer, nullable=False)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    row = db.Column(db.String(8))
    column = db.Column(db.String(8))
    area = db.Column(db.String(8))
    love_seats = db.Column(db.String(32))
    seat_type = db.Column(db.String(16))
    status = db.Column(db.Integer,
                       nullable=False,
                       server_default='0',
                       index=True)
    locked_time = db.Column(db.DateTime)
    created_time = db.Column(db.DateTime,
                             server_default=text('CURRENT_TIMESTAMP'))

    __table_args__ = (Index('ps_index', "pid", "sid"), )

    @classmethod
    def getby(cls, pid, sid):
        return cls.get('%s-%s' % (pid, sid))

    def copy(self, seat):
        """
            将一个Seat对象中的信息拷贝到PlaySeat对象中
            @params
                seat: Seat对象
        """
        self.sid = seat.sid
        self.cid = seat.cid
        self.hid = seat.hid
        self.x = seat.x
        self.y = seat.y
        self.row = seat.row
        self.column = seat.column
        self.area = seat.area
        self.love_seats = seat.love_seats
        self.seat_type = seat.seat_type
        self.status = seat.status

    @classmethod
    def getby_orderno(cls, orderno):
        return cls.query.filter_by(orderno=orderno).all()

    @classmethod
    def lock(cls, orderno, pid, sid_list):
        session = db.create_scoped_session()
        rows = session.query(PlaySeat).filter(
            PlaySeat.pid == pid, PlaySeat.status == SeatStatus.ok.value,
            PlaySeat.sid.in_(sid_list)).update({'orderno': orderno,
                                                'status':
                                                SeatStatus.locked.value,
                                                'locked_time': datetime.now()},
                                               synchronize_session=False)
        if rows != len(sid_list):
            session.rollback()
            return 0
        session.commit()
        return rows

    @classmethod
    def unlock(cls, orderno, pid, sid_list):
        session = db.create_scoped_session()
        rows = session.query(PlaySeat).filter_by(
            orderno=orderno, status=SeatStatus.locked.value).update(
                {
                    'orderno': None,
                    'status': SeatStatus.ok.value
                },
                synchronize_session=False)
        if rows != len(sid_list):
            session.rollback()
            return 0
        session.commit()
        return rows

    @classmethod
    def buy(cls, orderno, pid, sid_list):
        session = db.create_scoped_session()
        rows = session.query(PlaySeat).filter_by(
            orderno=orderno, status=SeatStatus.locked.value).update(
                {'status': SeatStatus.sold.value},
                synchronize_session=False)
        if rows != len(sid_list):
            session.rollback()
            return 0
        session.commit()
        return rows

    @classmethod
    def print_tickets(cls, orderno, pid, sid_list):
        session = db.create_scoped_session()
        rows = session.query(PlaySeat).filter_by(
            orderno=orderno, status=SeatStatus.sold.value).update(
                {'status': SeatStatus.printed.value},
                synchronize_session=False)
        if rows != len(sid_list):
            session.rollback()
            return 0
        session.commit()
        return rows

    @classmethod
    def refund(cls, orderno, pid, sid_list):
        session = db.create_scoped_session()
        rows = session.query(PlaySeat).filter_by(
            orderno=orderno, status=SeatStatus.sold.value).update(
                {'status': SeatStatus.ok.value,
                 'orderno': None},
                synchronize_session=False)
        if rows != len(sid_list):
            session.rollback()
            return 0
        session.commit()
        return rows
