from flasgger import Swagger, swag_from
from flask import Flask, redirect, url_for, request, jsonify, make_response
from flask_restful import reqparse, abort, Api, Resource
from app import db
from app.models import User, GrainTemp, LoraGateway, LoraNode, GrainBarn, PowerIo, GrainStorehouse, NodeMqttTransFunc, RelayCurrentRs485Func, AlarmStatus, AlarmLevelSetting
from sqlalchemy import and_
import json
import random
import datetime, time
from utils import random_color, index_color, calc, str2hexstr, calc_modus_hex_str_to_send
from rs485_socket import rs485_socket_send
from mqtt_publisher import mqtt_pub_air_con, transmitMQTT, mqtt_auto_control_air
from mqtt_passthrough_publisher import transmitMQTT_byte

import bitstring
import json
import urllib
from app.email import send_email


# api = Api(app)
#
# swagger = Swagger(app)


class Menus(Resource):
    def get(self):
        menus = [
            {
                'id': '1',
                'icon': 'laptop',
                'name': '粮仓列表',
                'route': '/grain',
            },
            {
                'id': '2',
                'bpid': '1',
                'name': '粮仓仪表板',
                'icon': 'bulb',
                'route': '/grain_dashboard/1',
            },
            {
                'id': '3',
                'bpid': '1',
                'name': '在线监测',
                'icon': 'bulb',
                'route': '/aircondetail/29',
            },
            {
                'id': '4',
                'bpid': '1',
                'name': '智能控温',
                'icon': 'code-o',
            },
            {
                'id': '41',
                'bpid': '4',
                'mpid': '4',
                'name': '壁挂空调控温',
                'icon': 'shopping-cart',
                'route': '/aircon_control/1',
            },
            {
                'id': '42',
                'bpid': '4',
                'mpid': '4',

                'name': '天硕空调开关控制',
                'icon': 'shopping-cart',
                'route': '/tianshuo_on_off',
            },
            {
                'id': '5',
                'bpid': '1',
                'name': '智能控电',
                'icon': 'shopping-cart',
                'route': '/fire_alarm/1',
            },
            {
                'id': '7',
                'bpid': '1',
                'name': '数据追溯',
                'icon': 'shopping-cart',
                'route': '/grain_history',
            },
            {
                'id': 'b',
                'bpid': '1',
                'name': '图表报告',
                'icon': 'code-o',
            },
            {
                'id': 'b1',
                'bpid': 'b',
                'mpid': 'b',
                'name': '线状图',
                'icon': 'line-chart',
                'route': '/chart/lineChart',
            },
            {
                'id': 'b2',
                'bpid': 'b',
                'mpid': 'b',
                'name': '柱状图',
                'icon': 'bar-chart',
                'route': '/chart/barChart',
            },
            {
                'id': 'b3',
                'bpid': 'b',
                'mpid': 'b',
                'name': '面积图',
                'icon': 'area-chart',
                'route': '/chart/areaChart',
            }, {
                'id': '8',
                'bpid': '1',
                'name': '用户管理',
                'icon': 'user',
                'route': '/user',
            },
            {
                'id': '81',
                'mpid': '-1',
                'bpid': '8',
                'name': 'User Detail',
                'route': '/user/:id',
            },
            {
                'id': 'c',
                'bpid': '1',
                'name': '系统设置',
                'icon': 'setting',
            },
            {
                'id': 'c1',
                'bpid': 'c',
                'mpid': 'c',
                'name': '仓房设置',
                'route': '/setting/storehouse_setting',
            },
            {
                'id': 'c11',
                'bpid': 'c1',
                'mpid': 'c1',
                'name': '仓号设置',
                'route': '/setting/storehouse_setting/navigation1',
            },
            {
                'id': 'c2',
                'bpid': 'c',
                'mpid': 'c',
                'name': '空调设置',
                'route': '/setting/airconditoner_setting',
            },
            {
                'id': 'c21',
                'bpid': 'c2',
                'mpid': 'c2',
                'name': '时间/上下限设置',
                'route': '/setting/airconditoner_setting/start_end_time/1',
            },
            {
                'id': 'c22',
                'bpid': 'c2',
                'mpid': 'c2',
                'name': '天硕空调设置',
                'route': '/setting/airconditoner_setting/tianshuo_setting/1',
            },
            # {
            #     'id': '9',
            #     'bpid': '1',
            #     'name': 'Request',
            #     'icon': 'api',
            #     'route': '/request',
            # },
            # {
            #     'id': 'a',
            #     'bpid': '1',
            #     'name': 'UI Element',
            #     'icon': 'camera-o',
            # },
            # {
            #     'id': 'a1',
            #     'bpid': 'a',
            #     'mpid': 'a',
            #     'name': 'IconFont',
            #     'icon': 'heart-o',
            #     'route': '/UIElement/iconfont',
            # },
            # {
            #     'id': 'a2',
            #     'bpid': 'a',
            #     'mpid': 'a',
            #     'name': 'DataTable',
            #     'icon': 'database',
            #     'route': '/UIElement/dataTable',
            # },
            # {
            #     'id': 'a3',
            #     'bpid': 'a',
            #     'mpid': 'a',
            #     'name': 'DropOption',
            #     'icon': 'bars',
            #     'route': '/UIElement/dropOption',
            # },
            # {
            #     'id': 'a4',
            #     'bpid': 'a',
            #     'mpid': 'a',
            #     'name': 'Search',
            #     'icon': 'search',
            #     'route': '/UIElement/search',
            # },
            # {
            #     'id': 'a5',
            #     'bpid': 'a',
            #     'mpid': 'a',
            #     'name': 'Editor',
            #     'icon': 'edit',
            #     'route': '/UIElement/editor',
            # },
            # {
            #     'id': 'a6',
            #     'bpid': 'a',
            #     'mpid': 'a',
            #     'name': 'layer (Function)',
            #     'icon': 'credit-card',
            #     'route': '/UIElement/layer',
            # },
        ]
        return menus

    def delete(self):
        pass

    def put(self):
        pass


