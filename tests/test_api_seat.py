#coding=utf-8

from flask import json
from tigereye.helper.code import Code
from tigereye.models.order import Order
from tigereye.models.seat import SeatStatus
from .helper import FlaskTestBase

pid = 1
sid_list = [1, 2]
sid = ','.join([str(i) for i in sid_list])
price = 5000
orderno = 'test-%s-%s' % (pid, sid)


class TestApiSeat(FlaskTestBase):

    def test_seat1_lock(self):
        locked_seats_num = len(sid_list)
        rv = self.get_succ_json('seat/lock/',
                           method='POST',
                           orderno=orderno,
                           pid=pid,
                           price=price,
                           sid=sid)
        self.assertEqual(rv['data']['locked_seats_num'], locked_seats_num)

        # 确认座位图已经改变
        rv = self.get_succ_json('play/seats/', pid=pid)
        succ_count = 0
        for seat in rv['data']:
            if seat['orderno'] == orderno:
                self.assertEqual(seat['status'], SeatStatus.locked.value)
                succ_count += 1
        self.assertEqual(succ_count, locked_seats_num)

        # 确定重复锁座失败
        data = self.get_json('seat/lock/',
                                  method='POST',
                                  orderno='test-%s-%s' % (pid, sid),
                                  pid=pid,
                                  price=price,
                                  sid=sid)
        self.assertEqual(data['rc'], Code.seat_lock_failed.value)

    def test_seat2_unlock(self):
        seats_num = len(sid_list)
        rv = self.get_succ_json('seat/lock/',
                           method='POST',
                           orderno=orderno,
                           pid=pid,
                           price=price,
                           sid=sid)
        self.assertEqual(rv['data']['locked_seats_num'], seats_num)
        rv = self.get_succ_json('seat/unlock/',
                           method='POST',
                           orderno='test-%s-%s' % (pid, sid),
                           pid=pid,
                           sid=sid)
        self.assertEqual(rv['data']['unlocked_seats_num'], seats_num)

        # 确认座位图已经改变
        rv = self.get_succ_json('play/seats/', pid=pid)
        succ_count = 0
        for seat in rv['data']:
            if seat['sid'] in sid_list:
                self.assertEqual(seat['status'], SeatStatus.ok.value)
                succ_count += 1
        self.assertEqual(succ_count, seats_num)
        # order = Order.getby_orderno(orderno)
        # order.delete()
        # order.commit()

    def test_seat3_buy(self):
        # 先锁定座位
        _orderno = orderno + 'buy'
        self.get_succ_json('seat/lock/',
                       method='POST',
                       orderno=_orderno,
                       pid=pid,
                       price=price,
                       sid=sid)
        # 再购买
        bought_seats_num = len(sid_list)
        seats = ','.join(['%s-0-%s' % (i, price) for i in sid_list])
        rv = self.get_succ_json('seat/buy/',
                           method='POST',
                           orderno=_orderno,
                           seats=seats)
