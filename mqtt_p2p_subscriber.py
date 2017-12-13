from flask import current_app
import os
import sys
import datetime
import socket, sys
import struct
from bitstring import BitArray, BitStream
import binascii
import logging
from utils import crc_func, sign
import random


from app.models import GrainTemp, LoraNode

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 初始化数据库连接:
engine = create_engine('sqlite:///data.sqlite')
# 创建DBSession类型:
Session = sessionmaker(bind=engine)
db_session=Session()

# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关

# 第二步，创建一个handler，用于写入日志文件
parent_dir = os.path.dirname(__file__)
logfile = os.path.join(parent_dir, 'log/mqtt_p2p_sub_logger.txt')
fh = logging.FileHandler(logfile, mode='w')
fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关

# 第三步，再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)  # 输出到console的log等级的开关

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

# ======================================================


# try:
#     db.session.query(GrainTemp).delete()
#     db.session.commit()
# except:
#     db.session.rollback()

# MQTT Initialize.--------------------------------------
try:
    import paho.mqtt.client as mqtt
except ImportError:
    print("MQTT client not find. Please install as follow:")
    print("git clone http://git.eclipse.org/gitroot/paho/org.eclipse.paho.mqtt.python.git")
    print("cd org.eclipse.paho.mqtt.python")
    print("sudo python setup.py install")


# ======================================================
# def on_connect(mqttc, obj, rc):
def on_connect(client, userdata, flags, rc):
    logger.info("OnConnetc, rc: " + str(rc))


def on_publish(mqttc, obj, mid):
    logger.info("OnPublish, mid: " + str(mid))


def on_subscribe(mqttc, obj, mid, granted_qos):
    logger.info("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    logger.info("Log:" + string)


def on_message(mqttc, obj, msg):
    curtime = datetime.datetime.now()
    strcurtime = curtime.strftime("%Y-%m-%d %H:%M:%S")
    logger.info(strcurtime + ": " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    payload_length = len(msg.payload)
    un_int = struct.unpack(str(payload_length) + 'B', msg.payload)

    logger.info('*********---NEW MESSAGE----*********')
    print(5 * '\n')
    print(2 * '*********---NEW MESSAGE----*********')
    logger.info(payload_length)
    print('-------payload_length------')
    print(payload_length)
    logger.info(un_int)
    print(un_int)
    uints = list(un_int)
    print(uints)

    if uints[payload_length - 1] == crc_func(uints[:payload_length - 1]):
        logger.info('CRC checked!')

        if payload_length == 5:
            lora_unpacking_ack(uints)
        elif payload_length == 8:
            print('----msg.payload------')
            print(msg.payload)
            print(type(msg.payload))
            print('--------receive-time-------')
            print(datetime.datetime.now())

            # packet_data = BitStream('0x4001004751E47533')
            # '{:0>2x}'.format(1) #dic to hex,append 0
            packet_data = BitStream(msg.payload)
            logger.info('--------packet_data--------')
            logger.info(packet_data)
            logger.info(len(packet_data))
            print('-----packet-data------')
            print(packet_data)
            logger.info('--------packet_data.bin--------')
            logger.info(packet_data.bin)
            print(packet_data.bin)
            logger.info(len(packet_data.bin))

            realtime_data = lora_unpacking_realtime_data(packet_data)

            save_realtime_data(realtime_data)
        else:
            logger.debug('bytes unknown!')

    else:
        logger.error('CRC check fail!')


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


def lora_unpacking_realtime_data(packet_data):
    logger.info('--------real data process beginning-----------')

    gateway_addr = str(packet_data.read(3).uint)
    node_addr = str(packet_data.read(13).int)
    tran_direct = packet_data.read(1).bool
    func_code = packet_data.read(3)
    switch = packet_data.read(1).bool

    temp1_sign = packet_data.read(1).bool
    temp2_sign = packet_data.read(1).bool
    temp3_sign = packet_data.read(1).bool

    temp1 = packet_data.read(10).uint
    temp2 = packet_data.read(10).uint
    temp3 = packet_data.read(10).uint
    battery_vol = packet_data.read(2).uint

    temprature1 = (sign(temp1_sign) * temp1) / 10.0
    temprature2 = (sign(temp2_sign) * temp2) / 10.0
    temprature3 = (sign(temp3_sign) * temp3) / 10.0

    logger.info('gateway_addr: %s', gateway_addr)
    logger.info('-------------------')
    logger.info('node_addr: %s', node_addr)
    print('--------node_addr----------')
    print(node_addr)
    print('----------------------------')
    logger.info('-------------------')

    logger.debug('tran_direct: %s', tran_direct)
    logger.debug('-------------------')

    logger.debug('func_code: %s', func_code)
    logger.debug('-------------------')

    logger.debug('switch: %s', switch)
    logger.debug('-------------------')

    logger.debug('temp1_sign', temp1_sign)
    logger.debug('-------------------')

    logger.debug('temp2_sign', temp2_sign)
    logger.debug('-------------------')

    logger.debug('temp3_sign', temp3_sign)
    logger.debug('-------------------')

    logger.info('temp1: %s', temp1)

    logger.info('temp2: %s', temp2)

    logger.info('temp3: %s', temp3)
    logger.info('-------------------')

    logger.info('battery_vol: %s', battery_vol)

    logger.info('values : %s, %s, %s, %s', temprature1, temprature2, temprature3, battery_vol)

    return (gateway_addr, node_addr, switch, temprature1, temprature2, temprature3, battery_vol)


def save_realtime_data(data):
    c = GrainTemp()
    c.grain_storehouse_id = 1
    c.lora_gateway_id = data[0]
    # c.grain_barn_id = 1
    # c.lora_node_id = data[1]
    c.switch = data[2]
    c.temp1 = data[3]
    c.temp2 = data[5]
    c.temp3 = data[4]
    c.battery_vol = data[6]
    c.datetime = datetime.datetime.now()

    grain_barn_id = db_session.query(LoraNode.grain_barn_id).filter(
            LoraNode.node_addr == data[1]).first()[0]
    lora_node_id = db_session.query(LoraNode.id).filter(
            LoraNode.node_addr == data[1]).first()[0]
    c.grain_barn_id = grain_barn_id
    c.lora_node_id = lora_node_id

    print('----grain_barn_id----')
    print(grain_barn_id)

    db_session.add(c)
    try:
        db_session.commit()
        logger.debug('inserted!')
    except Exception as e:
        logger.error("Inserting Grian_temp: %s", e)
        db_session.rollback()
    # DBSession.close()


def lora_unpacking_ack(packet_data):
    # todo
    print(3 * '\n')

    print('''***************************************************\n
        **-------- ack data process beginning -----------**\n
        ***************************************************''')

    print(3 * '\n')
# =====================================================
# if __name__ == '__main__':
def mqtt_p2p_sub():
    mqttc = mqtt.Client("mqtt_p2p_sub" + str(random.choice(range(100))))
    mqttc.username_pw_set("iiot", "smartlinkcloud")
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    mqttc.on_log = on_log

    # strBroker = "localhost"
    strBroker = "101.200.158.2"

    mqttc.connect(strBroker, 1883, 60)
    mqttc.subscribe("001.upstream", 0)
    mqttc.loop_forever()


if __name__ == '__main__':
    # app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    mqtt_p2p_sub()