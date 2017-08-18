#!/usr/bin/python
# This shows a service of an MQTT subscriber.
# Copyright (c) 2010-2015, By openthings@163.com.

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

        realtime_data = lora_unpacking_realtime_data(packet_data)

        save_realtime_data(realtime_data)

        on_exec(str(msg.payload))
    else:
        print('nothings!')


def on_exec(strcmd):
    print ("Exec:",strcmd)
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
    publish.single(strMqttChannel, strMsg, hostname = strMqttBroker, auth = {'username':'iiot', 'password':'smartlinkcloud'})

#=====================================================
# if __name__ == '__main__': 
#     mqttc = mqtt.Client("mynodeserver")
#     mqttc.username_pw_set("iiot", "smartlinkcloud")
#     mqttc.on_message = on_message
#     mqttc.on_connect = on_connect
#     mqttc.on_publish = on_publish
#     mqttc.on_subscribe = on_subscribe
#     mqttc.on_log = on_log

#     #strBroker = "localhost"
#     strBroker = "101.200.158.2"

#     mqttc.connect(strBroker, 1883, 60)
#     mqttc.subscribe("001.downstream", 0)
#     mqttc.loop_forever()


if __name__ == '__main__':

    gateway_addr = '0b001' # 1
    node_addr = '0b0000000000001' # 1
    trans_direct = '0b1'  # 1
    func_code = '0b0010001' # 17
    wind_direct = '0b00' #auto
    wind_speed = '0b00' #1
    model = '0b1101100000' #
    on_off = '0b01' # on
    work_mode = '0b001' #cold
    temp = '0b11100' #28

    str_bin = packing(gateway_addr, node_addr, trans_direct, func_code, wind_direct, wind_speed, model, on_off, work_mode, temp)
    print('----str_bin------')
    print(str_bin.bin)
    print(str_bin.hex)
    print('----str_bin------')

    print(len(str_bin))


    units = []
    for i in range(int(len(str_bin) / 8)):
        units.append(str_bin.read(8).uint)
    print(units)

    crc = crc_func(units)
    print('-------hex------')
    print(hex(crc))

    str_bytes=struct.pack('7B', units[0], units[1], units[2], units[3], units[4], units[5], crc)

    print(str_bytes)
    print(len(str_bytes))
    print(repr(str_bytes))

    for i in range(0, 999999):
        time.sleep(1)

        transmitMQTT(str_bytes)
        # transmitMQTT(str_hex + "--{0}--".format(i))

        print ("Send msg ok.{0}".format(i))
