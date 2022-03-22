#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
@Time : 2022/2/14 20:42
@Author : wxy
@contact: wxy18955007261@163.com
@file: SailingPackageClient.py
@desc: 打包脚本服务端,启用端口8002
上传至服务器/opt/test目录下
运行: nohup python2 SailingPackageServer.py >> package.log 2>&1 &
"""
import os
import socket

# sgg 重启cb和web
import struct
import threading
import time

port = 8002

def sggInstall():
    try:
        os.system("unzip /opt/test/sailingPackage.zip")
        # 删除cb的jar
        os.system("rm -rf /opt/sgg/engine/consolebus/jar/*")
        # 删除web的lib
        os.system("rm -rf /opt/sgg/web/apache-tomcat-8.5.32/webapps/sgg_ws/WEB-INF/lib/*")
        # 删除web的com文件夹
        os.system("rm -rf /opt/sgg/web/apache-tomcat-8.5.32/webapps/sgg_ws/WEB-INF/classes/com/*")
        os.system("rm -rf /opt/sgg/web/apache-tomcat-8.5.32/webapps/sgg_ws/WEB-INF/classes/META-INF/*")
        os.system("rm -rf /opt/sgg/web/apache-tomcat-8.5.32/webapps/sgg_ws/WEB-INF/classes/updateSql/*")
        os.system("rm -rf /opt/sgg/web/apache-tomcat-8.5.32/webapps/sgg_ws/WEB-INF/classes/basesql/*")
        # 移动文件
        os.system("mv -f /opt/test/tmp/packageSailing/sgg/consolebus/jar/*  /opt/sgg/engine/consolebus/jar/")
        os.system("mv -f /opt/test/tmp/packageSailing/sgg/consolebus/consolebus-1.0.jar  /opt/sgg/engine/consolebus")
        os.system("mv -f /opt/test/tmp/packageSailing/sgg/web/lib/*  /opt/sgg/web/apache-tomcat-8.5.32/webapps/sgg_ws/WEB-INF/lib/")
        os.system("mv -f /opt/test/tmp/packageSailing/sgg/web/classes/*  /opt/sgg/web/apache-tomcat-8.5.32/webapps/sgg_ws/WEB-INF/classes/")
        # 修改权限
        os.system("chmod -R 751 /opt/sgg/web/apache-tomcat-8.5.32/webapps/sgg_ws/WEB-INF/classes")
        os.system("chmod -R 751 /opt/sgg/web/apache-tomcat-8.5.32/webapps/sgg_ws/WEB-INF/lib")
        os.system("chmod -R 751 /opt/sgg/engine/consolebus/jar")
        os.system("chmod 751 /opt/sgg/engine/consolebus/consolebus-1.0.jar")
        # 重启
        os.system("/opt/sgg/bin/sgg-shutdwon-consolebus.sh")
        os.system("/opt/sgg/bin/sgg-start-consolebus.sh")
        os.system("/opt/sgg/web/apache-tomcat-8.5.32/bin/shutdown.sh")
        os.system("/opt/sgg/web/apache-tomcat-8.5.32/bin/startup.sh")
        # 删除临时文件
        os.system("rm -rf /opt/test/tmp")
        os.system("rm -rf /opt/test/sailingPackage.zip")
    except:
        print("安装异常")


def uggInstall():
    try:
        os.system("unzip /opt/test/sailingPackage.zip")
        # 删除cb的jar
        os.system("rm -rf /opt/sgg/engine/consolebus/jar/*")
        # 删除web的lib
        os.system("rm -rf /opt/sgg/web/apache-tomcat-8.5.32/webapps/sgg_ws/WEB-INF/lib/*")
        # 删除web的com文件夹
        os.system("rm -rf /opt/sgg/web/apache-tomcat-8.5.32/webapps/sgg_ws/WEB-INF/classes/com/*")
        os.system("rm -rf /opt/sgg/web/apache-tomcat-8.5.32/webapps/sgg_ws/WEB-INF/classes/META-INF/*")
        # 移动文件
        os.system("mv -f /opt/test/tmp/packageSailing/ugg/consolebus/jar/*  /opt/sgg/engine/consolebus/jar/")
        os.system("mv -f /opt/test/tmp/packageSailing/ugg/consolebus/consolebus-1.0.jar  /opt/sgg/engine/consolebus")
        os.system("mv -f /opt/test/tmp/packageSailing/ugg/web/lib/*  /opt/sgg/web/apache-tomcat-8.5.32/webapps/sgg_ws/WEB-INF/lib/")
        os.system("mv -f /opt/test/tmp/packageSailing/ugg/web/classes/*  /opt/sgg/web/apache-tomcat-8.5.32/webapps/sgg_ws/WEB-INF/classes/")
        # 修改权限
        os.system("chmod -R 751 /opt/sgg/web/apache-tomcat-8.5.32/webapps/sgg_ws/WEB-INF/classes")
        os.system("chmod -R 751 /opt/sgg/web/apache-tomcat-8.5.32/webapps/sgg_ws/WEB-INF/lib")
        os.system("chmod -R 751 /opt/sgg/engine/consolebus/jar")
        os.system("chmod 751 /opt/sgg/engine/consolebus/consolebus-1.0.jar")
        # 重启
        os.system("/opt/sgg/bin/sgg-shutdwon-consolebus.sh")
        os.system("/opt/sgg/bin/sgg-start-consolebus.sh")
        os.system("/opt/sgg/web/apache-tomcat-8.5.32/bin/shutdown.sh")
        os.system("/opt/sgg/web/apache-tomcat-8.5.32/bin/startup.sh")
        # 删除临时文件
        os.system("rm -rf /opt/test/tmp")
        os.system("rm -rf /opt/test/sailingPackage.zip")
    except:
        print("安装异常")


def dscg5Install():
    try:
        os.system("unzip /opt/test/sailingPackage.zip")
        # 删除cb的jar
        os.system("rm -rf /opt/dscg/engine/consolebus/jar/*")
        os.system("rm -f /opt/dscg/engine/consolebus/consolebus-*.jar")
        # 删除web的lib
        os.system("rm -rf /opt/dscg/web/container/webapps/dscg_ws/WEB-INF/lib/*")
        # 删除web的com文件夹
        os.system("rm -rf /opt/dscg/web/container/webapps/dscg_ws/WEB-INF/classes/com/*")
        os.system("rm -rf /opt/dscg/web/container/webapps/dscg_ws/WEB-INF/classes/META-INF/*")
        os.system("rm -rf /opt/dscg/web/container/webapps/dscg_ws/WEB-INF/classes/cn/*")
        os.system("rm -rf /opt/dscg/web/container/webapps/dscg_ws/WEB-INF/classes/sql/*")
        # 移动文件
        os.system("mv -f /opt/test/tmp/packageSailing/dscg5/consolebus/jar/*  /opt/dscg/engine/consolebus/jar/")
        os.system("mv -f /opt/test/tmp/packageSailing/dscg5/consolebus/consolebus-*.jar  /opt/dscg/engine/consolebus")
        os.system(
            "mv -f /opt/test/tmp/packageSailing/dscg5/web/lib/*  /opt/dscg/web/container/webapps/dscg_ws/WEB-INF/lib/")
        os.system(
            "mv -f /opt/test/tmp/packageSailing/dscg5/web/classes/*  /opt/dscg/web/container/webapps/dscg_ws/WEB-INF/classes/")
        # 修改权限
        os.system("chmod -R 751 /opt/dscg/web/container/webapps/dscg_ws/WEB-INF/classes")
        os.system("chmod -R 751 /opt/dscg/web/container/webapps/dscg_ws/WEB-INF/lib")
        os.system("chmod -R 751 /opt/dscg/engine/consolebus/jar")
        os.system("chmod 751 /opt/dscg/engine/consolebus/consolebus-*.jar")
        # 重启
        os.system("/opt/dscg/bin/dscg-down-consolebus.sh")
        os.system("/opt/dscg/bin/dscg-run-consolebus.sh")
        os.system("/opt/dscg/bin/dscg-down-tomcat.sh")
        os.system("/opt/dscg/bin/dscg-run-tomcat.sh")
        # 删除临时文件
        os.system("rm -rf /opt/test/tmp")
        os.system("rm -rf /opt/test/sailingPackage.zip")
    except:
        print("安装异常")

def dscg3Install():
    try:
        os.system("unzip /opt/test/sailingPackage.zip")
        # 删除cb的jar
        os.system("rm -rf /opt/dscg/engine/consolebus/jar/*")
        os.system("rm -f /opt/dscg/engine/consolebus/consolebus-*.jar")
        # 删除web的lib
        os.system("rm -rf /opt/dscg/web/container/webapps/dscg_ws/WEB-INF/lib/*")
        # 删除web的com文件夹
        os.system("rm -rf /opt/dscg/web/container/webapps/dscg_ws/WEB-INF/classes/com/*")
        os.system("rm -rf /opt/dscg/web/container/webapps/dscg_ws/WEB-INF/classes/META-INF/*")
        os.system("rm -rf /opt/dscg/web/container/webapps/dscg_ws/WEB-INF/classes/cn/*")
        os.system("rm -rf /opt/dscg/web/container/webapps/dscg_ws/WEB-INF/classes/sql/*")
        # 移动文件
        os.system("mv -f /opt/test/tmp/packageSailing/dscg3/consolebus/jar/*  /opt/dscg/engine/consolebus/jar/")
        os.system("mv -f /opt/test/tmp/packageSailing/dscg3/consolebus/consolebus-*.jar  /opt/dscg/engine/consolebus")
        os.system(
            "mv -f /opt/test/tmp/packageSailing/dscg3/web/lib/*  /opt/dscg/web/container/webapps/dscg_ws/WEB-INF/lib/")
        os.system(
            "mv -f /opt/test/tmp/packageSailing/dscg3/web/classes/*  /opt/dscg/web/container/webapps/dscg_ws/WEB-INF/classes/")
        # 修改权限
        os.system("chmod -R 751 /opt/dscg/web/container/webapps/dscg_ws/WEB-INF/classes")
        os.system("chmod -R 751 /opt/dscg/web/container/webapps/dscg_ws/WEB-INF/lib")
        os.system("chmod -R 751 /opt/dscg/engine/consolebus/jar")
        os.system("chmod 751 /opt/dscg/engine/consolebus/consolebus-*.jar")
        # 重启
        os.system("/opt/dscg/bin/dscg-down-consolebus.sh")
        os.system("/opt/dscg/bin/dscg-run-consolebus.sh")
        os.system("/opt/dscg/bin/dscg-down-tomcat.sh")
        os.system("/opt/dscg/bin/dscg-run-tomcat.sh")
        # 删除临时文件
        os.system("rm -rf /opt/test/tmp")
        os.system("rm -rf /opt/test/sailingPackage.zip")
    except:
        print("安装异常")

def handle():
    FILEINFO_SIZE = struct.calcsize('128sI')
    try:
        # 获取打包好的文件信息，并解包
        fhead = connect.recv(FILEINFO_SIZE)
        name, filesize = struct.unpack('128sI', fhead)
        name = str(name.decode())
        zipServerPath = "/opt/test/sailingPackage.zip"
        # 文件名必须去掉\00，否则会报错，此处为接收文件
        with open(zipServerPath, 'wb') as f:
            ressize = filesize
            while True:
                if ressize > 1024:
                    filedata = connect.recv(1024)
                else:
                    time.sleep(0.5)
                    filedata = connect.recv(ressize)
                    f.write(filedata)
                    break
                if not filedata:
                    break
                f.write(filedata)
                ressize = ressize - len(filedata)
                if ressize < 0:
                    break
        if name.find("sgg") != -1:
            print("部署sgg..")
            sggInstall()
        if name.find("ugg") != -1:
            print("部署ugg..")
            uggInstall()
        if name.find("dscg5") != -1:
            print("部署dscg5..")
            dscg5Install()
        if name.find("dscg3") != -1:
            print("部署dscg3..")
            dscg3Install()
        connect.shutdown(2)
        connect.close()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    #开端口
    os.system("iptables -I INPUT -p tcp  --dport 8002 -j ACCEPT")
    # 建立socket链接，并监听8002端口
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', port))
    sock.listen(100)
    print("监听端口8002,等待上传")
    while True:
        connect, address = sock.accept()
        print(str(address) + "连接")
        t = threading.Thread(target=handle)
        t.setDaemon(True)
        t.start()
