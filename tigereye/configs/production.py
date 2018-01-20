# -*- coding: utf-8 -*-

from tigereye.configs.default import DefaultConfig


class ProductionConfig(DefaultConfig):

    DEBUG = False
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = False
    SQLALCHEMY_ECHO = False
    SEND_LOGS = True

    EMAIL_HOST = 'smtp.exmail.qq.com'
    EMAIL_PORT = 465
    EMAIL_HOST_USER = SERVER_EMAIL = DEFAULT_FROM_EMAIL = 'test1@iguye.com'
    EMAIL_HOST_PASSWORD = 'P67844QUssW3'
    EMAIL_USE_SSL = True
    ADMINS = ["guye@iguye.com"]