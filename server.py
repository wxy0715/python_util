#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
@Time : 2021/10/28 19:09
@Author : wxy
@contact: wxy18955007261@163.com
@file: server.py
@desc: windows改密服务端和client配套
"""
import os
import socket
import subprocess
import traceback

cmd="net user test4 123456 /add"
import ctypes


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 44444))
    server.listen(5)  # 开始监听TCP传入连接
    print('starting....')
    while True:
        conn, addr = server.accept()
        # 接受用户名和密码
        client_msg = conn.recv(1024).decode()
        user = client_msg.split('|')[0]
        pwd = client_msg.split('|')[1]
        print(user)
        print(pwd)
        cmd = "net user " + user + " " + pwd + " /add1"
        f = None
        try:
            bat = os.getcwd() + r"\script\cmd.bat"
            f = open(bat, 'w')
            f.write(cmd)
        except Exception as e:
            traceback.print_exc()
            raise e
        finally:
            if f:
                f.close()

        try:
            shell = os.getcwd() + r"\script\shell.vbs"
            # shell=False的时候cmd_list是一个列表，shell=True的时候cmd_list是一个字符串
            msg = subprocess.Popen(shell, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("[PID] %s: %s" % (msg.pid, cmd))
            msg.wait(timeout=3)
            stderr = str(msg.stderr.read().decode("gbk")).strip()
            stdout = str(msg.stdout.read().decode("gbk")).strip()
            if "" != stderr:
                print(stderr)
                conn.send("失败".encode('utf-8'))
            if stdout.find("失败") > -1:
                print(stdout)
                conn.send("失败".encode('utf-8'))
            if stdout.find("成功") > -1:
                print(stdout)
                conn.send("成功".encode('utf-8'))
        except Exception as e:
            conn.send("失败".encode('utf-8'))