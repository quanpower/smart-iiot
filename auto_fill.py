# -*- coding:utf-8 -*-

import logging
from app import db
import random
from datetime import datetime
import datetime
import bitstring

log = logging.getLogger(__name__)

from app.models import GrainStorehouse, GrainBarn, LoraGateway, LoraNode, GrainTemp, PowerIo,\
    AlarmLevelSetting, TianshuoRs485, PowerIoRs485Func, TianshuoRs485Func, NodeMqttTransFunc  #ConcLocation, ConcGateway, ConcRegion, ConcNode, ConcTemp


try:
    grain_storehouses = list()
    grain_storehouses.append(GrainStorehouse(storehouse_no='1', storehouse_name=u'福州直属库'))
    db.session.add(grain_storehouses[0])
    db.session.commit()
except Exception, e:
    log.error("Creating grain_storehouse: %s", e)
    db.session.rollback()


try:
    lora_gateways = list()
    lora_gateways.append(LoraGateway(gateway_addr='1', grain_storehouse=grain_storehouses[0]))

    db.session.add(lora_gateways[0])
    db.session.commit()
except Exception, e:
    log.error("Creating lora_gateway: %s", e)
    db.session.rollback()


try:
    grain_barns = list()
    grain_barns.append(GrainBarn(barn_no='1', barn_name=u'9号仓', grain_storehouse=grain_storehouses[0], lora_gateway=lora_gateways[0], high_limit=30, low_limit=20 ))
    grain_barns.append(GrainBarn(barn_no='2', barn_name=u'11号仓', grain_storehouse=grain_storehouses[0], lora_gateway=lora_gateways[0], high_limit=30, low_limit=20 ))
    grain_barns.append(GrainBarn(barn_no='3', barn_name=u'3号仓', grain_storehouse=grain_storehouses[0], lora_gateway=lora_gateways[0], high_limit=30, low_limit=20 ))
    grain_barns.append(GrainBarn(barn_no='4', barn_name=u'4号仓', grain_storehouse=grain_storehouses[0], lora_gateway=lora_gateways[0], high_limit=30, low_limit=20 ))
    grain_barns.append(GrainBarn(barn_no='5', barn_name=u'5号仓', grain_storehouse=grain_storehouses[0], lora_gateway=lora_gateways[0], high_limit=30, low_limit=20 ))
    grain_barns.append(GrainBarn(barn_no='6', barn_name=u'6号仓', grain_storehouse=grain_storehouses[0], lora_gateway=lora_gateways[0], high_limit=30, low_limit=20 ))
    grain_barns.append(GrainBarn(barn_no='7', barn_name=u'7号仓', grain_storehouse=grain_storehouses[0], lora_gateway=lora_gateways[0], high_limit=30, low_limit=20 ))
    grain_barns.append(GrainBarn(barn_no='8', barn_name=u'8号仓', grain_storehouse=grain_storehouses[0], lora_gateway=lora_gateways[0], high_limit=30, low_limit=20 ))
    grain_barns.append(GrainBarn(barn_no='9', barn_name=u'1号仓', grain_storehouse=grain_storehouses[0], lora_gateway=lora_gateways[0], high_limit=30, low_limit=20 ))
    grain_barns.append(GrainBarn(barn_no='10', barn_name=u'10号仓', grain_storehouse=grain_storehouses[0], lora_gateway=lora_gateways[0], high_limit=30, low_limit=20 ))
    grain_barns.append(GrainBarn(barn_no='11', barn_name=u'2号仓', grain_storehouse=grain_storehouses[0], lora_gateway=lora_gateways[0], high_limit=30, low_limit=20 ))
    grain_barns.append(GrainBarn(barn_no='12', barn_name=u'12号仓', grain_storehouse=grain_storehouses[0], lora_gateway=lora_gateways[0], high_limit=30, low_limit=20 ))

    for i in range(len(grain_barns)):
        db.session.add(grain_barns[i])

    db.session.commit()

except Exception, e:
    log.error("Creating barns: %s", e)
    db.session.rollback()


try:
    power_ios = list()
    power_ios.append(PowerIo(addr='1', name=u'9号仓配电箱1#'))
    power_ios.append(PowerIo(addr='2', name=u'9号仓配电箱2#'))

    db.session.add(power_ios[0])
    db.session.add(power_ios[1])

    db.session.commit()
except Exception, e:
    log.error("Creating power_io: %s", e)
    db.session.rollback()


try:
    tianshuo_485s = list()
    tianshuo_485s.append(TianshuoRs485(addr='1', name=u'11号仓1#空调'))
    tianshuo_485s.append(TianshuoRs485(addr='2', name=u'11号仓2#空调'))

    db.session.add(tianshuo_485s[0])
    db.session.add(tianshuo_485s[1])

    db.session.commit()
