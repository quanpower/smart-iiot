#!/usr/bin/python
# This shows a service of an MQTT subscriber.
# Copyright (c) 2017-2020, By quanpower@gmail.com.

import sys
import datetime
import socket, sys

import binascii
# from app.models import GrainTemp
import logging
# from app import db

import paho.mqtt.publish as publish
import time 
from utils import crc_func
from app.models import LoraGateway, LoraNode, GrainBarn, AlarmLevelSetting, PowerIo, NodeMqttTransFunc, GrainTemp, GrainStorehouse, RelayCurrentRs485Func
#
# from app import db
# from app.models import LoraGateway, LoraNode, GrainBarn, AlarmLevelSetting, PowerIoRs485Func, PowerIo, NodeMqttTransFunc, GrainTemp, GrainStorehouse
# from sqlalchemy import and_
from utils import calc_modus_hex_str_to_send, crc_func, str2hexstr, calc

import struct

#======================================================    

log = logging.getLogger(__name__)



#MQTT Initialize.--------------------------------------
try:
    import paho.mqtt.client as mqtt
except ImportError:
    print("MQTT client not find. Please install as follow:")
    print("git clone http://git.eclipse.org/gitroot/paho/org.eclipse.paho.mqtt.python.git")
    print("cd org.eclipse.paho.mqtt.python")
    print("sudo python setup.py install")

#======================================================
# def on_connect(mqttc, obj, rc):
def on_connect(client, userdata, flags, rc):
    print("OnConnetc, rc: "+str(rc))

