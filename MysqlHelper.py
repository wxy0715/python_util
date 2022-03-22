#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time : 2020/12/23 15:54
# @Author : wxy
# @contact: wxy18955007261@163.com
# @file: MysqlHelper.py
# @desc: 封装mysql
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

    def insert(self, sql, params=None):
        return self.__common(sql, params)

    """删除"""

    def delete(self, sql, params=None):
        return self.__common(sql, params)

    """修改"""

    def update(self, sql, params=None):
        return self.__common(sql, params)

    """查询一条"""

    def fetchone(self, sql, params=None):
        data = None
        try:
            count = self.cursor.execute(sql, params)
            if count != 0:
                data = self.cursor.fetchone()
        except Exception as ex:
            print(ex)
        return data

    """查询所有"""

    def fetchall(self, sql, params=None):
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


if __name__ == "__main__":
    mysqlUtil = MysqlHelper(
        host="39.97.123.62",
        user='lsblj',
        password='lsblj',
        database='lsblj',
        port=3306,
        charset='utf8',
    )
    sql = """
         SELECT * FROM lsblj_user
     """
    data = mysqlUtil.fetchall(sql, params=None)
    print(data)
