# -*- coding: utf-8 -*-

from tigereye.configs.default import DefaultConfig


class TestConfig(DefaultConfig):

    TESTING = True
    JSON_SORT_KEYS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
