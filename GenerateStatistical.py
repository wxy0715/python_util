#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
@Time : 2021/4/12 19:25
@Author : wxy
@contact: wxy18955007261@163.com
@file: GenerateStatistical.py
@desc: 自动生成统计分析日报,周报,月报---使用方式 0 0 * * * /usr/bin/python3 脚本位置
"""

import os
import time

import pymysql

class MysqlHelper:
    """
    初始化参数
    :param host:        主机
    :param user:        用户名
    :param password:    密码
    :param database:    数据库
    :param port:        端口号，默认是3306
    :param charset:     编码，默认是utf8
    """

    def __init__(self, host, user, password, database, port, charset):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.charset = charset
        """获取连接和游标"""
        self.db = pymysql.connect(host=self.host,
                                  user=self.user,
                                  password=self.password,
                                  database=self.database,
                                  port=self.port,
                                  charset=self.charset)
        self.cursor = self.db.cursor()

    """私有公共函数,主要用于增删改"""

    def __common(self, sql, params):
        count = 0
        try:
            count = self.cursor.execute(sql, params)
            self.db.commit()
        except Exception as ex:
            print(ex)
        return count

    """增加"""

    def insert(self, sql, params):
        return self.__common(sql, params)

    """删除"""

    def delete(self, sql, params):
        return self.__common(sql, params)

    """修改"""

    def update(self, sql, params):
        return self.__common(sql, params)

    """查询一条"""

    def fetchone(self, sql, params):
        data = None
        try:
            count = self.cursor.execute(sql, params)
            if count != 0:
                data = self.cursor.fetchone()
        except Exception as ex:
            print(ex)
        return data

    """查询所有"""

    def fetchall(self, sql, params):
        data = None
        try:
            count = self.cursor.execute(sql, params)
            if count != 0:
                data = self.cursor.fetchall()
        except Exception as ex:
            print(ex)
        return data

    """关闭连接"""

    def close(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.db is not None:
            self.db.close()


now_time = time.time()
last_day_time = time.time() - 60 * 60 * 24


def exec_day(name, types, method):
    os.system('/usr/bin/curl -i "http://127.0.0.1:8080/export/exportByPython?interval=hour&start=' + str(last_day_time) + '&end='
              + str(now_time) + '&name=' + str(name) + '&type=' + types + '"')


def exec_week(name, types, exec_days, method):
    week = (time.strftime("%w", time.localtime()))
    if exec_days == 7:
        if week == '0':
            last_week_time = time.time() - 60 * 60 * 24 * 7
            os.system('/usr/bin/curl -i "http://127.0.0.1:8080/export/exportByPython?interval=week&start=' + str(last_week_time)
                      + '&end=' + str(now_time) + '&name=' + str(name) + '&type=' + types + '"')
    else:
        if week == exec_days-1:
            last_week_time = time.time() - 60 * 60 * 24 * 7
            os.system('/usr/bin/curl -i "http://127.0.0.1:8080/export/exportByPython?interval=week&start=' + str(last_week_time)
                      + '&end=' + str(now_time) + '&name=' + str(name) + '&type=' + types + '"')


def exec_month(name, types, exec_days, method):
    month = (time.strftime("%d", time.localtime()))
    if exec_days < 10:
        exec_days = '0'+str(exec_days)
        if month == exec_days:
            last_month_time = time.time() - 60 * 60 * 24 * 31
            os.system('/usr/bin/curl -i "http://127.0.0.1:8080/export/exportByPython?interval=month&start=' + str(last_month_time) + '&end='
                      + str(now_time) + '&name=' + str(name) + '&type=' + types + '"')
    else:
        if month == str(exec_days):
            last_month_time = time.time() - 60 * 60 * 24 * 31
            os.system('/usr/bin/curl -i "http://127.0.0.1:8080/export/exportByPython?interval=month&start=' + str(last_month_time) + '&end='
                      + str(now_time) + '&name=' + str(name) + '&type=' + types + '"')


if __name__ == '__main__':
    mysqlUtil = MysqlHelper(
        host='127.0.0.1',
        user='lsblj',
        password='lsblj',
        database='lsblj',
        port=3306,
        charset='utf8',
    )
    # 查询是否存在策略
    result = mysqlUtil.fetchall("SELECT * FROM lsblj_regular_report", None)
    if not result:
        print("could not list data")
        exit()
    # 0-id,1-策略名称,2-报表类型,3-执行方式,4-具体天数,5-导出方式
    for row in result:
        # 策略策略为1的按天
        if row[3] == 1:
            exec_day(row[1], str(row[2]).replace(",",""), row[5])
        # 策略策略为2的按周
        elif row[3] == 2:
            exec_week(row[1], str(row[2]).replace(",",""), row[4], row[5])
        # 策略策略为2的按月
        elif row[3] == 3:
            exec_month(row[1], str(row[2]).replace(",",""), row[4], row[5])
    # 生成月报
    # day = (time.strftime("%d", time.localtime()))
    # if day == '1':
    #     # 获取上个月有多少天
    #     month = (time.strftime("%m", time.localtime(last_day_time)))
    #     year = (time.strftime("%Y", time.localtime(last_day_time)))
    #     print(month+"-"+year)
    #     days = calendar.monthrange(int(year), int(month))[1]
    #     last_month_time = time.time() - 60 * 60 * 24 * days
    #     os.system('/usr/bin/curl -i "http://127.0.0.1:8080/export/exportByPython?interval=month&start=' + str(now_time) + '&end=' + str(last_month_time) + '"')
