# coding=utf-8

from enum import Enum, unique
from sqlalchemy import text
from sqlalchemy.sql import func
from tigereye.extensions import db
from tigereye.models import Model


@unique
class PlayStatus(Enum):
    """正常"""
    ok = 0
    """维修中"""
    repair = 99


class Play(db.Model, Model):

    pid = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer, nullable=False)
    hid = db.Column(db.Integer, nullable=False)
    mid = db.Column(db.Integer, nullable=False)

    start_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, default=0, nullable=False)  # 影片时长

    # 价格类型（1-正价 2-优惠场次）price_type=2说明marketPrice是优惠后的价格
    price_type = db.Column(db.Integer)
    price = db.Column(db.Integer)  # 原价(名义价格，主要用于显示，可不用)
    market_price = db.Column(db.Integer)  # 影院柜台售卖价
    lowest_price = db.Column(db.Integer, default=0)  # 限制能卖的最低价格

    created_time = db.Column(db.DateTime,
                             server_default=text('CURRENT_TIMESTAMP'))
    updated_time = db.Column(db.DateTime, onupdate=func.now())
    status = db.Column(db.Integer,
                       server_default='0',
                       nullable=False,
                       index=True)
