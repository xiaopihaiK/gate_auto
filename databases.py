#!/usr/bin/python
# -*- coding: UTF-8 -*-
# code by Benl0xe 
# email:kang.liu@qt.cn
import pymysql

import pymysql.cursors

# 获取数据库连接
connection = pymysql.connect(
    host='',
    port=3306,
    user='order',
    password='',
    db='order'
)

def insert(order_id,timep,order_price,status,currency_pair):
    try:
        # 获取会话指针
        with connection.cursor() as cursor:
            # 创建sql语句
            sql = "insert into `order`(`order_id`,`timep`,`order_price`,`status`,`currency_pair`) values (%s,%s,%s,%s,%s)"

            # 执行sql
            cursor.execute(sql, (order_id,timep,order_price,status,currency_pair))
            # cursor.execute(sql)
            # 提交
            connection.commit()
            print '数据插入成功...'
    except Exception as e:
        print e
    finally:
        connection.close()

def query_open():
    all_open = []
    try:
        # 获取会话指针
        with connection.cursor() as cursor:
            # 创建sql语句
            sql = "select order_id,currency_pair from `order` where status = 'open';"

            # 执行sql
            cursor.execute(sql,)
            # cursor.execute(sql)
            # 提交
            result_open = cursor.fetchall()
            for i in result_open:
                open_flag = i[0]+'-'+i[1]
                all_open.append(open_flag)
            connection.commit()
            print '数据查询成功...'
    except Exception as e:
        print e
    return all_open