class Barns(Resource):
    def get(self):

        alarmLevel = db.session.query(AlarmLevelSetting.warning, AlarmLevelSetting.error).all()
        alarmLevelWarning = alarmLevel[0][0]
        alarmLevelError = alarmLevel[0][1]

        def return_color(max_abc):
            if max_abc < alarmLevelWarning:
                return "#64ea91"
            elif (alarmLevelWarning <= max_abc) and (max_abc <= alarmLevelError):
                return "#ffff00"
            else:
                return "#ff0000"

        barns = db.session.query(GrainBarn.barn_no, GrainBarn.barn_name).join(GrainStorehouse,
            GrainStorehouse.id == GrainBarn.grain_storehouse_id).filter(
            GrainStorehouse.storehouse_no == '1').all()
        print("-------barns are---------:", barns)
        barn_temps = []
        for barn in barns:
            print('---------------barn--------------', barn)
            nodes = db.session.query(LoraNode.node_addr).join(GrainBarn, GrainBarn.id == LoraNode.grain_barn_id).filter(
                GrainBarn.barn_no == barn[0]).all()
            print('nodes:', nodes)
            max_temps = []
            for node in nodes:
                print('******node******', node)
                temps = db.session.query(GrainTemp.temp1, GrainTemp.temp2, GrainTemp.temp3, LoraGateway.gateway_addr,
                        LoraNode.node_addr).join(LoraGateway,LoraGateway.id == GrainTemp.lora_gateway_id).join(LoraNode,LoraNode.id == GrainTemp.lora_node_id).filter(
                        and_(LoraGateway.gateway_addr == '1', LoraNode.node_addr == node[0])).order_by(
                        GrainTemp.datetime.desc()).all()

                # print('temps', temps)
                if temps:
                    max_temp = max(temps[0][0], temps[0][1], temps[0][2])
                    # print('max_temp', max_temp)

                    max_temp_dic = {"max_temp": max_temp}
                    max_temps.append(max_temp_dic)
                else:
                    max_temps = []
            # print('max_temps:', max_temps)

            if max_temps:
                max_temp_value = max(a['max_temp'] for a in max_temps)
            else:
                max_temp_value = 0
            barn_temps_dic = {"icon": "home", "color": return_color(max_temp_value), "title": barn[1],
                              "number": max_temp_value, "barnNo": barn[0]}
            barn_temps.append(barn_temps_dic)
        barn_dic = {"barns": barn_temps}
        # print("barns", barn_dic)

        return barn_dic

    def delete(self):
        pass

    def put(self):
        pass


class AllBarns(Resource):
    def get(self):
        pass

    def delete(self):
        pass

    def put(self):
        pass

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('userID', type=int)
        parser.add_argument('username', type=str)

        args = parser.parse_args()

        print(args)
        userID = args['userID']
        username = args['username']

        storehouse_value_lable = {'value': '1', 'label': '福州库'}

        barns = db.session.query(GrainBarn.barn_no, GrainBarn.barn_name).join(GrainStorehouse,
        GrainStorehouse.id == GrainBarn.grain_storehouse_id).filter(GrainStorehouse.storehouse_no == '1').all()
        print("-------barns are---------:", barns)

        barn_children = []
        for i in range(len(barns)):
            barn=barns[i]
            print('---------------barn--------------', barn)
            user_owned_barns = db.session.query(User.owned_barns).filter(User.id == userID).all()
            user_owned_barns_text = user_owned_barns[0][0]
            print(user_owned_barns_text)
            user_owned_barns_list = user_owned_barns_text.split(',')
            print(user_owned_barns_list)
            
            if barn[0] in user_owned_barns_list:
                disabled = False
            else:
                disabled = True

            barn_value_label = {'value':barn[0], 'label':barn[1] ,'disabled':disabled}
            barn_children.append(barn_value_label)
        storehouse_value_lable['children'] = barn_children
        all_barns_list = [storehouse_value_lable]

        print('------all_barns_list-------')
        print(all_barns_list)

        return all_barns_list