except Exception, e:
    log.error("Creating tianshuo_485: %s", e)
    db.session.rollback()


try:
    lora_nodes = list()
    lora_nodes.append(LoraNode(node_addr='1', grain_storehouse=grain_storehouses[0], lora_gateway=lora_gateways[0], grain_barn=grain_barns[0], power_io=power_ios[0]))
    lora_nodes.append(LoraNode(node_addr='2', grain_storehouse=grain_storehouses[0], lora_gateway=lora_gateways[0], grain_barn=grain_barns[0], power_io=power_ios[0]))
    lora_nodes.append(LoraNode(node_addr='3', grain_storehouse=grain_storehouses[0], lora_gateway=lora_gateways[0], grain_barn=grain_barns[0], power_io=power_ios[1]))
    lora_nodes.append(LoraNode(node_addr='4', grain_storehouse=grain_storehouses[0], lora_gateway=lora_gateways[0], grain_barn=grain_barns[0], power_io=power_ios[1]))

    db.session.add(lora_nodes[0])
    db.session.add(lora_nodes[1])
    db.session.add(lora_nodes[2])
    db.session.add(lora_nodes[3])

    db.session.commit()
except Exception, e:
    log.error("Creating lora_node: %s", e)
    db.session.rollback()

def today():
    return datetime.datetime.now()


for i in range(1, 100):
    gt = GrainTemp()
    gt.grain_storehouse = grain_storehouses[0]
    gt.lora_gateway = lora_gateways[0]
    gt.grain_barn = grain_barns[0]
    gt.lora_node = lora_nodes[random.randint(0, 3)]
    gt.switch = False
    gt.temp1 = random.randrange(20, 30)
    gt.temp2 = random.randrange(20, 30)
    gt.temp3 = random.randrange(20, 30)
    gt.battery_vol = random.randint(1, 3)
    gt.datetime = today()

    db.session.add(gt)
    try:
        db.session.commit()
        print "inserted", gt
    except Exception, e:
        log.error("Creating GrainTemp: %s", e)
        db.session.rollback()


try:
    power_io_rs485_funcs = list()
    power_io_rs485_funcs.append(PowerIoRs485Func(function_name='open_channel_1', function_code=5, start_at_reg_high=0, start_at_reg_low=16, num_of_reg_high=255, num_of_reg_low=0))
    power_io_rs485_funcs.append(PowerIoRs485Func(function_name='close_channel_1', function_code=5, start_at_reg_high=0, start_at_reg_low=16, num_of_reg_high=0, num_of_reg_low=0))

    # power_1_close = '010500100000CC0F'
    # power_1_open = '01050010FF008DFF'

    db.session.add(power_io_rs485_funcs[0])
    db.session.add(power_io_rs485_funcs[1])

    db.session.commit()
except Exception, e:
    log.error("Creating power_io_rs485_funcs: %s", e)
    db.session.rollback()


try:
    tianshuo_rs485_funcs = list()
    tianshuo_rs485_funcs.append(TianshuoRs485Func(function_name='off_and_cold', function_code=6, start_at_reg_high=0, start_at_reg_low=0, num_of_reg_high=0, num_of_reg_low=1))
    tianshuo_rs485_funcs.append(TianshuoRs485Func(function_name='on_and_cold', function_code=6, start_at_reg_high=0, start_at_reg_low=0, num_of_reg_high=0, num_of_reg_low=9))

    # off_cold = '010600000001'
    # on_cold = '010600000009'

    db.session.add(tianshuo_rs485_funcs[0])
    db.session.add(tianshuo_rs485_funcs[1])

    db.session.commit()
except Exception, e:
    log.error("Creating tianshuo_rs485_funcs: %s", e)
    db.session.rollback()


for i in range(1, 13):
    mq_func = NodeMqttTransFunc()
    mq_func.gateway_addr = '001'
    mq_func.node_addr = bitstring.pack('uint:13', i).bin
    mq_func.trans_direct = '1'
    mq_func.func_code = '0010001'
    mq_func.wind_direct = '00'
    mq_func.wind_speed = '11'
    mq_func.model = '1000111001'
    mq_func.on_off = '00'
    mq_func.work_mode = '001'
    mq_func.temp = '10100'

    db.session.add(mq_func)
    try:
        db.session.commit()
        print "inserted", mq_func
    except Exception, e:
        log.error("Creating NodeMqttTransFunc: %s", e)
        db.session.rollback()


try:
    alarm_level_setting = list()
    alarm_level_setting.append(AlarmLevelSetting(warning=35, error=45))

    db.session.add(alarm_level_setting[0])

    db.session.commit()
except Exception, e:
    log.error("Creating alarm_level_setting: %s", e)
    db.session.rollback()



