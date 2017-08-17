#!/usr/bin/python
# This shows a service of an MQTT subscriber.
# Copyright (c) 2010-2015, By openthings@163.com.

import sys
import datetime
import socket, sys
import struct
from bitstring import BitArray, BitStream
import binascii
# from app.models import GrainTemp
import logging
# from app import db
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

        # realtime_data = lora_unpacking_realtime_data(packet_data)

        # save_realtime_data(realtime_data)

        # on_exec(str(msg.payload))
    else:
        print('nothings!')
        b = binascii.b2a_hex(msg.payload)
        # packet_data = BitStream('0x4001004751E47533')
        # '{:0>2x}'.format(1) #dic to hex,append 0
        packet_data = BitStream('0x'+ b)

        print('--------packet_data--------')
        print(packet_data)
        print('--------packet_data.bin--------')
        print(packet_data.bin)

        # realtime_data = lora_unpacking_realtime_data(packet_data)

        # save_realtime_data(realtime_data)

        # on_exec(str(msg.payload))



def on_exec(strcmd):
    print "Exec:",strcmd
    strExec = strcmd

def lora_unpacking(packet_data):
    packet_data.pos = 56
    crc = packet_data.read(8)
    packet_data.pos = 0
    if crc == crc_func(packet_data.read(56)):
        packet_data.pos = 0


    else:
        pass

def lora_unpacking_realtime_data(packet_data):
    print('--------real data process beginning-----------')

    gateway_addr = packet_data.read(3).uint
    node_addr = packet_data.read(13).int
    tran_direct = packet_data.read(1).bool
    func_code = packet_data.read(3)
    switch = packet_data.read(1).bool

    temp1_sign = packet_data.read(1).bool
    temp2_sign = packet_data.read(1).bool
    temp3_sign = packet_data.read(1).bool

    temp1 = packet_data.read(10).uint
    temp2 = packet_data.read(10).uint
    temp3 = packet_data.read(10).uint
    battery_vol =  packet_data.read(2).uint


    def sign(temp_sign):
        if not temp_sign:
            sign = 1
        else:
            sign = -1
        return sign

    temprature1 = (sign(temp1_sign) * temp1)/10.0
    temprature2 = (sign(temp2_sign) * temp2)/10.0
    temprature3 = (sign(temp3_sign) * temp3)/10.0

    print('gateway_addr:',gateway_addr)
    print('-------------------')
    print('node_addr:',node_addr)
    print('-------------------')

    print('tran_direct:',tran_direct)
    print('-------------------')

    print('func_code:',func_code)
    print('-------------------')

    print('switch:',switch)
    print('-------------------')

    print('temp1_sign',temp1_sign)
    print('-------------------')

    print('temp2_sign',temp2_sign)
    print('-------------------')

    print('temp3_sign',temp3_sign)
    print('-------------------')

    print('temp1:',temp1)
    print('-------------------')

    print('temp2:',temp2)
    print('-------------------')

    print('temp3:',temp3)
    print('-------------------')

    print('battery_vol:',battery_vol)
    
    print(temprature1, temprature2, temprature3, battery_vol)

    return (gateway_addr, node_addr, switch, temprature1, temprature2, temprature3, battery_vol)

def save_realtime_data(data):
    c = GrainTemp()
    c.gateway_addr = data[0]
    c.node_addr = data[1]
    c.switch = data[2]
    c.temp1 = data[3]
    c.temp2 = data[4]
    c.temp3 = data[5]
    c.battery_vol = data[6]
    c.datetime = datetime.datetime.now()

    db.session.add(c)
    try:
        db.session.commit()
        print "inserted", c
    except Exception, e:
        log.error("Inserting Grian_temp: %s", e)
        db.session.rollback()


def lora_unpacking_ack(packet_data):
    # todo
    print('-------- ack data process beginning -----------')


    

def crc_func(bitstring):
    pass
    # todo
    
#=====================================================
if __name__ == '__main__': 
    mqttc = mqtt.Client("mynodeserver")
    mqttc.username_pw_set("iiot", "smartlinkcloud")
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    mqttc.on_log = on_log

    #strBroker = "localhost"
    strBroker = "101.200.158.2"

    mqttc.connect(strBroker, 1883, 60)
    mqttc.subscribe("001.downstream", 0)
    mqttc.loop_forever()