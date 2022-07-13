#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
@Time : 2022/7/12 10:42
@Author : wxy
@contact: wxy18955007261@163.com
@file: HaitianPackage.py
@desc: 打包脚本
"""
import os
import subprocess

# 打包完成命令 不能使用mvn clean install (lombok插件导致报错)\\
# -Dmaven.multiModuleProjectDirectory=packageClientFilePath 这个是特定格式,别的需要替换
import threading

import paramiko
from paramiko import SSHClient

prodIp = '192.168.1.80'
devIp = '192.168.2.10'
cmd = '"D:\\Program Files\\jdk1.8.0_201\\bin\\java.exe" -Dmaven.multiModuleProjectDirectory=D:\\HaiTian\\预算中台\\budgetmiddleoffice\\ServiceSite "-Dmaven.home=D:\\Program Files\\apache-maven-3.5.4" "-Dclassworlds.conf=D:\\Program Files\\apache-maven-3.5.4\\bin\\m2.conf" "-Dmaven.ext.class.path=D:\\Program Files\\idea\\IntelliJ IDEA 2019.3.3\\plugins\\maven\\lib\\maven-event-listener.jar" "-javaagent:D:\\Program Files\\idea\\IntelliJ IDEA 2019.3.3\\lib\\idea_rt.jar=50834:D:\\Program Files\\idea\\IntelliJ IDEA 2019.3.3\\bin" -Dfile.encoding=UTF-8 -classpath "D:\\Program Files\\apache-maven-3.5.4\\boot\\plexus-classworlds-2.5.2.jar" org.codehaus.classworlds.Launcher -Didea.version2019.3.3 -s "D:\\Program Files\\apache-maven-3.5.4\\conf\\settings.xml" "-Dmaven.repo.local=D:\\Program Files\\maven\\apache-maven-3.5.4\\repository" clean package docker:build'
# 打包项目列表
packageList = ["budgetmiddleoffice", "budgetmaster", "projectplan_gzy", "projectplan_origin", "adjust"]
packageIp = prodIp
dockerIp = "47.110.127.118"
# 指标中台
budgetmiddleofficePath = "D:\\HaiTian\\预算中台\\budgetmiddleoffice\\ServiceSite"
# 指标管理
budgetmasterPath = "D:\\HaiTian\\全面预算指标\\budgetmaster\\ServiceSite"
# 预算编制-广中医
projectplan_gzyPath = "D:\\HaiTian\\广州中医药\\projectplan_gzy\\ServiceSite"
# 预算编制
projectplanPath = "D:\\HaiTian\\预算编制\\projectplan\\ServiceSite"
# 预算调整
adjustPath = "D:\\HaiTian\\全面预算调整\\seasky_adjust\\ServiceSite"


class budgetmiddleoffice:
    def __init__(self):
        os.chdir(budgetmiddleofficePath)
        ps = subprocess.Popen('git checkout develop')
        ps.wait()
        ps = subprocess.Popen('git pull')
        ps.wait()

    def package(self):
        os.chdir(budgetmiddleofficePath)
        packageCmd = cmd.replace("packageClientFilePath", budgetmiddleofficePath)
        msg = subprocess.Popen(packageCmd, shell=True, stderr=subprocess.STDOUT, encoding='utf-8')
        msg.wait()
        pass

    # 登录服务器拉取镜像
    def pull(self):
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 建立连接
        ssh.connect(packageIp, username="root", port=22, password="Seasky123456")
        # 使用这个连接执行命令
        pullCmd = "docker pull demo.seaskysh.com/seaskysh/budgetmiddleoffice:" + self.getImage()
        print("拉取镜像:" + pullCmd)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        stdin, stdout, stderr = ssh.exec_command(pullCmd)
        res, err = stdout.read(), stderr.read()
        if res:
            print(res.decode().strip())
        else:
            print(err)
            exit(0)
        stdin, stdout, stderr = ssh.exec_command("docker images")
        print(stdout.read().decode().strip())
        # 关闭连接
        ssh.close()


    # 登录服务器推送镜像
    def push(self):
        ssh = SSHClient()
        # 允许连接不在know_hosts文件中的主机
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 建立连接
        ssh.connect(dockerIp, username="root", port=22, password="seaskysh@dev2019")
        # 使用这个连接执行命令
        pushCmd = "docker push demo.seaskysh.com/seaskysh/budgetmiddleoffice:" + self.getImage()
        print("推送镜像:" + pushCmd)
        stdin, stdout, stderr = ssh.exec_command(pushCmd)
        res, err = stdout.read(), stderr.read()
        if res:
            print(res.decode().strip())
        else:
            print(err)
            exit(0)
        # 关闭连接
        ssh.close()

    def getImage(self):
        os.chdir(budgetmiddleofficePath)
        version = ''
        with open("pom.xml", encoding='UTF-8') as lines:
            for line in lines:
                if line.find('<version>') > 0:
                    version = line.strip().replace("<version>", "").replace("</version>", "")
                    print("版本号为:"+version)
                    return version
        return version


class budgetmaster:
        def __init__(self):
            os.chdir(budgetmasterPath)
            ps = subprocess.Popen('git checkout develop')
            ps.wait()
            ps = subprocess.Popen('git pull')
            ps.wait()

        def package(self):
            os.chdir(budgetmasterPath)
            packageCmd = cmd.replace("packageClientFilePath", budgetmasterPath)
            msg = subprocess.Popen(packageCmd, shell=True, stderr=subprocess.STDOUT, encoding='utf-8')
            msg.wait()
            pass

        # 登录服务器拉取镜像
        def pull(self):
            ssh = SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # 建立连接
            ssh.connect(packageIp, username="root", port=22, password="Seasky123456")
            # 使用这个连接执行命令
            pullCmd = "docker pull demo.seaskysh.com/seaskysh/budget-quota:" + self.getImage()
            print("拉取镜像:" + pullCmd)
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            stdin, stdout, stderr = ssh.exec_command(pullCmd)
            res, err = stdout.read(), stderr.read()
            if res:
                print(res.decode().strip())
            else:
                print(err)
                exit(0)

            stdin, stdout, stderr = ssh.exec_command("docker images")
            print(stdout.read().decode().strip())
            # 关闭连接
            ssh.close()

        # 登录服务器推送镜像
        def push(self):
            ssh = SSHClient()
            # 允许连接不在know_hosts文件中的主机
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # 建立连接
            ssh.connect(dockerIp, username="root", port=22, password="seaskysh@dev2019")
            # 使用这个连接执行命令
            pushCmd = "docker push demo.seaskysh.com/seaskysh/budget-quota:" + self.getImage()
            print("推送镜像:" + pushCmd)
            stdin, stdout, stderr = ssh.exec_command(pushCmd)
            res, err = stdout.read(), stderr.read()
            if res:
                print(res.decode().strip())
            else:
                print(err)
                exit(0)
            # 关闭连接
            ssh.close()

        def getImage(self):
            os.chdir(budgetmasterPath)
            version = ''
            with open("pom.xml", encoding='UTF-8') as lines:
                for line in lines:
                    if line.find('<version>') > 0:
                        version = line.strip().replace("<version>", "").replace("</version>", "")
                        print("版本号为:" + version)
                        return version
            return version


class projectplan_gzy:
            def __init__(self):
                os.chdir(projectplan_gzyPath)
                ps = subprocess.Popen('git checkout develop')
                ps.wait()
                ps = subprocess.Popen('git pull')
                ps.wait()

            def package(self):
                os.chdir(projectplan_gzyPath)
                packageCmd = cmd.replace("packageClientFilePath", projectplan_gzyPath)
                msg = subprocess.Popen(packageCmd, shell=True, stderr=subprocess.STDOUT, encoding='utf-8')
                msg.wait()
                pass

            # 登录服务器拉取镜像
            def pull(self):
                ssh = SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                # 建立连接
                ssh.connect(packageIp, username="root", port=22, password="Seasky123456")
                # 使用这个连接执行命令
                pullCmd = "docker pull demo.seaskysh.com/seaskysh/projectplan-gzy:" + self.getImage()
                print("拉取镜像:" + pullCmd)
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                stdin, stdout, stderr = ssh.exec_command(pullCmd)
                res, err = stdout.read(), stderr.read()
                if res:
                    print(res.decode().strip())
                else:
                    print(err)
                    exit(0)

                stdin, stdout, stderr = ssh.exec_command("docker images")
                print(stdout.read().decode().strip())
                # 关闭连接
                ssh.close()

            # 登录服务器推送镜像
            def push(self):
                ssh = SSHClient()
                # 允许连接不在know_hosts文件中的主机
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                # 建立连接
                ssh.connect(dockerIp, username="root", port=22, password="seaskysh@dev2019")
                # 使用这个连接执行命令
                pushCmd = "docker push demo.seaskysh.com/seaskysh/projectplan-gzy:" + self.getImage()
                print("推送镜像:" + pushCmd)
                stdin, stdout, stderr = ssh.exec_command(pushCmd)
                res, err = stdout.read(), stderr.read()
                if res:
                    print(res.decode().strip())
                else:
                    print(err)
                    exit(0)
                # 关闭连接
                ssh.close()

            def getImage(self):
                os.chdir(projectplan_gzyPath)
                version = ''
                with open("pom.xml", encoding='UTF-8') as lines:
                    for line in lines:
                        if line.find('<version>') > 0:
                            version = line.strip().replace("<version>", "").replace("</version>", "")
                            print("版本号为:" + version)
                            return version
                return version


class projectplan:
    def __init__(self):
        os.chdir(projectplanPath)
        ps = subprocess.Popen('git checkout develop')
        ps.wait()
        ps = subprocess.Popen('git pull')
        ps.wait()

    def package(self):
        os.chdir(projectplanPath)
        packageCmd = cmd.replace("packageClientFilePath", projectplanPath)
        msg = subprocess.Popen(packageCmd, shell=True, stderr=subprocess.STDOUT, encoding='utf-8')
        msg.wait()
        pass

    # 登录服务器拉取镜像
    def pull(self):
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 建立连接
        ssh.connect(packageIp, username="root", port=22, password="Seasky123456")
        # 使用这个连接执行命令
        pullCmd = "docker pull demo.seaskysh.com/seaskysh/projectplan:" + self.getImage()
        print("拉取镜像:" + pullCmd)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        stdin, stdout, stderr = ssh.exec_command(pullCmd)
        res, err = stdout.read(), stderr.read()
        if res:
            print(res.decode().strip())
        else:
            print(err)
            exit(0)

        stdin, stdout, stderr = ssh.exec_command("docker images")
        print(stdout.read().decode().strip())
        # 关闭连接
        ssh.close()

    # 登录服务器推送镜像
    def push(self):
        ssh = SSHClient()
        # 允许连接不在know_hosts文件中的主机
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 建立连接
        ssh.connect(dockerIp, username="root", port=22, password="seaskysh@dev2019")
        # 使用这个连接执行命令
        pushCmd = "docker push demo.seaskysh.com/seaskysh/projectplan:" + self.getImage()
        print("推送镜像:" + pushCmd)
        stdin, stdout, stderr = ssh.exec_command(pushCmd)
        res, err = stdout.read(), stderr.read()
        if res:
            print(res.decode().strip())
        else:
            print(err)
            exit(0)
        # 关闭连接
        ssh.close()

    def getImage(self):
        os.chdir(projectplanPath)
        version = ''
        with open("pom.xml", encoding='UTF-8') as lines:
            for line in lines:
                if line.find('<version>') > 0:
                    version = line.strip().replace("<version>", "").replace("</version>", "")
                    print("版本号为:" + version)
                    return version
        return version


class adjust:
    def __init__(self):
        os.chdir(adjustPath)
        ps = subprocess.Popen('git checkout develop')
        ps.wait()
        ps = subprocess.Popen('git pull')
        ps.wait()

    def package(self):
        os.chdir(adjustPath)
        packageCmd = cmd.replace("packageClientFilePath", adjustPath)
        msg = subprocess.Popen(packageCmd, shell=True, stderr=subprocess.STDOUT, encoding='utf-8')
        msg.wait()
        pass

    # 登录服务器拉取镜像
    def pull(self):
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 建立连接
        ssh.connect(packageIp, username="root", port=22, password="Seasky123456")
        # 使用这个连接执行命令
        pullCmd = "docker pull demo.seaskysh.com/seaskysh/adjustproject:" + self.getImage()
        print("拉取镜像:" + pullCmd)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        stdin, stdout, stderr = ssh.exec_command(pullCmd)
        res, err = stdout.read(), stderr.read()
        if res:
            print(res.decode().strip())
        else:
            print(err)
            exit(0)

        stdin, stdout, stderr = ssh.exec_command("docker images")
        print(stdout.read().decode().strip())
        # 关闭连接
        ssh.close()

    # 登录服务器推送镜像
    def push(self):
        ssh = SSHClient()
        # 允许连接不在know_hosts文件中的主机
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 建立连接
        ssh.connect(dockerIp, username="root", port=22, password="seaskysh@dev2019")
        # 使用这个连接执行命令
        pushCmd = "docker push demo.seaskysh.com/seaskysh/adjustproject:" + self.getImage()
        print("推送镜像:" + pushCmd)
        stdin, stdout, stderr = ssh.exec_command(pushCmd)
        res, err = stdout.read(), stderr.read()
        if res:
            print(res.decode().strip())
        else:
            print(err)
            exit(0)
        # 关闭连接
        ssh.close()

    def getImage(self):
        os.chdir(adjustPath)
        version = ''
        with open("pom.xml", encoding='UTF-8') as lines:
            for line in lines:
                if line.find('<version>') > 0:
                    version = line.strip().replace("<version>", "").replace("</version>", "")
                    print("版本号为:" + version)
                    return version
        return version


if __name__ == '__main__':
    selectName = input("请选择打包的项目:" + ','.join(packageList) + "逗号分割\n")
    if str(selectName).find('budgetmaster') != -1:
        print("打包全面预算指标管理系统开始...")
        budgetmasterClass = budgetmaster()
        budgetmasterClass.package()
        budgetmasterClass.push()
        budgetmasterClass.pull()
        print("更新全面预算指标管理系统完成...")

    if str(selectName).find('budgetmiddleoffice') != -1:
        print("打包全面预算指标中台开始...")
        budgetmiddleofficeClass = budgetmiddleoffice()
        budgetmiddleofficeClass.package()
        budgetmiddleofficeClass.push()
        budgetmiddleofficeClass.pull()
        print("更新全面预算指标中台完成...")

    if str(selectName).find('projectplan_gzy') != -1:
        print("打包预算编制-广中医开始...")
        projectplan_gzyClass = projectplan_gzy()
        projectplan_gzyClass.package()
        projectplan_gzyClass.push()
        projectplan_gzyClass.pull()
        print("更新预算编制-广中医完成...")

    if str(selectName).find('projectplan_origin') != -1:
        print("打包预算编制开始...")
        projectplanClass = projectplan()
        projectplanClass.package()
        projectplanClass.push()
        projectplanClass.pull()
        print("更新预算编制完成...")

    if str(selectName).find('adjust') != -1:
        print("打包预算调整开始...")
        adjustClass = adjust()
        adjustClass.package()
        adjustClass.push()
        adjustClass.pull()
        print("更新预算调整完成...")