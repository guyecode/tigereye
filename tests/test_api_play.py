#coding=utf-8

from flask import json
from .helper import FlaskTestBase


class TestApiPlay(FlaskTestBase):

    def test_play_seats(self):
        pid = 1
        rv = self.get_succ_json('play/seats/', pid=pid)
        for seat in rv['data']:
            self.assertEqual(seat['pid'], pid)
