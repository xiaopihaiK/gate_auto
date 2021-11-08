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
import get_price # get_price file
import databases

symbol = raw_input('输入需要购买的币种（SHIB_USDT）：')

result_price = get_price.get_price(symbol = symbol) # retern price,amount,USDT

buy_one = result_price[0] # 买一的价格
amount = result_price[1] # 设定USDT后买入的数量
USDT = result_price[2] # 设定买入的USDT


print '买一价格：' + str(buy_one)
print '购买的数量为：' + str(amount)
print '共购买了：' + str(USDT) + 'USDT'

def order_buy(symbol,amount,price):
    host = "https://api.gateio.ws"
    prefix = "/api/v4"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    url = '/spot/orders'
    query_param = ''
    body = '{"currency_pair":"'+str(symbol)+'","type":"limit","account":"spot","side":"buy","iceberg":"0","amount":"'+str(amount)+'","price":"'+str(price)+'","auto_borrow":false}'
    sign_headers = get_sign.gen_sign('POST', prefix + url, query_param, body)
    headers.update(sign_headers)
    r = requests.request('POST', host + prefix + url, headers=headers, data=body)
    print(r.json())
    order_price = r.json()['price']
    order_id = r.json()['id']
    status = r.json()['status']
    create_time = r.json()['create_time']
    currency_pair = r.json()['currency_pair']
    return order_id,order_price,status,create_time,currency_pair

res = order_buy(symbol=symbol,amount=amount,price=buy_one)


databases.insert(order_id=res[0],order_price=res[1],status=res[2],currency_pair=res[4],timep=res[3])


print res
