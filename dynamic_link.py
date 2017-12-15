# -*- coding:utf-8 -*-

from app.models import LoraGateway, LoraNode, GrainBarn, AlarmLevelSetting, PowerIo, NodeMqttTransFunc, GrainTemp, GrainStorehouse, RelayCurrentRs485Func
from sqlalchemy import create_engine, and_
from utils import calc_modus_hex_str_to_send, crc_func, str2hexstr, calc
from mqtt_publisher import mqtt_pub_air_con, transmitMQTT, mqtt_auto_control_air
from mqtt_passthrough_publisher import transmitMQTT_byte
import bitstring
from bitstring import BitArray, BitStream
import struct
import time
import datetime

from sqlalchemy.orm import sessionmaker

# 初始化数据库连接:
engine = create_engine('sqlite:///data.sqlite')
# 创建DBSession类型:
Session = sessionmaker(bind=engine)
db_session=Session()


def dynamic_link():
    """
    control air-conditioner and electric power autoly
    """

    alarmLevel = db_session.query(AlarmLevelSetting.warning, AlarmLevelSetting.error).all()
    alarmLevelWarning = alarmLevel[0][0]
    alarmLevelError = alarmLevel[0][1]

    print('\n' * 5)
    print('------------dynamic_link beginning-------------')
    print('\n' * 5)

    print('alarmLevelWarning', alarmLevelWarning)
    print('alarmLevelError', alarmLevelError)

    barns = db_session.query(GrainBarn.barn_no, GrainBarn.barn_name, GrainBarn.high_limit, GrainBarn.low_limit).join(GrainStorehouse, GrainStorehouse.id == GrainBarn.grain_storehouse_id).filter(GrainStorehouse.storehouse_no=='1').all()
    print("-------barns are---------:", barns)
    for i in range(len(barns)):
        barn = barns[i]
        print('---------------**********barn*********--------------\n', barn)
        nodes = db_session.query(LoraNode.node_addr).join(GrainBarn, GrainBarn.id == LoraNode.grain_barn_id).filter(GrainBarn.barn_no == barn[0]).all()
        print('nodes:\n', nodes)

        auto_nodes = db_session.query(LoraNode.node_addr).join(GrainBarn, GrainBarn.id == LoraNode.grain_barn_id).filter(and_(LoraNode.auto_manual == 'auto', GrainBarn.barn_no == barn[0])).all()
        print('auto_nodes\n', auto_nodes)
        
        for j in range(len(auto_nodes)):
            time.sleep(5)

            auto_node = auto_nodes[j]
            print('---------------******auto_node******--------------:\n', auto_node)

            temps = db_session.query(GrainTemp.temp1, GrainTemp.temp2, GrainTemp.temp3, GrainTemp.datetime, LoraGateway.gateway_addr,
                LoraNode.node_addr).join(LoraGateway, LoraGateway.id == GrainTemp.lora_gateway_id).join(LoraNode, 
                LoraNode.id == GrainTemp.lora_node_id).filter(and_(LoraGateway.gateway_addr == '1', LoraNode.node_addr == auto_node[0])).order_by(
                GrainTemp.datetime.desc()).first()

            print('******temps******\n', temps)

            # auto power on/off air-conditoner
            if temps:
                fireAlarmSenserTemp = max(temps[0], temps[1])
                airSenserTemp = temps[2]

                print('-------airSenserTemp--------')
                print(airSenserTemp)

                print('******auto_node[0] in auto model******', auto_node[0])

                mqtt_node_addr = bitstring.pack('uint:13', auto_node[0]).bin
                print('-------auto_node_mqtt_node_addr--------', mqtt_node_addr)

                node_mqtt_trans_func = db_session.query(NodeMqttTransFunc.gateway_addr, NodeMqttTransFunc.node_addr, NodeMqttTransFunc.trans_direct, NodeMqttTransFunc.func_code,
                    NodeMqttTransFunc.wind_direct, NodeMqttTransFunc.wind_speed, NodeMqttTransFunc.model, NodeMqttTransFunc.on_off,
                    NodeMqttTransFunc.work_mode, NodeMqttTransFunc.temp).filter(NodeMqttTransFunc.node_addr == mqtt_node_addr).all()

                print('******node_mqtt_trans_func******\n', node_mqtt_trans_func)

                if node_mqtt_trans_func:
                    airSenserTempHighLimit = barn[2]
                    airSenserTempLowLimit = barn[3]
                    print('----airSenserTempHighLimit-----', airSenserTempHighLimit)
                    print('----airSenserTempLowLimit------', airSenserTempLowLimit)

                    if airSenserTemp > airSenserTempHighLimit:
                        print('temp higher than highlimit, transmit ')
                        on_off = '01'
                        mqtt_auto_control_air(node_mqtt_trans_func, on_off)
                    elif airSenserTemp < airSenserTempLowLimit:
                        print('temp lower than lowlimit, transmit ')
                        on_off = '00'
                        mqtt_auto_control_air(node_mqtt_trans_func, on_off)


        print('^^^^^^^^^^^^^' * 5)
        print('\n' * 3 )
        print('-----------in all normal nodes cicle---------------')
        for k in range(len(nodes)):
            # todo: repalce geteway_addr
            node = nodes[k]
            print('\n' * 3 )
            print('---------------******node circle begin******--------------', node)
            temps = db_session.query(GrainTemp.temp1, GrainTemp.temp2, GrainTemp.temp3, GrainTemp.datetime, LoraGateway.gateway_addr,
                LoraNode.node_addr).join(LoraGateway, LoraGateway.id == GrainTemp.lora_gateway_id).join(LoraNode, 
                LoraNode.id == GrainTemp.lora_node_id).filter(and_(LoraGateway.gateway_addr == '1', LoraNode.node_addr == node[0])).order_by(
                GrainTemp.datetime.desc()).first()

            print('******temps******\n', temps)

            power_io_addr_query = db_session.query(PowerIo.addr).join(LoraNode, PowerIo.id == LoraNode.power_io_id).filter(LoraNode.node_addr == node[0]).all()
            # open first channel
            print('******power_io_addr******', power_io_addr_query)
            power_io_addr = power_io_addr_query[0][0]

            suck_func_code = db_session.query(RelayCurrentRs485Func.function_code).filter(
                RelayCurrentRs485Func.function_name == 'suck_func_code').first()
            

            print('\n' * 3)
            print('+++++++++++current daq+++++++++++++')
            # current daq
            current_daq_func_code = db_session.query(RelayCurrentRs485Func.function_code).filter(
                RelayCurrentRs485Func.function_name == 'current_A1_A2_func_code').first()
            


            transmitMQTT_byte(power_io_addr, current_daq_func_code[0])
            print('+++++++++++current daq+++++++++++++')
            print('\n' * 3)

            # cut off electric if fire alarm senser higher than HIGH LIMIT
            if temps:
                fireAlarmSenserTemp = max(temps[0], temps[1])
                airSenserTemp = temps[2]
                print('******fireAlarmSenserTemp******', fireAlarmSenserTemp)

                if fireAlarmSenserTemp > alarmLevelError:
                    # FireAlarm：disconnect switch
                    print("cut off power!")
                    print('suck_func_code:')
                    print(power_io_addr)
                    print(suck_func_code[0])

                    if power_io_addr and suck_func_code[0]:
                        print('----send mqtt to cut off!------')
                        transmitMQTT_byte(power_io_addr, suck_func_code[0])
                        time.sleep(3)

            # timing ON/OFF
            mqtt_node_addr = bitstring.pack('uint:13', node[0]).bin
            print('-------mqtt_node_addr--------', mqtt_node_addr)

            node_mqtt_trans_func = db_session.query(NodeMqttTransFunc.gateway_addr, NodeMqttTransFunc.node_addr, NodeMqttTransFunc.trans_direct, NodeMqttTransFunc.func_code,
                NodeMqttTransFunc.wind_direct, NodeMqttTransFunc.wind_speed, NodeMqttTransFunc.model, NodeMqttTransFunc.on_off,
                NodeMqttTransFunc.work_mode, NodeMqttTransFunc.temp).filter(NodeMqttTransFunc.node_addr == mqtt_node_addr).all()

            print('******node_mqtt_trans_func******', node_mqtt_trans_func)

            start_end_time = db_session.query(LoraNode.node_addr, LoraNode.auto_start_time, LoraNode.auto_end_time).filter(LoraNode.node_addr == node[0]).all()
            print('\n' * 3)
            print('*************' * 3)
            print('******auto-power-on-off ******')
            print('******start_end_time******', start_end_time)

            if node_mqtt_trans_func and start_end_time:
                auto_start_time = start_end_time[0][1]
                auto_end_time = start_end_time[0][2]

                time_now = datetime.datetime.now()
                if  time_now > auto_start_time and time_now < auto_start_time + datetime.timedelta(seconds=240):
                    print('auto start now!')
                    on_off = '01'
                    mqtt_auto_control_air(node_mqtt_trans_func, on_off)
                if time_now > auto_end_time and time_now < auto_end_time + datetime.timedelta(seconds=240):
                    print('auto end now!')
                    on_off = '00'
                    mqtt_auto_control_air(node_mqtt_trans_func, on_off)

            time.sleep(5)

if __name__ == '__main__':
    while True:
        dynamic_link()
