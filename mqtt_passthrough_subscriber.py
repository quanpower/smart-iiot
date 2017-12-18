# -*- coding:utf-8 -*-
import os
import sys
import datetime
import socket, sys
import struct
from bitstring import BitArray, BitStream
import binascii
from app.models import LoraNode, PowerIo
import logging
from app import db
from utils import crc_func, sign


from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///data.sqlite')
# 创建DBSession类型:
Session = sessionmaker(bind=engine)
db_session=Session()


# 第一步，创建一个logger  
logger = logging.getLogger()  
logger.setLevel(logging.INFO)    # Log等级总开关  
  
# 第二步，创建一个handler，用于写入日志文件  
parent_dir = os.path.dirname(__file__)
logfile = os.path.join(parent_dir, 'log/mqtt_passthrough_sub_logger.txt')
fh = logging.FileHandler(logfile, mode='w')  
fh.setLevel(logging.DEBUG)   # 输出到file的log等级的开关  
  
# 第三步，再创建一个handler，用于输出到控制台  
ch = logging.StreamHandler()  
ch.setLevel(logging.WARNING)   # 输出到console的log等级的开关  
  
# 第四步，定义handler的输出格式  
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")  
fh.setFormatter(formatter)  
ch.setFormatter(formatter)  
  
# 第五步，将logger添加到handler里面  
logger.addHandler(fh)  
logger.addHandler(ch)  
  
# 日志  
logger.debug('this is a logger debug message')  
logger.info('this is a logger info message')  
logger.warning('this is a logger warning message')  
logger.error('this is a logger error message')  
logger.critical('this is a logger critical message') 

#======================================================    

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
    logger.info("OnConnetc, rc: "+str(rc))

def on_publish(mqttc, obj, mid):
    logger.info("OnPublish, mid: "+str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    logger.info("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(mqttc, obj, level, string):
    logger.info("Log:"+string)

def on_message(mqttc, obj, msg):
    curtime = datetime.datetime.now()
    strcurtime = curtime.strftime("%Y-%m-%d %H:%M:%S")
    logger.info(strcurtime + ": " + msg.topic+" "+str(msg.qos)+" "+str(msg.payload))  

    print('-----------------receive time----------------------')
    print(datetime.datetime.now())

    payload_length = len(msg.payload)
    print('-------payload_length---------')
    print(msg.payload)
    print(payload_length)
    un_int = struct.unpack(str(payload_length) + 'B', msg.payload)
    print(un_int)
    uints = list(un_int)
    print(uints)

    if payload_length == 13:
    
        currents = lora_unpacking_current_a1a2(msg.payload)

        update_current(currents)


def on_exec(strcmd):
    logger.debug("Exec:", strcmd)
    strExec = strcmd


def lora_unpacking(packet_data):
    packet_data.pos = 56
    crc = packet_data.read(8)
    packet_data.pos = 0
    if crc == crc_func(packet_data.read(56)):
        packet_data.pos = 0
    else:
        pass


def lora_unpacking_current_a1a2(packet_data):
    logger.info('--------current_a1a2 process beginning-----------')
    print('--------current_a1a2 process beginning-----------')

    int_power_io_addr = int.from_bytes(packet_data[0:1], byteorder='big')
    power_io_addr = str(int_power_io_addr)
    print('----int_power_io_addr-----')
    print(int_power_io_addr)
    print(power_io_addr)
    current_bytes_1 = packet_data[3:7]
    current_bytes_2 = packet_data[7:11]

    print('-----current_bytes------')
    print(packet_data)
    print(current_bytes_1)
    print(current_bytes_2)

    # hex_current1 = binascii.b2a_hex(current_bytes_1).decode()
    # print(hex_current1)


    current_value_mA_1 = struct.unpack('!f', current_bytes_1)[0]
    current_value_A_1 = round(10 * ((current_value_mA_1-4.0)/16), 2)
    current_value_mA_2 = struct.unpack('!f', current_bytes_2)[0]
    current_value_A_2 = round(10 * ((current_value_mA_2-4.0)/16), 2)
    
    print('-----current_value_mA------')
    print(current_value_mA_1)
    print(current_value_mA_2)
    print('-----current_value_A------')
    print(current_value_A_1)
    print(current_value_A_2)

    return (power_io_addr, current_value_A_1, current_value_A_2)


def update_current(data):
    power_io_addr = data[0]
    current1 = data[1]
    current2 = data[2]
    print('-----power_io_addr------')
    print(power_io_addr)
    # node1_query = db_session.query(LoraNode.node_addr).filter(LoraNode.current_no == 1).all()
    node1_query = db_session.query(LoraNode.node_addr).join(PowerIo, PowerIo.id == LoraNode.power_io_id).filter(and_(PowerIo.addr == power_io_addr, LoraNode.current_no == 1)).first()
    print(node1_query)
    if node1_query:
        node1 = node1_query[0]
    node2_query = db_session.query(LoraNode.node_addr).join(PowerIo, PowerIo.id == LoraNode.power_io_id).filter(and_(PowerIo.addr == power_io_addr, LoraNode.current_no == 2)).first()
    if node2_query:
        node2 = node2_query[0]
    print('--------node1,node2------------')


    lora_node = db_session.query(LoraNode).filter_by(node_addr=node1).first()  
    lora_node.current = current1

    lora_node1 = db_session.query(LoraNode).filter_by(node_addr=node2).first()  
    lora_node1.current = current2


    try:
        db_session.commit()
        logger.debug('updated!') 
    except Exception as e:
        logger.error("Inserting LoraNode: %s", e)
        db_session.rollback()


def lora_unpacking_ack(packet_data):
    # todo
    logger.info('-------- ack data process beginning -----------')
    print('------receive time------')
    print(datetime.datetime.now())

#=====================================================
def mqtt_passthrough_sub():

    mqttc = mqtt.Client("001.passthrough_subscriber")
    mqttc.username_pw_set("iiot", "smartlinkcloud")
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    mqttc.on_log = on_log

    #strBroker = "localhost"
    strBroker = "101.200.158.2"

    mqttc.connect(strBroker, 1883, 60)
    mqttc.subscribe("001.passthrough_upstream", 0)
    mqttc.loop_forever()

if __name__ == '__main__':

    mqtt_passthrough_sub()