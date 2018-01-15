from datetime import datetime

default_datetime_format = '%Y-%m-%d %H:%M:%S'
default_date_format = '%Y-%m-%d'


def today():
    return datetime.today().strftime('%Y%m%d')


def now():
    return datetime.now().strftime('%Y%m%d%H%M%S')
