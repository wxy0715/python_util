#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Time : 2021/3/2 9:08
@Author : wxy
@contact: wxy18955007261@163.com
@file: modify.py
@desc:
"""
import sys

import pymysql
import os
import time

# 完整结构数据库
db1_host = '127.0.0.1'
db1_user = 'lsblj'
db1_pwd = 'lsblj'
db1_dbname = 'lsblj_default'

# 待升级的数据库
db2_host = '127.0.0.1'
db2_user = 'lsblj'
db2_pwd = 'lsblj'
db2_dbname = 'lsblj'

# 新数据库信息
new_tablename = []
# 旧数据库信息
old_tablename = []
# 修改语句
sql = ''


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


if __name__ == '__main__':
    mysqlUtil_old = MysqlHelper(
        host=db2_host,
        user=db2_user,
        password=db2_pwd,
        database=db2_dbname,
        port=3306,
        charset='utf8',
    )
    mysqlUtil_new = MysqlHelper(
        host=db1_host,
        user=db1_user,
        password=db1_pwd,
        database=db1_dbname,
        port=3306,
        charset='utf8',
    )
    os.system("mysqldump -h" + db2_host + " -u"+db2_user+" -p" + db2_pwd + " "+db2_dbname + " > lsblj_backup-"+time.strftime("%Y%m%d", time.localtime()) +".sql")

    # 1.查询完整结构数据库的所有表
    result = mysqlUtil_new.fetchall("SHOW TABLES FROM " + db1_dbname, params=None)
    if not result:
        print("DB Error, could not list tables")
        sys.exit(1)
    for row in result:
        new_tablename.append(row[0])

    # 2.查询旧数据库的所有表
    result = mysqlUtil_old.fetchall("SHOW TABLES FROM " + db2_dbname, params=None)
    if result:
        for row in result:
            old_tablename.append(row[0])

    sql += 'SET FOREIGN_KEY_CHECKS=0;\n'
    # 先建表-防止外键索引报错
    for index in range(len(new_tablename)):
        if new_tablename[index] not in old_tablename:
            # 创建表
            result = mysqlUtil_new.fetchone("SHOW CREATE TABLE "+new_tablename[index], params=None)
            sql += result[1]+";\n"
    fo = open("change.sql", "w+")
    sql += 'SET FOREIGN_KEY_CHECKS=1;\n'
    line = fo.write(sql)
    fo.close()
    os.system("mysql -u"+db2_user + " -p" + db2_pwd + " " + db2_dbname + " <" + os.getcwd()+"/change.sql")
    print("新表建立完成")
    old_tablename = []
    result = mysqlUtil_old.fetchall("SHOW TABLES FROM " + db2_dbname, params=None)
    if result:
        for row in result:
            old_tablename.append(row[0])

    sql = ''
    sql += 'SET FOREIGN_KEY_CHECKS=0;\n'
    # 比较表结构 --先不管主键
    for index in range(len(new_tablename)):
        if new_tablename[index] in old_tablename:
            # 先查询建表语句
            old = mysqlUtil_old.fetchall("SHOW CREATE TABLE " + new_tablename[index], params=None)[0][1]
            new = mysqlUtil_new.fetchall("SHOW CREATE TABLE " + new_tablename[index], params=None)[0][1]
            list_old = str(old).split("\n")
            list_new = str(new).split("\n")
            # 旧表操作 先删除外键索引再删除AUTO_INCREMENT
            for key in list_old:
                if str(key).find('AUTO_INCREMENT') >= 0 and str(key).split()[0] != ")":
                    # 删除旧表的自增属性
                    sql += 'ALTER TABLE ' + new_tablename[index] + ' MODIFY ' + str(key).replace("AUTO_INCREMENT", "").replace(",", "") +";\n"
                if str(key).find('PRIMARY KEY') >= 0:
                    continue
                elif str(key).find('CONSTRAINT') >= 0:
                    # 删除旧表的外键索引
                    sql += 'ALTER TABLE ' + new_tablename[index] + ' DROP FOREIGN KEY ' + str(key).split()[1] +";\n"
    print("删除外键索引和自增属性完成")
    # 比较表结构 --主键操作和普通字段
    for index in range(len(new_tablename)):
        if new_tablename[index] in old_tablename:
            # 先查询建表语句
            old = mysqlUtil_old.fetchall("SHOW CREATE TABLE " + new_tablename[index], params=None)[0][1]
            new = mysqlUtil_new.fetchall("SHOW CREATE TABLE " + new_tablename[index], params=None)[0][1]
            list_old = str(old).split("\n")
            list_new = str(new).split("\n")
            # 旧表操作 删除主键索引
            for key in list_old:
                if str(key).find('PRIMARY') >= 0:
                    sql += 'ALTER TABLE ' + new_tablename[index] + ' DROP PRIMARY KEY '+";\n"
                elif str(key).find('UNIQUE') >= 0:
                    # 删除旧表的唯一索引
                    sql += 'ALTER TABLE ' + new_tablename[index] + ' DROP KEY ' + str(key).split()[2] + ";\n"
                elif str(key).find('CONSTRAINT') < 0 and str(key).find('KEY') >= 0:
                    # 删除旧表的普通索引
                    sql += 'ALTER TABLE ' + new_tablename[index] + ' DROP KEY ' + str(key).split()[1] + ";\n"
    print("删除唯一索引和普通索引完成")
    for index in range(len(new_tablename)):
        if new_tablename[index] in old_tablename:
            old = mysqlUtil_old.fetchall("SHOW CREATE TABLE " + new_tablename[index], params=None)[0][1]
            new = mysqlUtil_new.fetchall("SHOW CREATE TABLE " + new_tablename[index], params=None)[0][1]
            list_new = str(new).split("\n")
            for key in list_new:
                if str(key).find('PRIMARY') >= 0:
                    sql += 'ALTER TABLE ' + new_tablename[index] + ' ADD PRIMARY KEY' + str(key).split()[2].replace("),", ")") + ";\n"
                elif str(key).find('UNIQUE') >= 0:
                    # 添加旧表的唯一索引
                    sql += 'ALTER TABLE ' + new_tablename[index] + ' ADD ' + str(key).replace("),", ")") + ";\n"
                elif str(key).find('CONSTRAINT') < 0 and str(key).find('KEY') >= 0:
                    # 添加旧表的普通索引
                    sql += 'ALTER TABLE ' + new_tablename[index] + ' ADD ' + str(key).replace("),", ")") + ";\n"
    print("添加唯一索引和普通索引完成")
    for index in range(len(new_tablename)):
        if new_tablename[index] in old_tablename:
            old = mysqlUtil_old.fetchall("SHOW CREATE TABLE " + new_tablename[index], params=None)[0][1]
            new = mysqlUtil_new.fetchall("SHOW CREATE TABLE " + new_tablename[index], params=None)[0][1]
            list_new = str(new).split("\n")
            for key in list_new:
                if str(key).find('CONSTRAINT') >= 0:
                    # 添加旧表的外键索引
                    sql += 'ALTER TABLE ' + new_tablename[index] + ' ADD ' + str(key).replace(",","") + ";\n"
    print("添加外键索引完成")
    for index in range(len(new_tablename)):
        if new_tablename[index] in old_tablename:
            # 先查询建表语句
            old = mysqlUtil_old.fetchall("SHOW CREATE TABLE " + new_tablename[index], params=None)[0][1]
            new = mysqlUtil_new.fetchall("SHOW CREATE TABLE " + new_tablename[index], params=None)[0][1]
            list_old = str(old).split("\n")
            list_new = str(new).split("\n")
            # 普通字段操作
            for key in list_new:
                if str(key).split()[0].upper() != "CREATE" and str(key).split()[0] != ")" and str(key).split()[0] != "KEY" and str(key).split()[0] != "UNIQUE" and str(key).split()[0] != "CONSTRAINT" and str(key).split()[0] != "PRIMARY":
                    if str(list_old).find(str(key).split()[0]) >= 0:
                        # 修改字段
                        if str(key).endswith(","):
                            sql += 'ALTER TABLE ' + new_tablename[index] + ' MODIFY ' + str(key)[:-1] + ";\n"
                        else:
                            sql += 'ALTER TABLE ' + new_tablename[index] + ' MODIFY ' + str(key) + ";\n"
                    else:
                        # 添加字段
                        if str(key).endswith(","):
                            sql += 'ALTER TABLE ' + new_tablename[index] + ' ADD ' + str(key)[:-1] + ";\n"
                        else:
                            sql += 'ALTER TABLE ' + new_tablename[index] + ' ADD ' + str(key) + ";\n"
    print("添加字段和修改字段完成")
    fo = open("change.sql", "w+")
    sql += 'SET FOREIGN_KEY_CHECKS=1;\n'
    line = fo.write(sql)
    fo.close()
    print("-----开始导入sql文件-----")
    os.system("mysql -u"+db2_user + " -p" + db2_pwd + " " + db2_dbname + " <" + os.getcwd()+"/change.sql")
    # 如果没有lsblj_config 就先执行上面的语句创建表,然后再进行判断数据是否一致
    mysqlUtil_old.fetchall("commit", params=None)
    mysqlUtil_new.fetchall("commit", params=None)
    db2_config = mysqlUtil_old.fetchall("select * from lsblj_config", params=None)
    # 判断db1里面有哪些是db2中没有的
    db2_data = []
    if db2_config:
        for old in db2_config:
            db2_data.append(old[1])
    mysqlUtil_new.fetchall("commit", params=None)
    db1_config = mysqlUtil_new.fetchall("select * from lsblj_config", params=None)
    for new in db1_config:
        if new[1] not in db2_data:
            mysqlUtil_old.insert("insert into lsblj_config(name, value) values (%s, %s)", params=(new[1], new[2]))
    mysqlUtil_new.close()
    mysqlUtil_old.close()
    print("更新完成")