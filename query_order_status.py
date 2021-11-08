#!/usr/bin/python
# -*- coding: UTF-8 -*-
# code by Benl0xe
# email:kang.liu@qt.cn
import time
import hashlib
import hmac
import requests
import get_sign
from decimal import Decimal
import databases

# 根据order_id查询订单状态
def query_open_staute(order_id,currency_pair):  # 根据order_id查询状态
    host = "https://api.gateio.ws"
    prefix = "/api/v4"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    url = '/spot/orders/'+str(order_id)
    query_param = 'currency_pair='+str(currency_pair)
    # `gen_sign` 的实现参考认证一章
    sign_headers = get_sign.gen_sign('GET', prefix + url, query_param)
    headers.update(sign_headers)
    r = requests.request('GET', host + prefix + url + "?" + query_param, headers=headers)
    # print(r.json())
    print 'id:'+str(r.json()['id'])+'状态:'+str(r.json()['status'])

# 查询mysql-status为open
def check_mysql_status_open():
    while True:
        open_result = databases.query_open()
        if len(open_result) == 1:
            order_id = open_result[0].split('-')[0]
            currency_pair = open_result[0].split('-')[1]
            print order_id
            print currency_pair
            query_open_staute(order_id = order_id , currency_pair = currency_pair)

        else:
            for i in open_result:
                order_id = i.split('-')[0]
                currency_pair = i.split('-')[1]
                print order_id
                query_open_staute(order_id=order_id, currency_pair=currency_pair)
                # print currency_pair
        time.sleep(5)

check_mysql_status_open()
