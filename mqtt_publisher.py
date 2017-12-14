#!/usr/bin/python
# This shows a service of an MQTT subscriber.
# Copyright (c) 2017-2020, By quanpower@gmail.com.

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
from utils import crc_func

#
# from app import db
# from app.models import LoraGateway, LoraNode, GrainBarn, AlarmLevelSetting, PowerIoRs485Func, PowerIo, NodeMqttTransFunc, GrainTemp, GrainStorehouse
# from sqlalchemy import and_
from utils import calc_modus_hex_str_to_send, crc_func, str2hexstr, calc

import struct

#======================================================    

log = logging.getLogger(__name__)

# try:
#     db.session.query(GrainTemp).delete()
#     db.session.commit()
# except:
#     db.session.rollback()

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
        packet_data = BitStream('0x'+ b)

        print('--------packet_data--------')
        print(packet_data)
        print('--------packet_data.bin--------')
        print(packet_data.bin)

        on_exec(str(msg.payload))
    else:
        print('nothings!')


def on_exec(strcmd):
    print ("Exec:", strcmd)
    strExec = strcmd


def lora_unpacking(packet_data):
    packet_data.pos = 56
    crc = packet_data.read(8)
    packet_data.pos = 0
    if crc == crc_func(packet_data.read(56)):
        packet_data.pos = 0
    else:
        pass


def packing(gateway_addr, node_addr , trans_direct, func_code, wind_direct, wind_speed, model, on_off, work_mode, temp):
    return bitstring.pack('bin, bin, bin, bin, bin, bin, bin, bin, bin, bin', gateway_addr, node_addr , trans_direct, func_code, wind_direct, wind_speed, model, on_off, work_mode, temp)
    

def transmitMQTT(strMsg):
    #strMqttBroker = "localhost"
    strMqttBroker = "101.200.158.2"
    strMqttChannel = "001.downstream"
    print(strMsg)
    curtime = datetime.datetime.now()
    strcurtime = curtime.strftime("%Y-%m-%d %H:%M:%S")
    # strMsg += strcurtime
    publish.single(strMqttChannel, strMsg, hostname=strMqttBroker, auth={'username': 'iiot', 'password': 'smartlinkcloud'})


def return_str_bin(node_addr, wind_direct, wind_speed, on_off, work_mode, temp, gateway_addr='0b001', trans_direct='0b1', func_code='0b0010001', model='0b0000011011'):
    return packing(gateway_addr, node_addr, trans_direct, func_code, wind_direct, wind_speed, model, on_off, work_mode, temp)


def return_crc(str_bin):
    print('----str_bin------')
    print(type(str_bin))
    print(str_bin)
    print('----len_str_bin------')
    print(len(str_bin))

    units = []
    for i in range(int(len(str_bin) / 8)):
        units.append(str_bin.read(8).uint)
    print('units', units)

    crc = crc_func(units)
    print('crc', crc)
    
    print('-------send-hex------')
    print(str_bin + hex(crc))
    return units,crc


def return_air_con_mqtt_str_bytes_to_send(str_bin):
    units,crc = return_crc(str_bin)

    str_bytes=struct.pack('7B', units[0], units[1], units[2], units[3], units[4], units[5], crc)
    print(len(str_bytes))
    print(repr(str_bytes))
    return str_bytes


def replace_0b(input):
    return input.replace('0b', '')


def mqtt_pub_air_con(data):
    # {'node_select': 2, 'wind_speed': 2, 'temp_setting': 28, 'wind_directtion': 1, 'switch': 1, 'working_model': 1}

    node_addr = bitstring.pack('uint:13',data['node_select']).bin
    wind_direct = bitstring.pack('uint:2',data['wind_directtion']).bin
    wind_speed = bitstring.pack('uint:2',data['wind_speed']).bin
    on_off = bitstring.pack('uint:2',data['switch']).bin
    work_mode = bitstring.pack('uint:3',data['working_model']).bin 
    temp = bitstring.pack('uint:5',data['temp_setting']).bin

    str_bin = return_str_bin(node_addr, wind_direct, wind_speed, on_off, work_mode, temp)
    str_bytes = return_air_con_mqtt_str_bytes_to_send(str_bin)

    transmitMQTT(str_bytes)


