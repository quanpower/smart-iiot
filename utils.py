import sys
import datetime
import socket, sys
import struct
import bitstring
from bitstring import BitArray, BitStream
import binascii
# from app.models import GrainTemp
import logging
# from app import db

import paho.mqtt.publish as publish
import time

def crc_func(units):
    _crc = 0
    for i in units:
        _crc += i
        if _crc > 255:
            _crc %= 256

    print(_crc)

    _crc = bitwise_reverse(_crc)
    _crc += 1

    return _crc

def bitwise_reverse(int_src):
    bin_str = bitstring.pack('uint:8',int_src).bin
    ret = "".join(map(lambda x: "1" if x == "0" else "0", bin_str))
    print(ret)
    return int(ret, 2)

def sign(temp_sign):
    if not temp_sign:
        sign = 1
    else:
        sign = -1
    return sign