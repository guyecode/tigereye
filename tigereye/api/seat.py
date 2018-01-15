# coding=utf-8
from datetime import datetime

from flask import request
from flask_classy import route

from tigereye.api import ApiView
from tigereye.models.play import Play
from tigereye.models.seat import PlaySeat
from tigereye.models.order import Order, OrderStatus
from tigereye.extensions.validator import Validator, multi_int, multi_complex_int
from tigereye.helper.code import Code


class SeatView(ApiView):
    """座位相关操作API"""

    @Validator(pid=int, sid=multi_int, price=int, orderno=str)
    @route('/lock/', methods=['POST'])
    def lock(self):
        pid = request.params['pid']
        sid = request.params['sid']
        price = request.params['price']
        orderno = request.params['orderno']
        play = Play.get(pid)
        if not play:
            return Code.play_does_not_exist, {'pid': pid}
        if price < play.lowest_price:
            return Code.prcice_less_than_the_lowest_price, {'price': price}

        locked_seats_num = PlaySeat.lock(orderno, pid, sid)
        if not locked_seats_num:
            return Code.seat_lock_failed, {}
        order = Order.create(play.cid, pid, sid)
        order.seller_order_no = orderno
        order.status = OrderStatus.locked.value
        order.tickets_num = locked_seats_num
        order.save()
        return {'locked_seats_num': locked_seats_num}

    @Validator(pid=int, sid=multi_int, orderno=str)
    @route('/unlock/', methods=['POST'])
    def unlock(self):
        pid = request.params['pid']
        sid = request.params['sid']
        orderno = request.params['orderno']
        order = Order.getby_orderno(orderno)
        if not order:
            return Code.order_does_not_exist, {'orderno': orderno}
        if order.status != OrderStatus.locked.value:
            return Code.order_status_error, {}
        unlocked_seats_num = PlaySeat.unlock(orderno, pid, sid)
        if not unlocked_seats_num:
            return Code.seat_unlock_failed, {}
        order.status = OrderStatus.unlocked.value
        order.save()
        return {'unlocked_seats_num': unlocked_seats_num}

    @Validator(seats=multi_complex_int, orderno=str)
    @route('/buy/', methods=['POST'])
    def buy(self):
        seats = request.params['seats']
        orderno = request.params['orderno']
        order = Order.getby_orderno(orderno)
        if not order:
            return Code.order_does_not_exist, {'orderno': orderno}
        if order.status != OrderStatus.locked.value:
            return Code.order_status_error, \
                   {'orderno': orderno, 'status': order.status}
        order.seller_order_no = request.params['orderno']
        order.amount = order.amount or 0
        sid_list = []
        for sid, handle_fee, price in seats:
            sid_list.append(sid)
            order.amount += handle_fee + price
        bought_seats_num = PlaySeat.buy(orderno, order.pid, sid_list)
        if not bought_seats_num:
            return Code.seat_buy_failed, {}
        order.tickets_num = len(seats)
        order.paid_time = datetime.now()
        order.status = OrderStatus.paid.value
        order.gen_ticket_flag()
        order.save()
        return {'bought_seats_num': bought_seats_num,
                'ticket_flag': order.ticket_flag}