def on_publish(mqttc, obj, mid):
    print("OnPublish, mid: "+str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(mqttc, obj, level, string):
    print("Log:"+string)

def on_message(mqttc, obj, msg):
    curtime = datetime.datetime.now()
    strcurtime = curtime.strftime("%Y-%m-%d %H:%M:%S")
    print(strcurtime + ": " + msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

    # packet_data = BitArray('0x4001004751E47533')
    # bit_payload = BitStream(msg.payload)
    # bit_payload = BitStream(bytes=msg.payload, length=64, offset=0)

    # print('bit-payload')
    # print(bit_payload)

    # print(len(msg.payload))
    if len(msg.payload) == 5:
        print('ack received')
    elif len(msg.payload) == 8:
        # un_int = struct.unpack(str(len(msg.payload)) + 'B', msg.payload)
        # print(un_int)
        b = binascii.b2a_hex(msg.payload)
        # packet_data = BitStream('0x4001004751E47533')
        # '{:0>2x}'.format(1) #dic to hex,append 0
        # packet_data = BitStream(b)

        # print('--------packet_data--------')
        # print(packet_data)
        # print('--------packet_data.bin--------')
        # print(packet_data.bin)
        #
        # on_exec(str(msg.payload))
    else:
        print('nothings!')


def on_exec(strcmd):
    print ("Exec:",strcmd)
    strExec = strcmd



def transmitMQTT(strMsg):
    #strMqttBroker = "localhost"
    strMqttBroker = "101.200.158.2"
    strMqttChannel = "001.passthrough_downstream"
    print('strMsg is:')
    print(strMsg)
    curtime = datetime.datetime.now()
    strcurtime = curtime.strftime("%Y-%m-%d %H:%M:%S")
    # strMsg += strcurtime
    publish.single(strMqttChannel, strMsg, hostname=strMqttBroker, auth={'username': 'iiot', 'password': 'smartlinkcloud'})



def return_crc(str_bin):
    print('----str_bin------')
    print(str_bin)
    print('----len_str_bin------')
    print(len(str_bin))

    units = []
    for i in range(int(len(str_bin) / 8)):
        units.append(str_bin.read(8).uint)
    print('units', units)

    crc = crc_func(units)
    print('-------send-hex------')
    print(str_bin + hex(crc))
    return units, crc

def test_pymodbus_crc():

    import pymodbus.utilities
    from pymodbus.compat import int2byte
    meins=[]
    meins.append(0x10)
    meins.append(0x33)
    meins.append(0x01)
    meins.append(0x01)

    meins1=b''
    for i in meins:
        meins1 = meins1 + int2byte(i)

    meins2=b'\x10\x33\x01\x01'

    meins3=bytearray.fromhex("10330101")

    crc=hex(pymodbus.utilities.computeCRC(b'\x10\x33\x01\x01'))
    print(crc)
    crc=hex(pymodbus.utilities.computeCRC(meins))
    print(crc)
    crc=hex(pymodbus.utilities.computeCRC(meins1))
    print(crc)
    crc=hex(pymodbus.utilities.computeCRC(meins2))
    print(crc)
    crc=hex(pymodbus.utilities.computeCRC(meins3))
    print(crc)

    # xihe = "081000000001020100CD90"
    xihe = "081000000001020100"
    xihe_bytes = bytes.fromhex(xihe)
    xihe_bytearray=bytearray.fromhex(xihe)
    crc = hex(pymodbus.utilities.computeCRC(xihe_bytearray))

    print(xihe_bytearray)
    print(crc)
    print(type(crc))



def gen_modbus_bytes():

    import pymodbus.utilities
    from pymodbus.compat import int2byte

    daq_adrresses = ['01', '02', '03', '04', '05', '06', '07', '08']
    release_func_code = '1000000001020000'
    suck_func_code = '1000000001020100'

    # xihe="\x01\x10\x00\x00\x00\x01\x02\x01\x01\x66\x00"
    # # xihe="0110000000010201016600"
    # shifang="\x01\x10\x00\x00\x00\x01\x02\x00\x01\x67\x90"
    # dianliu="\x01\x03\x00\x04\x00\x04\x05\xC8"
    # ma="\x40\xe0\x6e\x8b"

    suck_func_bytes=[]
    release_func_bytes=[]
    releay_func_bytes=[]
    for daq_adrress in daq_adrresses:
        suck_hex_func = daq_adrress + suck_func_code
        release_hex_func = daq_adrress + release_func_code

        suck_func_bytearray = bytearray.fromhex(suck_hex_func)
        release_func_bytearray = bytearray.fromhex(release_hex_func)

        suck_crc = pymodbus.utilities.computeCRC(suck_func_bytearray)
        release_crc = pymodbus.utilities.computeCRC(release_func_bytearray)

        suck_hex_str = daq_adrress + suck_func_code + hex(suck_crc)[2:]
        release_hex_str = daq_adrress + release_func_code + hex(release_crc)[2:]

        suck_func_byte = bytes.fromhex(suck_hex_str)
        release_func_byte = bytes.fromhex(release_hex_str)

        suck_func_bytes.append(suck_func_byte)
        release_func_bytes.append(release_func_byte)
        releay_func_bytes.append([suck_func_byte, release_func_byte])

        print('---------{}----------'.format(daq_adrress))

        print('-----suck_func_bytes------')
        print(suck_func_byte)
        print('-----release_func_bytes-----')
        print(release_func_byte)
        print('----------------------')

    return releay_func_bytes


def gen_modbus_byte(powerNo, func_code):

    import pymodbus.utilities
    from pymodbus.compat import int2byte


    hex_powerNo = ''.join(format(int(powerNo), '02x'))
    hex_func = hex_powerNo + func_code

    # hex_powerNo2 = "".join("{:02x}".format(int(powerNo)))
    # print('----hex_powerNo,hex_func---')
    # print(hex_powerNo)
    # print(hex_func)
    func_bytearray = bytearray.fromhex(hex_func)
    # print('----func_bytearray---')
    # print(func_bytearray)

    crc = pymodbus.utilities.computeCRC(func_bytearray)
    crc_bytes = struct.pack('>H',crc)
    crc_bytes2 = (crc).to_bytes(2, byteorder='big')
    # print('------crc_bytes--------')
    # print(crc_bytes)
    # print(crc_bytes2)

    crc_hex = binascii.b2a_hex(crc_bytes)
    hex_str = hex_func + crc_hex.decode()
    # print('----hex_str---')
    # print(hex_str)

    func_byte = bytes.fromhex(hex_str)
    # print('----func_byte----')
    # print(func_byte)

    func_byte1 = bytes.fromhex(hex_func) + crc_bytes2
    # print('----func_byte1----')
    # print(func_byte1)

    print('---------{}----------'.format(powerNo))
    print('-----func_byte-----')
    print(func_byte)
    print('----------------------')

    return func_byte


def transmitMQTT_byte(powerNo, func_code):

    func_byte = gen_modbus_byte(powerNo, func_code)
    transmitMQTT(func_byte)


if __name__ == '__main__':

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    # 初始化数据库连接:
    engine = create_engine('sqlite:///data.sqlite')
    # 创建DBSession类型:
    Session = sessionmaker(bind=engine)
    db_session=Session()

    for i in range(1000):

        # releay_func_bytes = gen_modbus_bytes()

        # for releay_func_byte in releay_func_bytes:

        #     print('-----------send-time------------')
        #     print(datetime.datetime.now())
        #     print('----xihe begin----')

        #     transmitMQTT(releay_func_byte[0])

        #     time.sleep(10)
        #     print('----shifang begin----')

        #     transmitMQTT(releay_func_byte[1])

        time.sleep(10)



        current_daq_func_code = db_session.query(RelayCurrentRs485Func.function_code).filter(
                RelayCurrentRs485Func.function_name == 'current_A1_A2_func_code').first()
        print('-------current_daq_func_code-----')
        print(current_daq_func_code)
        transmitMQTT_byte('3', current_daq_func_code[0])



