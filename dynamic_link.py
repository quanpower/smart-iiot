from app import db
from app.models import LoraGateway, LoraNode, GrainBarn, AlarmLevelSetting, PowerIoRs485Func, PowerIoRs485, NodeMqttTransFunc, GrainTemp, GrainStorehouse
from sqlalchemy import and_
from utils import rs485_socket_send,calc_modus_hex_str_to_send,crc_func
from mqtt_publisher import mqtt_pub_air_con,transmitMQTT
from bitstring import BitArray, BitStream

# FIRE_ALARM_HIGH_LIMIT = 40
# AIR_CONDITIONER_HIGH_LIMIT = 40
# AIR_CONDITIONER_LOW_LIMIT = 30


def electricControl(hex_str):
    rs485_socket_send(hex_str)

def mqtt_auto_control_air(node_mqtt_trans_func,on_off):

    gateway_addr = node_mqtt_trans_func[0][0]
    node_addr = node_mqtt_trans_func[0][1]
    trans_direct = node_mqtt_trans_func[0][2]
    func_code = node_mqtt_trans_func[0][3]
    wind_direct = node_mqtt_trans_func[0][4]
    wind_speed = node_mqtt_trans_func[0][5]
    model = node_mqtt_trans_func[0][6]
    work_mode = node_mqtt_trans_func[0][8]
    temp = node_mqtt_trans_func[0][9]
    
    str_origin = gateway_addr + node_addr + trans_direct + func_code
    + wind_direct + wind_speed + model + on_off + work_mode + temp
    
    str_bin = BitStream('0b' + str_origin)
    print('----str_bin------')
    print(str_bin)
    print('----len_str_bin------')
    print(len(str_bin))

    units = []
    for i in range(int(len(str_bin) / 8)):
        units.append(str_bin.read(8).uint)
    print('units',units)

    crc = crc_func(units)
    print('-------send-hex------')
    print(units,hex(crc))

    str_bytes=struct.pack('7B', units[0], units[1], units[2], units[3], units[4], units[5], crc)
    print(str_bytes)
    print(len(str_bytes))
    print(repr(str_bytes))

    transmitMQTT(str_bytes)

