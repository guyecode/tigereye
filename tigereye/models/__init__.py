from datetime import datetime, date
from flask import json as _json
from sqlalchemy import inspect
from tigereye.extensions import db
from tigereye.helper.wetime import default_datetime_format, default_date_format

__all__ = ['cinema.Cinema']

class Model(object):
    @classmethod
    def get(cls, primary_key):
        return cls.query.get(primary_key)

    @property
    def persistent(self):
        return inspect(self).persistent

    def put(self):
        if self.persistent:
            self._json_cache = self.__json__()
        db.session.add(self)

    def delete(self):
        db.session.delete(self)

    @classmethod
    def commit(cls):
        db.session.commit()

    @classmethod
    def rollback(cls):
        db.session.rollback()

    def save(self):
        try:
            self.put()
            self.commit()
        except Exception:
            self.rollback()
            raise

    def __json__(self):
        _d = {}
        if hasattr(self, '_json_cache') and self._json_cache:
            _d = self._json_cache
        for k, v in vars(self).items():
            if k.startswith('_'):
                continue
            if isinstance(v, datetime):
                v = v.strftime(default_datetime_format)
            if isinstance(v, date):
                v = v.strftime(default_date_format)
            _d[k] = v
        return _d

    def __repr__(self):
        return '####<%s %s> ' % \
            (self.__class__.__name__, self.__mapper__.primary_key[0].name)

    def __len__(self):
        return 1


class JSONEncoder(_json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Model):
            return o.__json__()
        return _json.JSONEncoder.default(self, o)
