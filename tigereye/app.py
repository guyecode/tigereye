# coding=utf-8
import os
import logging
from logging import FileHandler, Formatter
from logging.handlers import SMTPHandler
from flask import Flask
from flask_redis import FlaskRedis

from tigereye import extensions
from tigereye.extensions import db, MockRedisWrapper
from tigereye.models import JSONEncoder
from tigereye.api import ApiView


def create_app(config=None):
    app = Flask('tigereye')
    app.config.from_object('tigereye.configs.default.DefaultConfig')
    app.config.from_object(config)
    # try to update the config via the environment variable
    app.config.from_envvar("TIGEREYE_SETTINGS", silent=True)
    configure_extensions(app)
    configure_views(app)
    app.json_encoder = JSONEncoder

    if not app.debug:
        app.logger.setLevel(logging.INFO)
        mail_handler = SMTPHandler(
            app.config['EMAIL_HOST'],
            app.config['SERVER_EMAIL'],
            app.config['ADMINS'],
            'TIGEREYE ALERT',
            credentials=(app.config['EMAIL_HOST_USER'],
                         app.config['EMAIL_HOST_PASSWORD']))
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(Formatter('''
        Message type:       %(levelname)s
        Location:           %(pathname)s:%(lineno)d
        Module:             %(module)s
        Function:           %(funcName)s
        Time:               %(asctime)s

        Message:

        %(message)s
        '''))
        app.logger.addHandler(mail_handler)

        file_handler = FileHandler(os.path.join(app.config['LOG_DIR'],
                                                'app.log'))
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(Formatter(
            '%(asctime)s %(levelname)s: %(message)s'))
        app.logger.addHandler(file_handler)

    return app


def configure_extensions(app):
    db.init_app(app)
    # 注意：当使用app.debug模式时，redis中的数据将会在server重启后丢弃。
    if app.debug or app.testing:
        extensions.redi = FlaskRedis.from_custom_provider(MockRedisWrapper)
    else:
        extensions.redi = FlaskRedis()
    extensions.redi.init_app(app)


def configure_views(app):
    from tigereye.api.misc import MiscView
    from tigereye.api.cinema import CinemaView
    from tigereye.api.hall import HallView
    from tigereye.api.play import PlayView
    from tigereye.api.seat import SeatView
    from tigereye.api.movie import MovieView
    from tigereye.api.order import OrderView
    for view in locals().values():
        if type(view) == type and issubclass(view, ApiView):
            view.register(app)
