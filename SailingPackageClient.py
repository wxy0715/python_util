#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
@Time : 2022/2/14 20:42
@Author : wxy
@contact: wxy18955007261@163.com
@file: SailingPackageClient.py
@desc: 打包脚本客户端
"""
import os
import shutil
import socket
import struct
import subprocess
import time

# 打包完成命令 不能使用mvn clean install (lombok插件导致报错)
# -Dmaven.multiModuleProjectDirectory=packageClientFilePath 这个是特定格式,别的需要替换
cmd = 'F:\\env\\jdk1.8.0_201\\bin\java.exe -Dmaven.multiModuleProjectDirectory=packageClientFilePath -Dmaven.home=F:\\env\\apache-maven-3.5.3 -Dclassworlds.conf=F:\\env\\apache-maven-3.5.3\\bin\\m2.conf "-Dmaven.ext.class.path=F:\\dev\\IntelliJ IDEA 2021.2.2\\plugins\\maven\\lib\\maven-event-listener.jar" "-javaagent:F:\\dev\\IntelliJ IDEA 2021.2.2\\lib\\idea_rt.jar=59167:F:\\dev\\IntelliJ IDEA 2021.2.2\\bin" -Dfile.encoding=UTF-8 -classpath F:\\env\\apache-maven-3.5.3\\boot\\plexus-classworlds-2.5.2.jar org.codehaus.classworlds.Launcher -Didea.version=2021.2.2 -s F:\\env\\apache-maven-3.5.3\\conf\\settings.xml -Dmaven.repo.local=F:\\repository clean install'
# 打包项目列表
list = ["sgg", "ugg", "dscg-5.0", "dscg-3.0"]
# 打包的服务端临时路径
zipServerPath = "/opt/test/sailingPackage.zip"
# 打包的目的ip,优化为列表,多服务器同时打包
sggIp = ["172.20.54.229", "172.20.52.229"]
dscg5Ip = ["172.20.54.213", "172.20.54.214"]
dscg3Ip = ["172.20.54.213", "172.20.54.214"]
uggIp = ["172.20.52.96", "172.20.54.96"]
port = 8002
# sgg项目路径
sggPublicCommonPath = "A:\\project\\SGG\\public-conmon"
sggCommonPath = "A:\\project\\SGG\\SGG-Common"
sggCbPath = "A:\\project\\SGG\\SGG-ConsoleBus"
sggWebPath = "A:\\project\SGG\\SGG-WebConsoleBackend"

# ugg项目路径
uggCbPath = "A:\\project\\SGG\\SGG-OneWay-ConsoleBus"
uggWebPath = "A:\\project\SGG\\SGG-OneWay-WebConsoleBackend"

# dscg项目路径
dscgCommonPath = "A:\\project\\DSCG\\DSCG-Common"
dscgCbPath = "A:\\project\\DSCG\\DSCG-ConsoleBus"
dscgWebPath = "A:\\project\\DSCG\\DSCG-WebConsoleBackend"

# 一次性允许传输的最大字节数
max_packet_size = 8192

class sgg:
    def __init__(self):
        self.zipPath = "C:\\tmp\\packageSailing\\sgg.zip"
        os.chdir(sggPublicCommonPath)
        ps = subprocess.Popen('git pull')
        ps.wait()
        os.chdir(sggCommonPath)
        ps = subprocess.Popen('git pull')
        ps.wait()
        os.chdir(sggCbPath)
        ps = subprocess.Popen('git pull')
        ps.wait()
        os.chdir(sggWebPath)
        ps = subprocess.Popen('git pull')
        ps.wait()

    def packagePublicCommon(self):
        os.chdir(sggPublicCommonPath)
        packageCmd = cmd.replace("packageClientFilePath", sggPublicCommonPath)
        ps = subprocess.Popen(packageCmd)
        ps.wait()
        pass

    def packageCommon(self):
        os.chdir(sggCommonPath)
        packageCmd = cmd.replace("packageClientFilePath", sggCommonPath)
        ps = subprocess.Popen(packageCmd)
        ps.wait()
        pass

    def packageCb(self):
        os.chdir(sggCbPath)
        packageCmd = cmd.replace("packageClientFilePath", sggCbPath)
        ps = subprocess.Popen(packageCmd)
        ps.wait()
        pass

    def packageWeb(self):
        os.chdir(sggWebPath)
        packageCmd = cmd.replace("packageClientFilePath", sggWebPath)
        ps = subprocess.Popen(packageCmd)
        ps.wait()
        pass

    def removeYml(self):
        os.chdir(sggWebPath)
        os.remove(sggWebPath+"\\target\\sgg_ws\\WEB-INF\\classes\\application.yml")
        pass

    def moveFolder(self):
        base_dir = "C:\\tmp\\packageSailing"
        try:
            shutil.rmtree(base_dir+"\\sgg")
        except:
            print("")
        shutil.copytree(sggCbPath+"\\target\\consolebus\\jar", base_dir+"\\sgg\\consolebus\\jar", symlinks=False, ignore=None, copy_function=shutil.copy, ignore_dangling_symlinks=False)
        shutil.copy(sggCbPath+"\\target\\consolebus\\consolebus-1.0.jar", base_dir+"\\sgg\\consolebus")
        shutil.copytree(sggWebPath+"\\target\\sgg_ws\\WEB-INF", base_dir+"\\sgg\\web", symlinks=False, ignore=None, copy_function=shutil.copy, ignore_dangling_symlinks=False)
        shutil.make_archive(base_dir+"\\sgg", "zip", base_dir=base_dir+"\\sgg")

    def client(self, ip=None):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(3)
            client.connect((ip, port))
            fhead = struct.pack('128sI', "sgg".encode(), os.stat(self.zipPath).st_size)
            client.send(fhead)
            # 传送文件
            with open(self.zipPath, 'rb') as f:
                while True:
                    filedata = f.read(1024)
                    if not filedata:
                        break
                    client.send(filedata)
            client.close()
            print("上传sgg包完成")
        except:
            print("连接异常")

class ugg:
    def __init__(self):
        self.zipPath = "C:\\tmp\\packageSailing\\ugg.zip"
        os.chdir(sggPublicCommonPath)
        ps = subprocess.Popen('git pull')
        ps.wait()
        os.chdir(sggCommonPath)
        ps = subprocess.Popen('git pull')
        ps.wait()
        os.chdir(uggCbPath)
        ps = subprocess.Popen('git pull')
        ps.wait()
        os.chdir(uggWebPath)
        ps = subprocess.Popen('git pull')
        ps.wait()

    def packagePublicCommon(self):
        os.chdir(sggPublicCommonPath)
        packageCmd = cmd.replace("packageClientFilePath", sggPublicCommonPath)
        ps = subprocess.Popen(packageCmd)
        ps.wait()
        pass

    def packageCommon(self):
        os.chdir(sggCommonPath)
        packageCmd = cmd.replace("packageClientFilePath", sggCommonPath)
        ps = subprocess.Popen(packageCmd)
        ps.wait()
        pass

    def packageCb(self):
        os.chdir(uggCbPath)
        packageCmd = cmd.replace("packageClientFilePath", uggCbPath)
        ps = subprocess.Popen(packageCmd)
        ps.wait()
        pass

    def packageWeb(self):
        os.chdir(uggWebPath)
        packageCmd = cmd.replace("packageClientFilePath", uggWebPath)
        ps = subprocess.Popen(packageCmd)
        ps.wait()
        pass

    # delete web yml
    def removeYml(self):
        os.chdir(uggWebPath)
        os.remove(uggWebPath+"\\target\\sgg_ws\\WEB-INF\\classes\\application.yml")
        pass

    def moveFolder(self):
        base_dir = "C:\\tmp\\packageSailing"
        try:
            shutil.rmtree(base_dir+"\\ugg")
        except:
            print("")
        shutil.copytree(uggCbPath+"\\target\\consolebus\\jar", base_dir+"\\ugg\\consolebus\\jar", symlinks=False, ignore=None, copy_function=shutil.copy, ignore_dangling_symlinks=False)
        shutil.copy(uggCbPath+"\\target\\consolebus\\consolebus-1.0.jar", base_dir+"\\ugg\\consolebus")
        shutil.copytree(uggWebPath+"\\target\\sgg_ws\\WEB-INF", base_dir+"\\ugg\\web", symlinks=False, ignore=None, copy_function=shutil.copy, ignore_dangling_symlinks=False)
        shutil.make_archive(base_dir+"\\ugg", "zip", base_dir=base_dir+"\\ugg")

    def client(self, ip=None):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(3)
            client.connect((ip, port))
            fhead = struct.pack('128sI', 'ugg'.encode('utf-8'), os.stat(self.zipPath).st_size)
            client.send(fhead)
            # 传送文件
            with open(self.zipPath, 'rb') as f:
                while True:
                    filedata = f.read(1024)
                    if not filedata:
                        break
                    client.send(filedata)
            client.close()
            print("上传ugg包完成")
        except:
            print("连接异常")

class dscg5:
    def __init__(self):
        self.zipPath = "C:\\tmp\\packageSailing\\dscg5.zip"
        os.chdir(dscgCommonPath)
        ps = subprocess.Popen('git checkout dscg-5.0')
        ps.wait()
        ps = subprocess.Popen('git pull')
        ps.wait()
        os.chdir(dscgCbPath)
        ps = subprocess.Popen('git checkout dscg-5.0')
        ps.wait()
        ps = subprocess.Popen('git pull')
        ps.wait()
        os.chdir(dscgWebPath)
        ps = subprocess.Popen('git checkout dscg-5.0')
        ps.wait()
        ps = subprocess.Popen('git pull')
        ps.wait()

    def packageCommon(self):
        os.chdir(dscgCommonPath)
        packageCmd = cmd.replace("packageClientFilePath", dscgCommonPath)
        ps = subprocess.Popen(packageCmd)
        ps.wait()
        pass

    def packageCb(self):
        os.chdir(dscgCbPath)
        packageCmd = cmd.replace("packageClientFilePath", dscgCbPath)
        ps = subprocess.Popen(packageCmd)
        ps.wait()
        pass

    def packageWeb(self):
        os.chdir(dscgWebPath)
        packageCmd = cmd.replace("packageClientFilePath", dscgWebPath)
        ps = subprocess.Popen(packageCmd)
        ps.wait()
        pass

    # delete web yml
    def removeYml(self):
        os.chdir(dscgWebPath)
        os.remove(dscgWebPath+"\\target\\dscg_ws\\WEB-INF\\classes\\application.yml")
        pass

    def moveFolder(self):
        base_dir = "C:\\tmp\\packageSailing"
        try:
            shutil.rmtree(base_dir+"\\dscg5")
        except:
            print("")
        shutil.copytree(dscgCbPath+"\\target\\consolebus\\jar", base_dir+"\\dscg5\\consolebus\\jar", symlinks=False, ignore=None, copy_function=shutil.copy, ignore_dangling_symlinks=False)
        result = os.listdir(dscgCbPath+"\\target\\consolebus")
        for cbJar in result:
            if cbJar.find(".jar") != -1:
                shutil.copy(dscgCbPath + "\\target\\consolebus\\"+cbJar, base_dir + "\\dscg5\\consolebus")
        shutil.copytree(dscgWebPath+"\\target\\dscg_ws\\WEB-INF", base_dir+"\\dscg5\\web", symlinks=False, ignore=None, copy_function=shutil.copy, ignore_dangling_symlinks=False)
        shutil.make_archive(base_dir+"\\dscg5", "zip", base_dir=base_dir+"\\dscg5")

    def client(self, ip=None):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(3)
            client.connect((ip, port))
            fhead = struct.pack('128sI', "dscg5".encode('utf-8'), os.stat(self.zipPath).st_size)
            client.send(fhead)
            # 传送文件
            with open(self.zipPath, 'rb') as f:
                while True:
                    filedata = f.read(1024)
                    if not filedata:
                        break
                    client.send(filedata)
            client.close()
            print("上传dscg5包完成")
        except:
            print("连接异常")

class dscg3:
    def __init__(self):
        self.zipPath = "C:\\tmp\\packageSailing\\dscg3.zip"
        os.chdir(dscgCommonPath)
        ps = subprocess.Popen('git checkout dscg-3.0')
        ps.wait()
        ps = subprocess.Popen('git pull')
        ps.wait()
        os.chdir(dscgCbPath)
        ps = subprocess.Popen('git checkout dscg-3.0')
        ps.wait()
        ps = subprocess.Popen('git pull')
        ps.wait()
        os.chdir(dscgWebPath)
        ps = subprocess.Popen('git checkout dscg-3.0')
        ps.wait()
        ps = subprocess.Popen('git pull')
        ps.wait()

    def packageCommon(self):
        os.chdir(dscgCommonPath)
        packageCmd = cmd.replace("packageClientFilePath", dscgCommonPath)
        ps = subprocess.Popen(packageCmd)
        ps.wait()
        pass

    def packageCb(self):
        os.chdir(dscgCbPath)
        packageCmd = cmd.replace("packageClientFilePath", dscgCbPath)
        ps = subprocess.Popen(packageCmd)
        ps.wait()
        pass

    def packageWeb(self):
        os.chdir(dscgWebPath)
        packageCmd = cmd.replace("packageClientFilePath", dscgWebPath)
        ps = subprocess.Popen(packageCmd)
        ps.wait()
        pass

    # delete web yml
    def removeYml(self):
        os.chdir(dscgWebPath)
        os.remove(dscgWebPath+"\\target\\dscg_ws\\WEB-INF\\classes\\application.yml")
        pass

    def moveFolder(self):
        base_dir = "C:\\tmp\\packageSailing"
        try:
            shutil.rmtree(base_dir+"\\dscg3")
        except:
            print("")
        shutil.copytree(dscgCbPath+"\\target\\consolebus\\jar", base_dir+"\\dscg3\\consolebus\\jar", symlinks=False, ignore=None, copy_function=shutil.copy, ignore_dangling_symlinks=False)
        result = os.listdir(dscgCbPath+"\\target\\consolebus")
        for cbJar in result:
            if cbJar.find(".jar") != -1:
                shutil.copy(dscgCbPath + "\\target\\consolebus\\"+cbJar, base_dir + "\\dscg3\\consolebus")
        shutil.copytree(dscgWebPath+"\\target\\dscg_ws\\WEB-INF", base_dir+"\\dscg3\\web", symlinks=False, ignore=None, copy_function=shutil.copy, ignore_dangling_symlinks=False)
        shutil.make_archive(base_dir+"\\dscg3", "zip", base_dir=base_dir+"\\dscg3")

    def client(self, ip=None):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(3)
            client.connect((ip, port))
            fhead = struct.pack('128sI', "dscg3".encode('utf-8'), os.stat(self.zipPath).st_size)
            client.send(fhead)
            # 传送文件
            with open(self.zipPath, 'rb') as f:
                while True:
                    filedata = f.read(1024)
                    if not filedata:
                        break
                    client.send(filedata)
            client.close()
            print("上传dscg3包完成")
        except:
            print("连接异常")


if __name__ == '__main__':
    selectName = input("请选择打包的项目:"+','.join(list)+"逗号分割\n")
    if str(selectName).find('sgg') != -1:
        print("打包sgg开始...")
        sggClass = sgg()
        sggClass.packagePublicCommon()
        sggClass.packageCommon()
        sggClass.packageCb()
        sggClass.packageWeb()
        sggClass.removeYml()
        sggClass.moveFolder()
        print("打包sgg完成...开始建立socket")
        for sggip in sggIp:
            sggClass.client(ip=sggip)

    if str(selectName).find("ugg") != -1:
        print("打包ugg开始...")
        uggClass = ugg()
        uggClass.packagePublicCommon()
        uggClass.packageCommon()
        uggClass.packageCb()
        uggClass.packageWeb()
        uggClass.removeYml()
        uggClass.moveFolder()
        print("打包ugg完成...开始建立socket")
        for uggip in uggIp:
            uggClass.client(ip=uggip)

    if str(selectName).find("dscg-5.0") != -1:
        print("打包dscg-5.0开始...")
        dscg5Class = dscg5()
        time.sleep(3)
        dscg5Class.packageCommon()
        dscg5Class.packageCb()
        dscg5Class.packageWeb()
        dscg5Class.removeYml()
        dscg5Class.moveFolder()
        print("打包dscg-5.0完成...开始建立socket")
        for dscg5ip in dscg5Ip:
            dscg5Class.client(ip=dscg5ip)

    if str(selectName).find("dscg-3.0") != -1:
        print("打包dscg-3.0开始...")
        dscg3Class = dscg3()
        time.sleep(3)
        dscg3Class.packageCommon()
        dscg3Class.packageCb()
        dscg3Class.packageWeb()
        dscg3Class.removeYml()
        dscg3Class.moveFolder()
        print("打包dscg-3.0完成...开始建立socket")
        for dscg3ip in dscg3Ip:
            dscg3Class.client(ip=dscg3ip)