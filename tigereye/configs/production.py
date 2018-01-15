# -*- coding: utf-8 -*-

from tigereye.configs.default import DefaultConfig


class ProductionConfig(DefaultConfig):

    DEBUG = False
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = False
    SQLALCHEMY_ECHO = False
    SEND_LOGS = True
