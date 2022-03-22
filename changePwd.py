#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
@Time : 2021/10/28 9:31
@Author : wxy
@contact: wxy18955007261@163.com
@file: changePwd.py
@desc:  设备改密 1windows(rdp) 2linux 3unix 4huawei 5aix 6cisco 7h3c 8uos 9kylin
ssh telnet vnc ftp sftp x11
"""
import re
import socket
import string
import sys
import time
from random import choice
import paramiko

# byte转16进制字符串 02 不足两位前面补0,X十六进制
def bytesToHexString(bs):
    return ''.join(['%02X' % b for b in bs])


# ascii_letters是生成所有字母，从a-z和A-Z,digits是生成所有数字0-9
def GenPassword(length=8, chars=string.ascii_letters+string.digits+'!@#%&*+='):
    pwd = ''.join([choice(string.ascii_lowercase) for _ in range(1)]) \
          + ''.join([choice(string.ascii_uppercase) for _ in range(1)]) \
          + ''.join([choice(string.digits) for _ in range(1)]) \
          + ''.join([choice('!@#%&*+=') for _ in range(1)])
    return pwd+''.join([choice(chars) for _ in range(length - len(pwd))])


ip = "49.232.142.65"
port = 3389
allow_root = 0
super_account = "root"
super_password = "qqwang0715.."
username = "test"
old_password = "wxy0715@@"
new_password = ""
device_type = 2
pwd_length = 8

successful = '成功'
en_successful = 'success'
failed = '失败'
en_fail = 'Error'
en_fail_hua3c = 'Cannot change password'
en_fail_hua3c1 = 'Permission denied'


def changeSSH(Ip, port, allow_root, super_account, super_password, user, old_password, new_password):
    # 建立一个sshclient对象
    global out
    ssh = paramiko.SSHClient()
    # 允许将信任的主机自动加入到host_allow 列表，此方法必须放在connect方法的前面
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        if allow_root == 1 and not super_account is None and not super_password is None:
            print(device_type, Ip, port, super_account, super_password, user, old_password, new_password)
            ssh.connect(hostname=Ip, port=port, username=super_account, password=super_password, timeout=5)
            if device_type == 4:
                ssh_shell = ssh.invoke_shell()
                out = ssh_shell.recv(1024)
                print(out)
                print(out.decode())
                while not re.search('<.*?>', str(out, 'utf-8')):
                    if '[Y/N]' in str(out, 'utf-8'):
                        # 强制改密
                        super_new_password = GenPassword(pwd_length)
                        print('Y/N')
                        ssh_shell.sendall('Y\n')
                        ssh_shell.sendall(super_password+'\n'+super_new_password+'\n'+super_new_password+'\n')
                        time.sleep(float(1))
                        out, err = ssh_shell.recv(1024)
                        print(out)
                        if successful in str(out,'utf-8') or en_successful in str(out,'utf-8') or successful in str(err,'utf-8') or en_successful in str(err,'utf-8') or en_fail not in str(out,'utf-8'):
                            print("改密成功!")
                    else:
                        ssh_shell.sendall('\n')
                        time.sleep(float(1))
                        out = ssh_shell.recv(1024);
                        print(out)

                res = ssh_shell.sendall('system-view\n')
                time.sleep(float(1))
                out = ssh_shell.recv(1024);
                res = ssh_shell.sendall('aaa\n')
                time.sleep(float(1))
                out = ssh_shell.recv(1024);
                res = ssh_shell.sendall('local-user '+user+' password irreversible-cipher '+new_password+'\n')
                time.sleep(float(1))
                out = ssh_shell.recv(1024);
                err = out
            elif device_type == 7:
                #华3交换机
                ssh_shell = ssh.invoke_shell()
                out = ssh_shell.recv(1024)
                print(out)
                while not re.search('<.*?>', str(out,'utf-8')):
                    if 'change your password' in str(out,'utf-8'):
                        super_new_password = GenPassword(pwd_length)
                        print('Y/N')
                        time.sleep(float(1))
                        ssh_shell.sendall(super_password+'\n')
                        time.sleep(float(1))
                        out = ssh_shell.recv(1024);
                        print(out)
                        ssh_shell.sendall(super_new_password+'\n')
                        time.sleep(float(1))
                        out = ssh_shell.recv(1024);
                        print(out)
                        ssh_shell.sendall(super_new_password+'\n')
                        time.sleep(float(1))
                        out = ssh_shell.recv(1024);

                        print('------------------------------')
                        print(out)
                        print('Updating user information' in str(out,'utf-8'))
                        if 'Updating user information' in str(out,'utf-8'):
                            print("改密成功!")
                    else:
                        ssh_shell.sendall('\n')
                    time.sleep(float(1))
                    out = ssh_shell.recv(1024);
                    print(out)
                res = ssh_shell.sendall('sys\n')
                time.sleep(float(1))
                out = ssh_shell.recv(1024);
                print(out)
                res = ssh_shell.sendall('local-user '+user+'\n')
                time.sleep(float(1))
                out = ssh_shell.recv(1024);
                print(out)
                res = ssh_shell.sendall('password simple '+new_password+'\n')
                time.sleep(float(1))
                out = ssh_shell.recv(1024);
                print(out)
                res = ssh_shell.sendall('save\n')
                time.sleep(float(1))
                out1 = ssh_shell.recv(1024);
                print(out1)
                res = ssh_shell.sendall('Y\n')
                time.sleep(float(1))
                out1 = ssh_shell.recv(1024);
                print(out1)
                res = ssh_shell.sendall('\n')
                time.sleep(float(1))
                out1 = ssh_shell.recv(1024);
                print(out1)
                res = ssh_shell.sendall('Y\n')
                time.sleep(float(1))
                out1 = ssh_shell.recv(1024);
                print(out1)
                res = ssh_shell.sendall('\n')
                time.sleep(float(1))
                out1 = ssh_shell.recv(1024);
                print(out1)
                err = out
        else:
            print(device_type, Ip, port, user, old_password, new_password)
            ssh.connect(hostname=Ip, port=port, username=user, password=old_password, timeout=5)
            if device_type == 4:
                # 华为
                is_change = False
                ssh_shell = ssh.invoke_shell()
                out = ssh_shell.recv(1024)
                time.sleep(float(1))
                while not re.search('<.*?>', str(out, 'utf-8')):
                    #强制改密
                    print(out)
                    if '[Y/N]' in str(out,'utf-8'):
                        print('Y/N')
                        ssh_shell.sendall('Y\n')
                        ssh_shell.sendall(old_password+'\n'+new_password+'\n'+new_password+'\n')
                        #print(out)
                        is_change = True
                    else:
                        ssh_shell.sendall('\n')
                    time.sleep(float(1))
                    out = ssh_shell.recv(1024);
                if not is_change:
                    ssh_shell.sendall('local-user change-password\n'+old_password+'\n'+new_password+'\n'+new_password+'\n')
                    time.sleep(float(1))
                    out = ssh_shell.recv(1024);
                err = out
            elif device_type == 7:
                #华3交换机
                is_change = False
                ssh_shell = ssh.invoke_shell()
                out = ssh_shell.recv(1024);
                print(out)
                while not re.search('<.*?>', str(out,'utf-8')):
                    if 'change your password' in str(out,'utf-8'):
                        print('Y/N')
                        time.sleep(float(1))
                        #ssh_shell.sendall('Y\n')
                        ssh_shell.sendall(old_password+'\n')
                        out = ssh_shell.recv(1024);
                        print(out)
                        ssh_shell.sendall(new_password+'\n')
                        out = ssh_shell.recv(1024);
                        print(out)
                        ssh_shell.sendall(new_password+'\n')
                        out = ssh_shell.recv(1024);
                        print(out)
                        is_change = True
                    else:
                        ssh_shell.sendall('\n')
                    time.sleep(float(1))
                    out = ssh_shell.recv(1024);
                print(out)
                if not is_change:
                    res = ssh_shell.sendall('sys\n')
                    time.sleep(float(1))
                    out = ssh_shell.recv(1024);
                    print(out)
                    res = ssh_shell.sendall('local-user '+user+'\n')
                    time.sleep(float(1))
                    out = ssh_shell.recv(1024);
                    print(out)
                    if en_fail_hua3c1 not in str(out,'utf-8'):
                        res = ssh_shell.sendall('password simple '+new_password+'\n')
                        time.sleep(float(1))
                        out = ssh_shell.recv(1024);
                        print(out)
                        ssh_shell.sendall(old_password+'\n')
                        time.sleep(float(1))
                        out = ssh_shell.recv(1024);
                        print(out)
                        if en_fail_hua3c not in str(out,'utf-8'):
                            ssh_shell.sendall(new_password+'\n')
                            out = ssh_shell.recv(1024);
                            print(out)
                            ssh_shell.sendall(new_password+'\n')
                            out = ssh_shell.recv(1024);
                            print(out)
                err = out
        print(f"修改密码结果为:{out}")
        if successful in str(out, 'utf-8') or en_successful in str(out, 'utf-8') or successful in str(err, 'utf-8') or en_successful in str(err, 'utf-8') or (en_fail not in str(out,'utf-8') and en_fail_hua3c not in str(out,'utf-8') and en_fail_hua3c1 not in str(out,'utf-8')):
            print(Ip + " 密码修改成功！")
        else:
            print('\033[31m错误：\033[0m' + str(err, 'utf-8'))
            print(Ip + " 密码修改失败！")
        # 关闭连接
        ssh.close()
    except paramiko.ssh_exception.AuthenticationException as e:
        print(Ip + ' ' + '\033[31m账号密码错误!\033[0m')
        with open('/tmp/changePwdAccountError.txt', 'a') as f:
            f.write(Ip + '\n')
    except socket.timeout as e:
        print(Ip + ' ' + '\033[31m连接超时！\033[0m')
        with open('/tmp/changePwdTimeoutSsh', 'a') as f:
            f.write(Ip + '\n')

def changeWindows(Ip, port, user, old_password, new_password):
    print(Ip, port, allow_root, old_password, new_password)
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((Ip, port))
    except socket.error as msg:
        print(msg)
        print(Ip + ' ' + '\033[31m'+msg+'\033[0m')
        sys.exit(1)
    print('connect success!')
    print(client.recv(1024))
    msg = 'changepassword:'+user+'|'+new_password+'\x00'
    client.send(msg.encode('utf-8'))
    data = client.recv(1024).decode('gbk').encode("utf-8").decode()
    pos = data.find('\r')
    if pos > -1 :
        data = data[0:pos]
    if data.find('成功')>-1:
        print(Ip + " 密码修改成功！")
    else:
        print(Ip + " 密码修改失败！")
    print('recv:', data)
    client.close()

if __name__ == '__main__':
    new_password = GenPassword()
    print(f"新密码为{new_password}")
    #changeSSH(ip, port, allow_root, super_account, super_password, username, old_password, new_password)
    changeWindows(ip, port, username, old_password, new_password)
