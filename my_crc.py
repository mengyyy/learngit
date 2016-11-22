#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY3:
    import binascii  # python3

INITIAL_MODBUS = 0xFFFF
INITIAL_DF1 = 0x0000


def init_table():
    # Initialize the CRC-16 table,
    #   build a 256-entry list, then convert to read-only tuple
    global table
    lst = []
    for i in range(256):
        data = i << 1
        crc = 0
        for j in range(8, 0, -1):
            data >>= 1
            if (data ^ crc) & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
        lst.append(crc)
    table = tuple(lst)
    return


def calcString(st, crc=INITIAL_MODBUS):
    """Given a bunary string and starting CRC, Calc a final CRC-16 """
    for ch in st:
        crc = (crc >> 8) ^ table[(crc ^ ord(ch)) & 0xFF]
    return crc


def calc_b_Str(b_st, crc=INITIAL_MODBUS):
    """Given a bunary string and starting CRC, Calc a final CRC-16 """
    for ch in b_st:
        crc = (crc >> 8) ^ table[(crc ^ ch) & 0xFF]
    return crc


def conver_st_hex(st):
    if PY3:
        st_hex = binascii.a2b_hex(st)
    if PY2:
        st_hex = st.decode('hex')
    return st_hex


def gen_st_crc(st):
    a = re.sub('\s+', '', st)
    if len(a) % 2 == 1:
        a = a + '0'
    b = conver_st_hex("".join(a.split()))
    if PY3:
        c = calc_b_Str(b)
    if PY2:
        c = calcString(b)
    d = conver_st_hex(
        (hex(c)[2:].zfill(4)[2:] + hex(c)[2:].zfill(4)[:2]))
    return b + d


def crc_chreck(st):
    if PY2:
        return 0 == calcString(st)
    if PY3:
        return 0 == calc_b_Str(st)

if __name__ == '__main__':
    init_table()
    while True:
        if PY3:
            a = input('please input hex str\n>>>')
        if PY2:
            a = raw_input('please input hex str\n>>>')
        if a == 'exit()':
            break
        if len(a.replace(' ', '')) % 2:
            a += '0'
        try:
            b = conver_st_hex("".join(a.split()))  # python3
            if PY3:
                c = calc_b_Str(b)
            if PY2:
                c = calcString(b)
        except TypeError:
            print("Input TypeError!!! Tyr again~~~")
            continue
        d = conver_st_hex(
            (hex(c)[2:].zfill(4)[2:] + hex(c)[2:].zfill(4)[:2]))
        print("%r" % (b + d))
    exit()

