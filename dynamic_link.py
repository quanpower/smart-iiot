# -*- coding:utf-8 -*-


from app import db
from app.models import LoraGateway, LoraNode, GrainBarn, AlarmLevelSetting, PowerIoRs485Func, PowerIo, NodeMqttTransFunc, GrainTemp, GrainStorehouse
from sqlalchemy import and_
from utils import rs485_socket_send, calc_modus_hex_str_to_send, crc_func, str2hexstr, calc
from mqtt_publisher import mqtt_pub_air_con,transmitMQTT
import bitstring
from bitstring import BitArray, BitStream
import struct
import time



# FIRE_ALARM_HIGH_LIMIT = 40
# AIR_CONDITIONER_HIGH_LIMIT = 40
# AIR_CONDITIONER_LOW_LIMIT = 30



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
    
    str_bin = BitStream('0b' + str_origin)
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
    print(units, hex(crc))

    str_bytes=struct.pack('7B', units[0], units[1], units[2], units[3], units[4], units[5], crc)
    print(len(str_bytes))
    print(repr(str_bytes))

    transmitMQTT(str_bytes)

def dynamic_link():
    """
    control air-conditioner and electric power autoly
    """

    alarmLevel = db.session.query(AlarmLevelSetting.warning, AlarmLevelSetting.error).all()
    alarmLevelWarning = alarmLevel[0][0]
    alarmLevelError = alarmLevel[0][1]
    print('alarmLevelWarning', alarmLevelWarning)
    print('alarmLevelError', alarmLevelError)

    barns = db.session.query(GrainBarn.barn_no, GrainBarn.barn_name, GrainBarn.high_limit, GrainBarn.low_limit).join(GrainStorehouse, GrainStorehouse.id == GrainBarn.grain_storehouse_id).filter(GrainStorehouse.storehouse_no=='1').all()
    print("-------barns are---------:", barns)
    for i in range(len(barns)):
        barn = barns[i]
        print('---------------**********barn*********--------------', barn)
        nodes = db.session.query(LoraNode.node_addr).join(GrainBarn, GrainBarn.id == LoraNode.grain_barn_id).filter(GrainBarn.barn_no == barn[0]).all()
        print('nodes:', nodes)

        for j in range(len(nodes)):
            # todo: repalce geteway_addr
            node = nodes[j]
            print('---------------******node******--------------', node)
            temps = db.session.query(GrainTemp.temp1, GrainTemp.temp2, GrainTemp.temp3, GrainTemp.datetime, LoraGateway.gateway_addr,
                LoraNode.node_addr).join(LoraGateway, LoraGateway.id == GrainTemp.lora_gateway_id).join(LoraNode, 
                LoraNode.id == GrainTemp.lora_node_id).filter(and_(LoraGateway.gateway_addr == '1', LoraNode.node_addr == node[0])).order_by(
                GrainTemp.datetime.desc()).first()

            print('******temps******', temps)

            power_io_addr_query = db.session.query(PowerIo.addr).join(LoraNode, PowerIo.id == LoraNode.power_io_id).filter(LoraNode.node_addr == node[0]).all()
            # open first channel
            print('******power_io_addr******', power_io_addr_query)
            power_io_addr = power_io_addr_query[0][0]

            open_channel_1 = db.session.query(PowerIoRs485Func.function_code, PowerIoRs485Func.start_at_reg_high,
                PowerIoRs485Func.start_at_reg_low, PowerIoRs485Func.num_of_reg_high, PowerIoRs485Func.num_of_reg_low).filter(PowerIoRs485Func.function_name == 'open_channel_1').all()
            close_channel_1 = db.session.query(PowerIoRs485Func.function_code, PowerIoRs485Func.start_at_reg_high,
                PowerIoRs485Func.start_at_reg_low, PowerIoRs485Func.num_of_reg_high, PowerIoRs485Func.num_of_reg_low).filter(PowerIoRs485Func.function_name == 'close_channel_1').all()
            print('******open_channel_1******', open_channel_1)
            print('******close_channel_1******', close_channel_1)


            if temps:
                fireAlarmSenserTemp = max(temps[0], temps[1])
                airSenserTemp = temps[2]
                print('******fireAlarmSenserTemp******', fireAlarmSenserTemp)

                if fireAlarmSenserTemp > alarmLevelError:
                    # FireAlarm：disconnect switch
                    if power_io_addr:

                        address = int(power_io_addr)
                        function_code = open_channel_1[0][0]
                        start_at_reg_high = open_channel_1[0][1]
                        start_at_reg_low = open_channel_1[0][2]
                        num_of_reg_high = open_channel_1[0][3]
                        num_of_reg_low = open_channel_1[0][4]

                        output_hex = calc_modus_hex_str_to_send(address, function_code, start_at_reg_high, start_at_reg_low, num_of_reg_high, num_of_reg_low)
                        rs485_socket_send(output_hex)
                print('******node[0]******', node[0])

                mqtt_node_addr = bitstring.pack('uint:13', node[0]).bin

                print('-------mqtt_node_addr--------', mqtt_node_addr)



                node_mqtt_trans_func = db.session.query(NodeMqttTransFunc.gateway_addr, NodeMqttTransFunc.node_addr, NodeMqttTransFunc.trans_direct, NodeMqttTransFunc.func_code,
                    NodeMqttTransFunc.wind_direct, NodeMqttTransFunc.wind_speed, NodeMqttTransFunc.model, NodeMqttTransFunc.on_off,
                    NodeMqttTransFunc.work_mode, NodeMqttTransFunc.temp).filter(NodeMqttTransFunc.node_addr == mqtt_node_addr).all()

                print('******node_mqtt_trans_func******', node_mqtt_trans_func)

                if node_mqtt_trans_func:
                    airSenserTempHighLimit = barn[2]
                    airSenserTempLowLimit = barn[3]
                    print('airSenserTempHighLimit', airSenserTempHighLimit)
                    print('airSenserTempLowLimit', airSenserTempLowLimit)

                    if airSenserTemp > airSenserTempHighLimit:
                        print('temp higher than highlimit, transmit ')
                        on_off = '01'
                        mqtt_auto_control_air(node_mqtt_trans_func, on_off)
                    elif airSenserTemp < airSenserTempLowLimit:
                        print('temp lower than highlimit, transmit ')
                        on_off = '00'
                        mqtt_auto_control_air(node_mqtt_trans_func, on_off)

if __name__ == '__main__':
    while True:
        dynamic_link()
        time.sleep(60)