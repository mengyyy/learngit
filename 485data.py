#!/usr/bin/env python
# -*-coding: utf-8 -*-

import socket
import my_crc
import time


class RS485(object):

    def __init__(self, ss, dst, fun, addr):
        self.ss = ss
        self.dst = dst.zfill(2)
        self.fun = fun.zfill(2)
        self.addr = addr.zfill(4)
        self.head = self.dst + self.fun + self.addr

    def be_send(self):
        self.ss.send(self.crc)


class RS485_03_05_06(RS485):

    def __init__(self, ss, dst, fun, addr, num):
        RS485.__init__(self, ss, dst, fun, addr)
        self.num = num.zfill(4)

    def gen_crc(self):
        self.crc = my_crc.gen_st_crc(
            self.dst + self.fun + self.addr + self.num)

    def crc_chreck(self):
        return my_crc.crc_chreck(self.crc)


class RS495_10(RS485):

    def __init__(self, ss, dst, fun, addr, num1, num2, *data):
        RS485.__init__(self, ss, dst, fun, addr)
        self.num1 = num1.zfill(4)
        self.num2 = num2.zfill(2)
        ddaa = ''
        for da in data:
            ddaa = ddaa + da.zfill(2)
        self.data = ddaa

    def gen_crc(self):
        self.crc = my_crc.gen_st_crc(
            self.dst + self.fun + self.addr + self.num1 +
            self.num2 + self.data)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('172.247.39.7', 9999))

my_crc.init_table()

a03 = RS485_03_05_06(s, '01', '03', '07d0', '0006')
a03.gen_crc()

a10 = RS495_10(s, '02', '10', '8888', '0025',
               '50', '11', '22', '33', '44', '55')
a10 .gen_crc()

for i in range(10):
    a03.be_send()
    print(s.recv(10240))
    time.sleep(1)
    a10.be_send()
    time.sleep(1)
s.close()

print(a03.crc_chreck())
print(a03.crc)