class AllNodes(Resource):
    def get(self):

        storehouse_value_lable = {'value': '1', 'label': '福州库'}

        barns = db.session.query(GrainBarn.barn_no, GrainBarn.barn_name).join(GrainStorehouse,
        GrainStorehouse.id == GrainBarn.grain_storehouse_id).filter(GrainStorehouse.storehouse_no == '1').all()
        print("-------barns are---------:", barns)

        barn_children = []
        for i in range(len(barns)):
            barn = barns[i]
            print('---------------barn--------------', barn)
            barn_value_label = {'value':barn[0], 'label':barn[1]}
            nodes = db.session.query(LoraNode.node_addr, LoraNode.node_name).join(GrainBarn, GrainBarn.id == LoraNode.grain_barn_id).filter(
                GrainBarn.barn_no == barn[0]).all()
            print('nodes:', nodes)

            node_children = []
            for j in range(len(nodes)):
                node = nodes[j]
                print('******node******', node)
                node_children.append({'value':node[0], 'label':node[1]})
                # node_children.append({'value':node[0], 'label':node[1]+'({0}号节点)'.format(node[0])})

            barn_children.append(barn_value_label)

            barn_value_label['children'] = node_children
        storehouse_value_lable['children'] = barn_children

        all_nodes_list = [storehouse_value_lable]

        print('------all_nodes_list-------')
        print(all_nodes_list)

        return all_nodes_list

    def delete(self):
        pass

    def put(self):
        pass