def dynamic_link():
    """
    control air-conditioner and electric power autoly
    """
    def return_color(max_abc):
        print('max_abc:', max_abc)
        if max_abc < 35:
            return "#64ea91"
        elif (35 <= max_abc) and (max_abc <= 50):
            return "#8fc9fb"
        else:
            return "#f69899"

    alarmLevel = db.session.query(AlarmLevelSetting.warning, AlarmLevelSetting.error).all()
    alarmLevelWarning = alarmLevel[0][0]
    alarmLevelError = alarmLevel[0][1]
    print('alarmLevelWarning', alarmLevelWarning)
    print('alarmLevelError', alarmLevelError)

    barns = db.session.query(GrainBarn.barn_no, GrainBarn.barn_name, GrainBarn.high_limit, GrainBarn.low_limit).join(GrainStorehouse, GrainStorehouse.id == GrainBarn.grain_storehouse_id).filter(GrainStorehouse.storehouse_no=='1').all()
    print("-------barns are---------:", barns)
    barn_temps = []
    for barn in barns:
        print('---------------barn--------------', barn)
        nodes = db.session.query(LoraNode.node_addr).join(GrainBarn, GrainBarn.id == LoraNode.grain_barn_id).filter(GrainBarn.barn_no == barn[0]).all()
        print('nodes:', nodes)
        max_temps = []
        for node in nodes:
            # todo: repalce geteway_addr
            print('******node******', node)
            temps = db.session.query(GrainTemp.temp1, GrainTemp.temp2, GrainTemp.temp3, LoraGateway.gateway_addr,
                LoraNode.node_addr).join(LoraGateway, LoraGateway.id == GrainTemp.lora_gateway_id).join(LoraNode, 
                LoraNode.id == GrainTemp.lora_node_id).filter(and_(LoraGateway.gateway_addr == '1', LoraNode.node_addr == node[0])).order_by(
                GrainTemp.datetime.desc()).first()

            power_io_addr = db.session.query(PowerIoRs485.io_addr).join(LoraNode, PowerIoRs485.id == LoraNode.power_io_rs485_id).filter(LoraNode.node_addr == node[0]).all()
            # open first channel
            open_1_channel = db.session.query(PowerIoRs485Func.function_code, PowerIoRs485Func.start_at_reg_high,
                PowerIoRs485Func.start_at_reg_low,PowerIoRs485Func.num_of_reg_high,PowerIoRs485Func.num_of_reg_low).filter(PowerIoRs485Func.function_name == 'open_1_channel').all()
            close_1_channel = db.session.query(PowerIoRs485Func.function_code, PowerIoRs485Func.start_at_reg_high,
                PowerIoRs485Func.start_at_reg_low,PowerIoRs485Func.num_of_reg_high,PowerIoRs485Func.num_of_reg_low).filter(PowerIoRs485Func.function_name == 'close_1_channel').all()

            print('temps', temps)
            if temps:
                fireAlarmSenserTemp = max(temps[0][0], temps[0][1])
                airSenserTemp = temps[0][2]

                node_mqtt_trans_func = db.session.query(NodeMqttTransFunc.gateway_addr,NodeMqttTransFunc.node_addr,NodeMqttTransFunc.trans_direct,NodeMqttTransFunc.func_code,
                    NodeMqttTransFunc.wind_direct, NodeMqttTransFunc.wind_speed, NodeMqttTransFunc.on_off, 
                    NodeMqttTransFunc.work_mode,NodeMqttTransFunc.temp).filter(NodeMqttTransFunc.node_addr == node[0]).first()



                if fireAlarmSenserTemp > alarmLevelError:
                    # todo: select address from db

                    address = int(power_io_addr)
                    function_code = open_1_channel[0]
                    start_at_reg_high = open_1_channel[1]
                    start_at_reg_low = open_1_channel[2]
                    num_of_reg_high = open_1_channel[3]
                    num_of_reg_low = open_1_channel[4]
                    output_hex = calc_modus_hex_str_to_send(address,function_code,start_at_reg_high,start_at_reg_low,num_of_reg_high,num_of_reg_low)
                    electricControl(output_hex)

                if airSenserTemp > barn[1]:

                    print(barn[1])
                    print('temp higher than highlimit, transmit ')
                    on_off = '00'
                    mqtt_auto_control_air(node_mqtt_trans_func,on_off)


                elif airSenserTemp < barn[2]:

                    print(barn[1])
                    print('temp lower than highlimit, transmit ')
                    on_off = '01'
                    mqtt_auto_control_air(node_mqtt_trans_func,on_off)

            else:
                max_temps = []
        print('max_temps:', max_temps)

        if max_temps:
            max_temp_value = max(a['max_temp'] for a in max_temps)
        else:
            max_temp_value = 0

        barn_temps_dic = {"icon": "home", "color": return_color(max_temp_value), "title": barn[1], "number": max_temp_value, "barnNo": barn[0]}
        barn_temps.append(barn_temps_dic)
    barn_dic = {"barns": barn_temps}
    # conc_dash_dic = {"concDash":[{"name":"1","status":1,"content":"上：25.7℃, 中：26.5℃, 下： 31℃","avatar":"http://dummyimage.com/48x48/f279aa/757575.png&text=1","date":"2017-08-19 23:38:45"},{"name":"White","status":2,"content":"上：25.7℃, 中：26.5℃, 下： 31℃","avatar":"http://dummyimage.com/48x48/79cdf2/757575.png&text=W","date":"2017-04-22 14:17:06"},{"name":"Martin","status":3,"content":"上：25.7℃, 中：26.5℃, 下： 31℃","avatar":"http://dummyimage.com/48x48/f1f279/757575.png&text=M","date":"2017-05-07 04:29:13"},{"name":"Johnson","status":1,"content":"上：25.7℃, 中：26.5℃, 下： 31℃","avatar":"http://dummyimage.com/48x48/d079f2/757575.png&text=J","date":"2017-01-14 02:38:37"},{"name":"Jones","status":2,"content":"上：25.7℃, 中：26.5℃, 下： 31℃","avatar":"http://dummyimage.com/48x48/79f2ac/757575.png&text=J","date":"2017-07-08 20:05:50"}]}
    # conc_dash_dic = {"concDash":statuses}
    print("barns", barn_dic)

    # barn_dic = {"barns": [{"icon": "home", "color": "#64ea91", "title": "1haocang", "number": 27.1}, {"icon": "home", "color": "#8fc9fb", "title": "2haocang", "number": 27.5}, {"icon": "home", "color": "#d897eb", "title": "3haocang", "number": 31}, {"icon": "home", "color": "#f69899", "title": "4haocang", "number": 32}, {"icon": "home", "color": "#64ea91", "title": "5haocang", "number": 27.1}, {"icon": "home", "color": "#8fc9fb", "title": "6haocang", "number": 27.5}, {"icon": "home", "color": "#d897eb", "title": "7haocang", "number": 31}, {"icon": "home", "color": "#f69899", "title": "8haocang", "number": 32}]}
    return barn_dic