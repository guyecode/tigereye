# coding=utf-8
from flask import current_app
from tigereye.extensions import db
from tigereye.models import Model


class Movie(db.Model, Model):

    mid = db.Column(db.Integer, primary_key=True)
    sn = db.Column(
        db.String(32), unique=True, nullable=False)  # 广电总局规定的影片全国唯一编码
    name = db.Column(db.String(64), nullable=False)
    language = db.Column(db.String(32))
    subtitle = db.Column(db.String(32))
    show_date = db.Column(db.Date)  # 上映时间
    mode = db.Column(db.String(16))  # 电影格式，如：胶片，数字
    vision = db.Column(db.String(16))  # 放映类型：3D 2D
    screen_size = db.Column(db.String(16))  # 屏幕尺寸
    introduction = db.Column(db.Text)
    status = db.Column(db.Integer,
                       server_default='0',
                       nullable=False,
                       index=True)

    @classmethod
    def create_test_data(cls, num=10):
        for i in range(1, num + 1):
            m = Movie()
            m.mid = i
            m.sn = str(i).zfill(10)
            m.name = '电影名称%s' % i
            m.language = '英文'
            m.subtitle = '中文'
            # m.show_date =
            m.mode = '数字'
            m.vision = '2D'
            m.screen_size = 'IMAX'
            m.introduction = 'blahblah哈哈'
            m.status = 1
            db.session.add(m)
        db.session.commit()
        current_app.logger.info('movie test data done!')