class AirConRealtimeTemp(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('gatewayAddr', type=str)
        parser.add_argument('nodeAddr', type=str)

        args = parser.parse_args()

        print('-----realtimetemp args-----', args)

        gatewayAddr = args['gatewayAddr']
        nodeAddr = args['nodeAddr']

        print(gatewayAddr)
        print(nodeAddr)

        temps = db.session.query(GrainTemp.temp1, GrainTemp.temp2, GrainTemp.temp3, GrainTemp.battery_vol).join(
            LoraNode, LoraNode.id == GrainTemp.lora_node_id).join(
            LoraGateway, LoraGateway.id == GrainTemp.lora_gateway_id).filter(
            and_(LoraNode.node_addr == nodeAddr, LoraGateway.gateway_addr == gatewayAddr)).order_by(
            GrainTemp.datetime.desc()).first()

        print("temps:", temps)

        if len(temps) > 0:
            air_con_realtime_temp_dic = {
            "airConRealtimeTemp": [{"icon": "bulb", "color": "#64ea91", "title": "插座", "number": temps[0]},
                                   {"icon": "bulb", "color": "#8fc9fb", "title": "空调", "number": temps[1]},
                                   {"icon": "bulb", "color": "#d897eb", "title": "仓温", "number": temps[2]},
                                   {"icon": "message", "color": "#f69899", "title": "电池", "number": temps[3]}]}
        else:
            air_con_realtime_temp_dic = {}
        return air_con_realtime_temp_dic

    def delete(self):
        pass

    def put(self):
        pass


class AirConTemps(Resource):
    '''
        get the lates 10 temps.
    '''

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('gatewayAddr', type=str)
        parser.add_argument('nodeAddr', type=str)

        args = parser.parse_args()

        print('-------aircontemps args---------', args)

        gatewayAddr = args['gatewayAddr']
        nodeAddr = args['nodeAddr']

        temp_records = db.session.query(GrainTemp.temp1, GrainTemp.temp2, GrainTemp.temp3, GrainTemp.datetime).join(
            LoraNode, LoraNode.id == GrainTemp.lora_node_id).join(
            LoraGateway, LoraGateway.id == GrainTemp.lora_gateway_id).filter(
            and_(LoraNode.node_addr == nodeAddr, LoraGateway.gateway_addr == gatewayAddr)).order_by(
            GrainTemp.datetime.desc()).limit(10).all()

        temp_log = []
        for i in range(len(temp_records)):
            temp_log.append({"时间": temp_records[i][3].strftime("%Y-%m-%d %H:%M:%S"), "温度1": temp_records[i][0],
                             "温度2": temp_records[i][1], "温度3": temp_records[i][2]})

        temps_reverse = temp_log[::-1]
        print('------------temps_reverse--------------')
        # print(temps_reverse)

        temps_dict = {"airConTemps": temps_reverse}
        return temps_dict

    def delete(self):
        pass

    def put(self):
        pass


class AirConTempRecord(Resource):
    '''
        get the temp records by the input datetime. %H:%M:S%
    '''

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('gateway_addr', type=str)
        parser.add_argument('node_addr', type=str)
        parser.add_argument('start_time', type=str)
        parser.add_argument('end_time', type=str)

        args = parser.parse_args()

        print('--------AirConTempRecord-------', args)

        gatewayAddr = args['gateway_addr']
        nodeAddr = args['node_addr']
        startTime = datetime.datetime.strptime(args['start_time'], "%Y-%m-%d %H:%M:%S")
        endTime = datetime.datetime.strptime(args['end_time'], "%Y-%m-%d %H:%M:%S")

        print(startTime)
        print(endTime)

        temp_records = db.session.query(GrainTemp.temp1, GrainTemp.temp2, GrainTemp.temp3, GrainTemp.datetime).join(
            LoraNode, LoraNode.id == GrainTemp.lora_node_id).join(
            LoraGateway, LoraGateway.id == GrainTemp.lora_gateway_id).filter(
            and_(LoraNode.node_addr == nodeAddr, LoraGateway.gateway_addr == gatewayAddr,
                 GrainTemp.datetime.between(startTime, endTime))).order_by(
            GrainTemp.datetime.desc()).all()
        # print('*********temp_records*************', temp_records)

        temp_log = []
        for i in range(len(temp_records)):
            temp_log.append(
                {"key": i, "time": temp_records[i][3].strftime("%Y-%m-%d %H:%M:%S"), "Temp1": temp_records[i][0],
                 "Temp2": temp_records[i][1], "Temp3": temp_records[i][2]})

        temps_reverse = temp_log[::-1]
        print('------------temps_records--------------')
        # print(temps_reverse)

        temps_record_dict = {"airConTempRecord": temps_reverse}
        return temps_record_dict

    def delete(self):
        pass

    def put(self):
        pass


class AirConDashboard(Resource):
    def return_status(self, a, b, c):

        alarmLevel = db.session.query(AlarmLevelSetting.warning, AlarmLevelSetting.error).all()
        alarmLevelWarning = alarmLevel[0][0]
        alarmLevelError = alarmLevel[0][1]

        max_abc = max(a, b, c)
        # print('max_abc:', max_abc)
        if max_abc < alarmLevelWarning:
            return 1
        elif (alarmLevelWarning <= max_abc) and (max_abc <= alarmLevelError):
            return 2
        else:
            return 3

    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('gatewayAddr', type=str)
        parser.add_argument('barnNo', type=str)

        args = parser.parse_args()

        # print('-------AirConDashboard args---------', args)

        gatewayAddr = args['gatewayAddr']
        barnNo = args['barnNo']


        nodes = db.session.query(LoraNode.node_addr, LoraNode.node_name).join(GrainBarn, GrainBarn.id == LoraNode.grain_barn_id).filter(
            GrainBarn.barn_no == barnNo).order_by(LoraNode.node_name.asc()).all()
        # print("nodes are:", nodes)
        statuses = []
        for i in range(len(nodes)):
            node = nodes[i]
            # todo: repalce geteway_addr
            temps = db.session.query(GrainTemp.temp1, GrainTemp.temp2, GrainTemp.temp3, GrainTemp.datetime).join(
                LoraGateway, LoraGateway.id == GrainTemp.lora_gateway_id).join(LoraNode, LoraNode.id == GrainTemp.lora_node_id).filter(
                and_(LoraGateway.gateway_addr == gatewayAddr, LoraNode.node_addr == node[0])).order_by(
                GrainTemp.datetime.desc()).first()
            if temps:
                status = {"name": node[1] + "号空调", "status": self.return_status(temps[0], temps[1], temps[2]),
                          "content": "插座：{0}℃, 空调：{1}℃, 仓温：{2}℃".format(
                              str(temps[0]), str(temps[1]), str(temps[2])),
                          "avatar": "http://dummyimage.com/48x48/ffff00/000000.png&text={0}".format(node[1]),
                          # "avatar": "http://dummyimage.com/48x48/{0}/757575.png&text={1}".format(
                              # index_color(int(node[0]))[1:], node[1]),
                          "date": datetime.datetime.strftime(temps[3], "%Y-%m-%d %H:%M:%S"), "nodeAddr": node[0]}
                statuses.append(status)
            else:
                statuses = []
        air_con_dash_dic = {"airConDash": statuses}
        # print("air_con_dash_dic", air_con_dash_dic)
        return air_con_dash_dic

    def delete(self):
        pass

    def put(self):
        pass


class GrainHistory(Resource):
    def get(self):
        get_parser = reqparse.RequestParser()
        get_parser.add_argument('status', type=int, location='args', required=True)
        args = get_parser.parse_args()
        status = args.get('status')

        history_records = db.session.query(GrainTemp.grain_barn_id, GrainTemp.lora_gateway_id, LoraNode.node_addr,
                                           GrainTemp.temp1, GrainTemp.temp2, GrainTemp.temp3, GrainTemp.battery_vol,
                                           GrainTemp.datetime).join(LoraNode, LoraNode.id == GrainTemp.lora_node_id).order_by(
            GrainTemp.datetime.desc()).all()
        print('*********history_records*************', history_records)

        historys = []
        for i in range(len(history_records)):
            historys.append({"key": i, "status": 1, "grain_barn_id": "http://dummyimage.com/100x100/{0}/{1}.png&text={2}".format(
                index_color(history_records[i][0])[1:], '000000', str(history_records[i][0])),
                             "lora_gateway_id": history_records[i][1], "lora_node_addr": history_records[i][2],
                             "temp1": history_records[i][3], "temp2": history_records[i][4],
                             "temp3": history_records[i][5], "battery_vol": history_records[i][6],
                             "datetime": history_records[i][7].strftime("%Y-%m-%d %H:%M:%S")})

        # historys_reverse = historys[::-1]
        
        print('-------------historys-------------', historys)

        grain_history_dic = {'data': historys, "total": len(historys)}

        return grain_history_dic

    def delete(self):
        pass

    def put(self):
        pass


class AirConControl(Resource):
    def get(self):
        airconcontrol_dic = {'data': 'airconcontrol'}
        return airconcontrol_dic

    def delete(self):
        pass

    def put(self):
        pass

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('node_select', type=int)
        parser.add_argument('wind_directtion', type=int)
        parser.add_argument('wind_speed', type=int)
        parser.add_argument('working_model', type=int)
        parser.add_argument('temp_setting', type=int)
        parser.add_argument('switch', type=int)

        args = parser.parse_args()

        print(args)

        mqtt_pub_air_con(args)

        return args
                

class AirConControlItems(Resource):
    def get(self):
        airconcontrols_dic = {'data': 'airconcontrols'}
        return airconcontrols_dic

    def delete(self):
        pass

    def put(self):
        pass

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('barnNo', type=int)
        args = parser.parse_args()

        print(args)
        barnNo = args['barnNo']

        nodes = db.session.query(LoraNode.node_addr, LoraNode.node_name, LoraNode.current).join(GrainBarn, GrainBarn.id == LoraNode.grain_barn_id).filter(
                GrainBarn.barn_no == barnNo).all()
        print('nodes:', nodes)

        airconcontrol_items = []
        for j in range(len(nodes)):
            node = nodes[j]
            print('******node******', node)
            airconcontrol_item = {}
            airconcontrol_item['nodeAddr'] = node[0]
            airconcontrol_item['content'] = node[1] + '号空调开关控制'
            airconcontrol_item['name'] = node[1]
            airconcontrol_item['title '] = node[1] + '号空调'
            airconcontrol_item['avatar'] =  'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1506181543644&di=36ab98904965175769fb54fbd316cbe1&imgtype=0&src=http%3A%2F%2Fimg003.21cnimg.com%2Fphotos%2Falbum%2F20150207%2Fm600%2F562A7CBD05C2B187842FC10B831015B0.jpeg'
            # judge if air-condiontioner is working?
            if node[2] >= 0.5:
                node_status = {'color':'green', 'text':'运行中', 'current_value':node[2]}
            elif node[2]> 0.1 and node[2] < 0.5:
                node_status = {'color':'yellow', 'text':'待机中', 'current_value':node[2]}
            else:
                node_status = {'color':'red', 'text':'已停止', 'current_value':node[2]}
            airconcontrol_item['onoff_status'] = node_status
            airconcontrol_items.append(airconcontrol_item)
        print('----airconcontrol_items-----')
        print(airconcontrol_items)
        return airconcontrol_items


class AirConControlOnOff(Resource):
    def get(self):
        airconcontrol_dic = {'data': 'airconcontrol'}
        return airconcontrol_dic

    def delete(self):
        pass

    def put(self):
        pass

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('airconSwitch', type=str)
        parser.add_argument('nodeAddr', type=int)

        args = parser.parse_args()
        print(args)

        airconSwitch = args['airconSwitch']
        node_addr = args['nodeAddr']
        print('\n' * 5)
        print('-------------ready to send mqtt---------------')
        print('airconSwitch')
        print('node_addr')
        print(airconSwitch)
        print(node_addr)



        mqtt_node_addr = bitstring.pack('uint:13', node_addr).bin

        node_mqtt_trans_func = db.session.query(NodeMqttTransFunc.gateway_addr, NodeMqttTransFunc.node_addr,
                                                NodeMqttTransFunc.trans_direct, NodeMqttTransFunc.func_code,
                                                NodeMqttTransFunc.wind_direct, NodeMqttTransFunc.wind_speed,
                                                NodeMqttTransFunc.model, NodeMqttTransFunc.on_off,
                                                NodeMqttTransFunc.work_mode, NodeMqttTransFunc.temp).filter(
            NodeMqttTransFunc.node_addr == mqtt_node_addr).all()

        print('******node_mqtt_trans_func******', node_mqtt_trans_func)

        if node_mqtt_trans_func:

            if airconSwitch == '1':
                print('airconditoner switch to on!')
                on_off = '01'
                mqtt_auto_control_air(node_mqtt_trans_func, on_off)
            elif airconSwitch == '0':
                print('airconditoner switch to off!')
                on_off = '00'
                mqtt_auto_control_air(node_mqtt_trans_func, on_off)
            print('******node_mqtt_trans_end******')
            print('\n' * 5)

        return args


class AirConControls(Resource):
    def get(self):
        airconcontrols_dic = {'data': 'airconcontrols'}
        return airconcontrols_dic

    def delete(self, todo_id):
        pass

    def put(self, todo_id):
        pass

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('data', type=int, location='form')
        args = parser.parse_args()

        print(args)
        return args


class ElectricPowerControl(Resource):
    def get(self):
        pass

    def delete(self):
        pass

    def put(self):
        pass

    def post(self):


        parser = reqparse.RequestParser()
        parser.add_argument('powerSwitch', type=str)
        parser.add_argument('powerNo', type=str)

        args = parser.parse_args()
        # todo: replace it with dynamic_link's function
        print('\n' * 5)
        print('-------------power_controls_ready----------------')
        print(args)
        powerNo = args['powerNo']
        powerSwitch = args['powerSwitch']

        if powerSwitch == '1':
            print("switch on!")
            func_code = db.session.query(RelayCurrentRs485Func.function_code).filter(
                RelayCurrentRs485Func.function_name == 'release_func_code').first()
            transmitMQTT_byte(powerNo, func_code[0])

        else:
            print("switch off!")
            func_code = db.session.query(RelayCurrentRs485Func.function_code).filter(
                RelayCurrentRs485Func.function_name == 'suck_func_code').first()
            transmitMQTT_byte(powerNo, func_code[0])
        print('-------------power_controls_end----------------')
        print('\n' * 5)

        return args


class ElectricPowerControlItems(Resource):
    def get(self):
        pass

    def delete(self):
        pass

    def put(self):
        pass

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('barnNo', type=int)
        args = parser.parse_args()

        print(args)
        barnNo = args['barnNo']

        powerIos = db.session.query(PowerIo.addr, PowerIo.name).join(GrainBarn, GrainBarn.id == PowerIo.grain_barn_id).filter(
                GrainBarn.barn_no == barnNo).all()
        print('powerIos:', powerIos)


        electric_power_items = []
        for i in range(len(powerIos)):
            powerIo = powerIos[i]
            print('******powerIo******', powerIo)
            electric_power_item = {}
            electric_power_item['powerNo'] = powerIo[0]
            electric_power_item['content'] = powerIo[1] + '号配电箱开关控制'
            electric_power_item['name'] = powerIo[1]
            electric_power_item['title '] = powerIo[1] + '号配电箱'
            electric_power_item['avatar'] =  'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1506180316165&di=f56b4ef5671e23987359bc9b6f00dbb3&imgtype=0&src=http%3A%2F%2Fwww.dgjs123.com%2Fd%2Ffile%2F2015-05%2F124608p0eg0m07mz00ed7d.jpg'
     
            electric_power_items.append(electric_power_item)
        print('----electric_power_items-----')
        print(electric_power_items)
        return electric_power_items


class TianshuoOnOffControl(Resource):

    def get(self):

        power_controls_dic = {'data': 'power_controls'}

        return power_controls_dic

    def delete(self, todo_id):
        pass

    def put(self, todo_id):
        pass

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('tianshuoSwitch', type=str)
        parser.add_argument('tianshuoNo', type=int)

        args = parser.parse_args()
        print(args)

        tianshuoNo = args['tianshuoNo']
        tianshuoSwitch = args['tianshuoSwitch']

        if tianshuoSwitch == '1':
            output_hex = calc_modus_hex_str_to_send(tianshuoNo, 6, 0, 0, 0, 9)
            rs485_socket_send(output_hex)
            print("{0} switch on!".format(tianshuoNo))

        elif tianshuoSwitch == '0':
            output_hex = calc_modus_hex_str_to_send(tianshuoNo, 6, 0, 0, 0, 1)
            rs485_socket_send(output_hex)
            print("{0} switch off!".format(tianshuoNo))


class LoraNodeUpdate(Resource):

    def get(self):

        power_controls_dic = {'data': 'power_controls'}

        return power_controls_dic

    def delete(self, todo_id):
        pass

    def put(self, todo_id):
        pass

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nodeAddr', type=int)

        parser.add_argument('timeDelta', type=str)

        args = parser.parse_args()
        print(args)

        nodeAddr = args['nodeAddr']
        timeDelta = args['timeDelta']
        print('timeDelta', timeDelta)

        time_now = datetime.datetime.now()
        manual_start_time = time_now
        manual_end_time = time_now + datetime.timedelta(hours=float(timeDelta))

        lora_node = db.session.query(LoraNode).filter_by(node_addr=nodeAddr).first()
        lora_node.manual_start_time = manual_start_time
        lora_node.manual_end_time = manual_end_time

        try:
            db.session.commit()
            print("lora node updated!")
        except Exception as e:
            # log.error("Updating LoraNode: %s", e)
            print("Updating LoraNode: %s", e)
            db.session.rollback()

        return 'lora node start/end time updated!'


class BarnLoraNodeUpdate(Resource):

    def get(self):

        power_controls_dic = {'data': 'power_controls'}

        return power_controls_dic

    def delete(self, todo_id):
        pass

    def put(self, todo_id):
        pass

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('barnNo', type=str)

        parser.add_argument('timeDelta', type=str)

        args = parser.parse_args()
        print(args)

        barnNo = args['barnNo']
        timeDelta = args['timeDelta']
        print('timeDelta', timeDelta)

        nodes = db.session.query(LoraNode.node_addr).join(GrainBarn, GrainBarn.id == LoraNode.grain_barn_id).filter(
            GrainBarn.barn_no == barnNo).order_by(LoraNode.node_addr.asc()).all()
        print("nodes are:", nodes)

        time_now = datetime.datetime.now()
        manual_start_time = time_now
        manual_end_time = time_now + datetime.timedelta(hours=float(timeDelta))

        for node in nodes:
            nodeAddr = node[0]
            lora_node = db.session.query(LoraNode).filter_by(node_addr=nodeAddr).first()
            lora_node.manual_start_time = manual_start_time
            lora_node.manual_end_time = manual_end_time

        try:
            db.session.commit()
            print("lora node updated!")
        except Exception as e:
            # log.error("Updating LoraNode: %s", e)
            print("Updating LoraNode: %s", e)
            db.session.rollback()

        return 'lora node start/end time updated!'


class NodeAddressByBarnNo(Resource):

    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('airconSwitch', type=str)
        parser.add_argument('barnNo', type=str)

        args = parser.parse_args()
        print(args)

        barnNo = args['barnNo']
        airconSwitch = args['airconSwitch']

        nodes = db.session.query(LoraNode.node_addr).join(GrainBarn, GrainBarn.id == LoraNode.grain_barn_id).filter(
            GrainBarn.barn_no == barnNo).order_by(LoraNode.node_addr.asc()).all()
        print("nodes are:", nodes)
        power_controls_dic = {'data': 'power_controls'}

        return nodes

    def delete(self, todo_id):
        pass

    def put(self, todo_id):
        pass

    def post(self):
        pass


class AirConOnOffAllOneKey(Resource):
    # todo: use calc to auto generate hex_string

    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('airconSwitch', type=str)
        parser.add_argument('barnNo', type=str)

        args = parser.parse_args()
        print(args)

        barnNo = args['barnNo']
        airconSwitch = args['airconSwitch']

        nodes = db.session.query(LoraNode.node_addr).join(GrainBarn, GrainBarn.id == LoraNode.grain_barn_id).filter(
            GrainBarn.barn_no == barnNo).order_by(LoraNode.node_addr.asc()).all()
        print("nodes are:", nodes)
        if airconSwitch == '1':
            pass
        elif airconSwitch == '0':
            pass
        else:
            print('airconSwitch is :', airconSwitch)
        return nodes

    def delete(self, todo_id):
        pass

    def put(self, todo_id):
        pass

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('airconSwitch', type=str)
        parser.add_argument('barnNo', type=str)

        args = parser.parse_args()
        print(args)

        barnNo = args['barnNo']
        airconSwitch = args['airconSwitch']

        nodes = db.session.query(LoraNode.node_addr).join(GrainBarn, GrainBarn.id == LoraNode.grain_barn_id).filter(
            GrainBarn.barn_no == barnNo).order_by(LoraNode.node_addr.asc()).all()
        print("nodes are:", nodes)

        if airconSwitch == '1':
            for node in nodes:
                node_addr = node[0]
                print('node_addr is:', node_addr)
                mqtt_node_addr = bitstring.pack('uint:13', node_addr).bin

                node_mqtt_trans_func = db.session.query(NodeMqttTransFunc.gateway_addr, NodeMqttTransFunc.node_addr,
                                                        NodeMqttTransFunc.trans_direct, NodeMqttTransFunc.func_code,
                                                        NodeMqttTransFunc.wind_direct, NodeMqttTransFunc.wind_speed,
                                                        NodeMqttTransFunc.model, NodeMqttTransFunc.on_off,
                                                        NodeMqttTransFunc.work_mode, NodeMqttTransFunc.temp).filter(
                    NodeMqttTransFunc.node_addr == mqtt_node_addr).all()

                print('******node_mqtt_trans_func******', node_mqtt_trans_func)

                if node_mqtt_trans_func:
                    print('airconditoner switch to on!')
                    on_off = '01'
                    mqtt_auto_control_air(node_mqtt_trans_func, on_off)

        elif airconSwitch == '0':
            for node in nodes:
                node_addr = node[0]
                print('node_addr is:', node_addr)
                mqtt_node_addr = bitstring.pack('uint:13', node_addr).bin

                node_mqtt_trans_func = db.session.query(NodeMqttTransFunc.gateway_addr, NodeMqttTransFunc.node_addr,
                                                        NodeMqttTransFunc.trans_direct, NodeMqttTransFunc.func_code,
                                                        NodeMqttTransFunc.wind_direct, NodeMqttTransFunc.wind_speed,
                                                        NodeMqttTransFunc.model, NodeMqttTransFunc.on_off,
                                                        NodeMqttTransFunc.work_mode, NodeMqttTransFunc.temp).filter(
                    NodeMqttTransFunc.node_addr == mqtt_node_addr).all()

                print('******node_mqtt_trans_func******', node_mqtt_trans_func)
                if node_mqtt_trans_func:
                    print('airconditoner switch to off!')
                    on_off = '00'
                    mqtt_auto_control_air(node_mqtt_trans_func, on_off)
        else:
            print('airconSwitch is :', airconSwitch)
        return nodes, args


class OneAirConStartEndTimeUpdate(Resource):
    def get(self):
        pass

    def delete(self, todo_id):
        pass

    def put(self, todo_id):
        pass

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('startTime', type=str)
        parser.add_argument('endTime', type=str)
        parser.add_argument('nodeAddr', type=str)

        args = parser.parse_args()
        print(args)

        startTime = args['startTime']
        endTime = args['endTime']
        nodeAddr = args['nodeAddr']
        auto_start_time = datetime.datetime.strptime('1901-01-01 ' + startTime + ':00', "%Y-%m-%d %H:%M:%S")
        auto_end_time = datetime.datetime.strptime('1901-01-01 ' + endTime + ':00', "%Y-%m-%d %H:%M:%S")

        lora_node = db.session.query(LoraNode).filter_by(node_addr=nodeAddr).first()
        lora_node.auto_start_time = auto_start_time
        lora_node.auto_end_time = auto_end_time

        try:
            db.session.commit()
            print("lora node updated!")
        except Exception as e:
            # log.error("Updating LoraNode: %s", e)
            print("Updating LoraNode: %s", e)
            db.session.rollback()

        return 'lora node start/end time updated!'

        return nodes, args


class NodeAlarmStatus(Resource):
    def get(self):

        alarms = db.session.query(AlarmStatus.alarm_status).all()
        status = [alarm[0] for alarm in alarms]
        alarmStatus = any(status)
        alarm_status = {'alarmStatus': alarmStatus}
        print(alarm_status)
        return alarm_status
        

    def delete(self):
        pass

    def put(self):
        pass

    def post(self):
        pass


class AirconBlockItems(Resource):
    def get(self):
        pass

    def delete(self):
        pass

    def put(self):
        pass

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('barnNo', type=str)

        args = parser.parse_args()
        print(args)

        barnNo = args['barnNo']
        print('barnNo', barnNo)


        title1 = '智能控温'
        avatar1 = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1504847335593&di=d7fd8e71543f9b99f12f614718757a0e&imgtype=0&src=http%3A%2F%2Fc1.neweggimages.com.cn%2FNeweggPic2%2Fneg%2FP800%2FA16-184-4PU.jpg'
        background1 = '#64ea91'
        link1 = '/aircon_control/' + barnNo
        smarttempctrl = {'name': '', 'title': title1, 'content': '', 'avatar': avatar1, 'link': link1, 'background': background1}


        title2 = '实时监测'
        avatar2 = 'https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=1819841961,264465916&fm=27&gp=0.jpg'
        background2 = '#8fc9fb'

        nodes = db.session.query(LoraNode.node_addr, LoraNode.node_name).join(GrainBarn, GrainBarn.id == LoraNode.grain_barn_id).filter(
            GrainBarn.barn_no == barnNo).order_by(LoraNode.node_name.asc()).all()

        nodeAddr = nodes[0][0]
        link2 = '/aircondetail/' + nodeAddr
        realtimetemp = {'name': '', 'title': title2, 'content': '', 'avatar': avatar2, 'link': link2, 'background': background2}


        title3 = '火灾预警'
        avatar3 = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1504847444729&di=8d63e49c779b5c58f828bdcb45efd73a&imgtype=0&src=http%3A%2F%2Fimgsrc.baidu.com%2Fimgad%2Fpic%2Fitem%2F0b55b319ebc4b745d353e132c5fc1e178b8215ca.jpg'
        background3 = '#d897eb'
        link3 = '/fire_alarm/' + barnNo
        firealarm = {'name': '', 'title': title3, 'content': '', 'avatar': avatar3, 'link': link3, 'background': background3}


        title4 = '无人值守'
        avatar4 = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1506452820706&di=2f39620de906300a10d3bc2e5920d45c&imgtype=0&src=http%3A%2F%2Fimg.taopic.com%2Fuploads%2Fallimg%2F120712%2F201699-120G2224T175.jpg'
        background4 = '#f69899'
        link4 = '/'
        unmanned = {'name': '', 'title': title4, 'content': '', 'avatar': avatar4, 'link': link4, 'background': background4}


        title5 = '动态联动'
        avatar5 = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1504847729495&di=f65bcca6a50ad1e5565c344eb05d0414&imgtype=jpg&src=http%3A%2F%2Fimg4.imgtn.bdimg.com%2Fit%2Fu%3D3709439994%2C3925194796%26fm%3D214%26gp%3D0.jpg'
        background5 = '#f8c82e'
        link5 = '/'
        dynamiclinkage = {'name': '', 'title': title5, 'content': '', 'avatar': avatar5, 'link': link5, 'background': background5}


        title6 = '智能控电'
        avatar6 = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1504847487313&di=250cf0c99e194c4a5c3413f866aa2a42&imgtype=0&src=http%3A%2F%2Fdown.safehoo.com%2Flt%2Fforum%2F201311%2F18%2F144905a4jnod435ndzn7sj.jpg'
        background6 = '#f797d6'
        link6 = '/fire_alarm/' + barnNo
        electric = {'name': '', 'title': title6, 'content': '', 'avatar': avatar6, 'link': link6, 'background': background6}


        airconBlockItems = [smarttempctrl, electric, realtimetemp, firealarm, unmanned, dynamiclinkage]
        airconBlockItems_dict = {'airconBlockItems': airconBlockItems}
        # print(airconBlockItems_dict)
        return airconBlockItems_dict


class AlarmEmail(Resource):
    def get(self):
        return "alram email"

    def delete(self):
        pass

    def put(self):
        pass

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('user_email', type=str)
        parser.add_argument('subject', type=str)
        parser.add_argument('user_name', type=str)
        parser.add_argument('alarm_msg', type=str)

        args = parser.parse_args()
        print('\n' * 5)
        print('**email**' *5)
        print(args)
        print('**email**' *5)

        print('\n' * 5)
        user_email = args['user_email']
        subject = args['subject']
        user_name = args['user_name']
        alarm_msg = args['alarm_msg']


        send_email(user_email, subject, 'mail/email_alarm', user_name=user_name, alarm_msg=alarm_msg)

        return 'alarm email has sended successfuly!'



        