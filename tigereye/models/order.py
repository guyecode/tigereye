# coding=utf-8
from random import randint
from enum import Enum, unique
from sqlalchemy import text
from sqlalchemy.sql import func
from tigereye.extensions import db
from tigereye.models import Model
from tigereye.helper import wetime


@unique
class OrderStatus(Enum):
    """已锁座"""
    locked = 1
    """解锁"""
    unlocked = 2
    """自动解锁(超过一定时间未操作被系统自动解锁)"""
    auto_unlocked = 3
    """已支付"""
    paid = 4
    """已出票"""
    printed = 5
    """退款"""
    refund = 6


class Order(db.Model, Model):
    __tablename__ = 'orders'

    oid = db.Column(db.String(32), primary_key=True)
    cid = db.Column(db.Integer, nullable=False)
    pid = db.Column(db.Integer, nullable=False)
    sid = db.Column(db.Integer, nullable=False)
    """取票码"""
    ticket_flag = db.Column(db.String(64))
    """订单总金额"""
    amount = db.Column(db.Integer, default=0, nullable=False)
    """此订单的票数"""
    tickets_num = 0
    """销售方订单号"""
    seller_order_no = db.Column(db.String(32), unique=True)
    """支付时间"""
    paid_time = db.Column(db.DateTime)
    """打票时间"""
    printed_time = db.Column(db.DateTime)
    """退款时间"""
    refund_time = db.Column(db.DateTime)
    created_time = db.Column(db.DateTime,
                             server_default=text('CURRENT_TIMESTAMP'))
    updated_time = db.Column(db.DateTime, onupdate=func.now())
    status = db.Column(db.Integer, server_default='0', nullable=False)

    @classmethod
    def create(cls, cid, pid, sid):
        order = cls()
        order.oid = '%s%s%s' % (wetime.now(), randint(100000, 999999), pid)
        order.cid = cid
        order.pid = pid
        if type(sid) == list:
            order.sid = ','.join(str(i) for i in sid)
        else:
            order.sid = sid
        return order

    def gen_ticket_flag(self):
        s = []
        for i in range(8):
            s.append(str(randint(1000, 9999)))
        self.ticket_flag = ''.join(s)

    def validate(self, ticket_flag):
        return self.ticket_flag == ticket_flag

    @classmethod
    def getby_orderno(cls, orderno):
        return Order.query.filter_by(seller_order_no=orderno).first()

    @classmethod
    def getby_ticket_flag(cls, ticket_flag):
        return cls.query.filter_by(ticket_flag=ticket_flag).first()