def mqtt_auto_control_air(node_mqtt_trans_func, on_off):

    gateway_addr = node_mqtt_trans_func[0][0]
    node_addr = node_mqtt_trans_func[0][1]
    trans_direct = node_mqtt_trans_func[0][2]
    func_code = node_mqtt_trans_func[0][3]
    wind_direct = node_mqtt_trans_func[0][4]
    wind_speed = node_mqtt_trans_func[0][5]
    model = node_mqtt_trans_func[0][6]
    work_mode = node_mqtt_trans_func[0][8]
    temp = node_mqtt_trans_func[0][9]
    
    str_origin = gateway_addr + node_addr + trans_direct + func_code +\
                 wind_direct + wind_speed + model + on_off + work_mode + temp
    print('-----str_origin-----')
    print(str_origin)
    str_bin = BitStream('0b' + str_origin)
    str_bytes = return_air_con_mqtt_str_bytes_to_send(str_bin)
    print('-----str_bytes-----')
    print(str_bytes)

    transmitMQTT(str_bytes)


def mqtt_pub_node_setting():
    gateway_addr = '0b001' # 1
    node_addr = '0b0000000010100' # 1
    trans_direct = '0b1'  # 1
    func_code = '0b0010010' # 18
    new_gateway_addr = '0b001'
    # new_node_addr = '0b0000000001111'
    new_node_addr = node_addr
    reserve = '0b0000'
    sleep_time = '0b0100101100' #5 minute
    # sleep_time = '0b0000110111' #55 second
    # sleep_time = '0b0001111000' #120 second

    send_power = '0b11'

    str_replaced = replace_0b(gateway_addr) + replace_0b(node_addr) + replace_0b(trans_direct) + replace_0b(func_code) + replace_0b(new_gateway_addr) + replace_0b(new_node_addr) + replace_0b(reserve) + replace_0b(sleep_time) + replace_0b(send_power)
    print('str_repalced:', str_replaced)
    str_bin = BitStream('0b' + str_replaced)
    print('str_bin:', str_bin)
    units, crc = return_crc(str_bin)
    str_bytes = struct.pack('8B', units[0], units[1], units[2], units[3], units[4], units[5], units[6], crc)
    print(str_bytes)
    print(len(str_bytes))
    print(repr(str_bytes))

    transmitMQTT(str_bytes)



if __name__ == '__main__':
    # while 1:
    #     mqtt_pub_node_setting()
    #     time.sleep(10)


    for i in range(10):
        model_int = 20+i
        print('model_int')
        print(model_int)
        model_bin=bin(model_int)[2:]
        model='0b00000'+model_bin
        print(model)

        gateway_addr = '0b001' # 1
        node_addr = '0b0000000010001' # 17
        # node_addr = '0b0000000011101' # 29
        trans_direct = '0b1'  # 1
        func_code = '0b0010001' # 17
        wind_direct = '0b01' #
        wind_speed = '0b11' #1
        # model = '0b0001100011' # sanling 569
        # model = '0b0000010110' # sanling 569
        # model = '0b0000101101' # media 45

        on_off = '0b01' # on
        work_mode = '0b001' #cold
        temp = '0b10000' #16

        def replace_0b(input):
            return input.replace('0b', '')

        # str_bin = return_str_bin(gateway_addr, node_addr, trans_direct, func_code, wind_direct, wind_speed, model, on_off, work_mode, temp)
        # str_bin = bitstring.pack(gateway_addr, node_addr, trans_direct, func_code, wind_direct, wind_speed, model, on_off, work_mode, temp)

        str_replaced = replace_0b(gateway_addr) + replace_0b(node_addr) + replace_0b(trans_direct) + replace_0b(func_code) + replace_0b(wind_direct) + replace_0b(wind_speed) + replace_0b(model) + replace_0b(on_off) + replace_0b(work_mode) + replace_0b(temp)

        print('str', str_replaced)
        print(len(str_replaced))
        str_bin = BitStream('0b' + str_replaced)
        str_bytes = return_air_con_mqtt_str_bytes_to_send(str_bin)

        transmitMQTT(str_bytes)
        print(i)
        time.sleep(60)
        print(5 * '\n')


    # mqtt_pub_node_setting()

        
