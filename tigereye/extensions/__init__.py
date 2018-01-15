# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from mockredis import MockRedis

db = SQLAlchemy()


class MockRedisWrapper(MockRedis):
    '''A wrapper to add the `from_url` classmethod'''
    @classmethod
    def from_url(cls, *args, **kwargs):
        return cls()


redi = None
