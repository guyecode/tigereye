# coding=utf-8
from datetime import datetime

from flask import request
from flask_classy import route

from tigereye.api import ApiView
from tigereye.models.play import Play
from tigereye.models.movie import Movie
from tigereye.models.seat import PlaySeat
from tigereye.models.order import Order, OrderStatus
from tigereye.extensions.validator import Validator, multi_int
from tigereye.helper.code import Code


class OrderView(ApiView):
    """订单相关操作API"""

    @Validator(orderno=str)
    def status(self):
        """查询订单状态"""
        orderno = request.params['orderno']
        order = Order.getby_orderno(orderno)
        if not order:
            return Code.order_does_not_exist, {'orderno': orderno}
        return {'status': order.status}

    @Validator(orderno=str)
    def ticket(self):
        """查询取票码"""
        orderno = request.params['orderno']
        order = Order.getby_orderno(orderno)
        if not order:
            return Code.order_does_not_exist, {'orderno': orderno}
        return {'ticket_flag': order.ticket_flag}

    @route('/ticket/info')
    @Validator(orderno=str)
    def ticket_info(self):
        """获取票面信息"""
        orderno = request.params['orderno']
        order = Order.getby_orderno(orderno)
        if not order:
            return Code.order_does_not_exist, {'orderno': orderno}
        order.play = Play.get(order.pid)
        order.movie = [Movie.get(order.play.mid)]
        order.tickets = PlaySeat.getby_orderno(orderno)
        return order

    @route('/ticket/print', methods=['POST'])
    @Validator(orderno=str, ticket_flag=str, sid=multi_int)
    def print_ticket(self):
        seats = request.params['sid']
        ticket_flag = request.params['ticket_flag']
        orderno = request.params['orderno']
        order = Order.getby_orderno(orderno)
        if not order:
            return Code.ticket_flag_error, {'ticket_flag': ticket_flag}
        if order.status == OrderStatus.printed.value:
            return Code.ticket_printed_already, {'status': order.status}
        if order.status != OrderStatus.paid.value:
            return Code.order_not_paid_yet, {'status': order.status}
        if not order.validate(ticket_flag):
            return Code.ticket_flag_error, {'ticket_flag': ticket_flag}
        printed_num = PlaySeat.print_tickets(order.seller_order_no, order.pid,
                                             seats)
        if not printed_num:
            return Code.ticket_print_failed, {}
        order.status = OrderStatus.printed.value
        order.printed_time = datetime.now()
        order.save()
        return {'printed_num': printed_num}

    @route('/ticket/refund', methods=['POST'])
    @Validator(orderno=str, ticket_flag=str, sid=multi_int)
    def refund_ticket(self):
        orderno = request.params['orderno']
        ticket_flag = request.params['ticket_flag']
        seats = request.params['sid']
        order = Order.getby_orderno(orderno)
        if not order:
            return Code.order_does_not_exist, {'orderno': orderno}
        if order.status == OrderStatus.printed.value:
            return Code.ticket_printed_already, {}
        if order.status != OrderStatus.paid.value:
            return Code.order_not_paid_yet, {}
        if not order.validate(ticket_flag):
            return Code.ticket_flag_error, {'ticket_flag': ticket_flag}
        refund_num = PlaySeat.refund(orderno, order.pid, seats)
        if not refund_num:
            return Code.ticket_refund_failed, {}
        order.status = OrderStatus.refund.value
        order.refund_time = datetime.now()
        order.save()
        return {'refund_num': refund_num}
