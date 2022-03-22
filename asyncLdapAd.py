#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@Time : 2021/1/23 16:37
@Author : wxy
@contact: wxy18955007261@163.com
@file: asyncLdapAd.py
@desc:
"""
import os
import sys

if os.system('pip3 install python-crontab') != 0:
    print("crontab")
    sys.exit(1)

from crontab import CronTab

class CrontabOperator(object):
    def __init__(self):
        # 创建当前用户的crontab
        self.cron = CronTab(user=user)

    def add_crontab_job(self, cmmand_line, time_str, commont_name, user):
        # 创建任务
        job = self.cron.new(command=cmmand_line)
        # 设置任务执行周期
        job.setall(time_str)
        # 给任务添加一个标识，给任务设置comment，这样就可以根据comment查询
        job.set_comment(commont_name)
        self.cron.write_to_user(user=user)  # 指定用户，写入指定用户下的crontab任务

    def del_crontab_jobs(self, comment_name, user):
        self.cron.remove_all(comment=comment_name)
        self.cron.remove_all(comment=comment_name + ' =')
        self.cron.write_to_user(user=user)  # 指定用户,删除指定用户下的crontab任务


if __name__ == '__main__':
    async_id = sys.argv[1]  # 获取传入的id
    async_status = sys.argv[2]  # 获取传入的状态 0增加1删除
    cmmand_line = '/usr/bin/curl https://localhost:8080/configLdapAd/asyncUser?ids=' + async_id
    commont_name = "async" + async_id
    user = "root"
    # 创建一个实例
    crontab_update = CrontabOperator()
    if async_status == '0':
        print("增加定时任务!")
        async_day = sys.argv[3] % 31  # 获取传入的天数
        crontab_update.add_crontab_job(cmmand_line, sys.argv[3], commont_name, user)
    elif async_status == '1':
        print("删除定时任务!")
        crontab_update.del_crontab_jobs(commont_name, user)
    else:
        print("同步传参错误!")
        sys.exit(1)
    print("同步成功!")
