# -*- coding: utf-8 -*-
"""
    tigereye.configs.default
    ~~~~~~~~~~~~~~~~~~~~~~~

"""
import os
import sys

_VERSION_STR = '{0.major}{0.minor}'.format(sys.version_info)


class DefaultConfig(object):

    # Get the app root path
    _basedir = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(
                            os.path.dirname(__file__)))))

    DEBUG = True
    TESTING = False

    # auto unlock after seat locked 10 minutes
    AUTO_UNLOCK_SECONDS = 10 * 60
    # Logs
    # If SEND_LOGS is set to True, the admins (see the mail configuration) will
    # recieve the error logs per email.
    SEND_LOGS = False
    LOG_DIR = os.path.join(_basedir, 'logs')
    # The filename for the info and error logs. The logfiles are stored at
    INFO_LOG = "info.log"
    ERROR_LOG = "error.log"

    # Default Database
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + _basedir + '/' + \
    #                           'db.sqlite3'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/tigereye'
    # This option will be removed as soon as Flask-SQLAlchemy removes it.
    # At the moment it is just used to suppress the super annoying warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # This will print all SQL statements
    SQLALCHEMY_ECHO = True

    # Security
    SECRET_KEY = 'nidawoya'

    # Caching
    # CACHE_TYPE = "simple"
    # CACHE_DEFAULT_TIMEOUT = 60

    # Mail
    # MAIL_SERVER = "localhost"
    # MAIL_PORT = 25
    # MAIL_USE_SSL = False
    # MAIL_USE_TLS = False
    # MAIL_USERNAME = "noreply@example.org"
    # MAIL_PASSWORD = ""
    # MAIL_DEFAULT_SENDER = ("Default Sender", "noreply@example.org")
    # # Where to logger should send the emails to
    ADMINS = ["guye@qq.com"]

    # Flask-Redis
    # REDIS_ENABLED = False
    # REDIS_URL = "redis://:password@localhost:6379"
    # REDIS_DATABASE = 0

    # URL Prefixes
    API_URL_PREFIX = ""
