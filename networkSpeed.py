#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
@Time : 2022/2/22 17:33
@Author : wxy
@contact: wxy18955007261@163.com
@file: networkSpeed.py
@desc:  
"""
from __future__ import division
import subprocess
import time
import re

TIME = 1  # 监视网速的时间间隔
DEVICE = 'eth0'
LOCAL = 'zh'
ALL = False


class NetSpeed():
    def __init__(self):
        self.device = DEVICE
        self.local = LOCAL

    def start(self):
        res = self.get_rx_tx(DEVICE)
        print('name:' + DEVICE + 'rx:' + res[0] + 'tx:' + res[1])

    # 调用系统命令ifconfig获取指定网卡名 已上传或者下载的字节大小，转换为kb
    def ifconfig(self, device='eth0', local='en'):
        output = subprocess.Popen(['ifconfig', device], stdout=subprocess.PIPE).communicate()[0]
        rx_bytes = re.findall('RX bytes:([0-9]*) ', output)[0]
        tx_bytes = re.findall('TX bytes:([0-9]*) ', output)[0]
        return float('%.3f' % (int(rx_bytes) / 1024)), float('%.3f' % (int(tx_bytes) / 1024))

    # 获取指定网卡的网速
    def get_rx_tx(self, device='eth0'):
        try:
            while True:
                rx_bytes, tx_bytes = self.ifconfig(device=device, local=self.local)
                time.sleep(TIME)
                rx_bytes_new, tx_bytes_new = self.ifconfig(device=device, local=self.local)

                col_rx = (rx_bytes_new - rx_bytes) / TIME
                col_tx = (tx_bytes_new - tx_bytes) / TIME

                col_rx = '%.3f' % col_rx
                col_tx = '%.3f' % col_tx
                return col_rx, col_tx
        except Exception as e:
            raise e


if __name__ == '__main__':
    speed = NetSpeed()
    print(speed.start())
