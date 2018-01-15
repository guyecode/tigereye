# coding=utf-8

from flask import request, current_app
from flask_classy import route
from tigereye.api import ApiView


class MiscView(ApiView):
    route_base = '/'

    def index(self):
        return self.check()

    def check(self):
        current_app.logger.info('checked from %s' % request.remote_addr)
        if current_app.debug:
            return "I'm fine."
        return "I'm OK."

    def ping(self):
        current_app.ping = request.args
        return 'ping'

    def pong(self):
        return current_app.ping

    def error(self):
        1 / 0
