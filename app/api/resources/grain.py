from flasgger import Swagger, swag_from
from flask import Flask, redirect, url_for, request, jsonify, make_response
from flask_restful import reqparse, abort, Api, Resource
from app import db
from app.models import User, GrainTemp, LoraGateway, LoraNode, GrainBarn, PowerIo, GrainStorehouse, NodeMqttTransFunc, RelayCurrentRs485Func
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


# api = Api(app)
#
# swagger = Swagger(app)


class LoraTemp(Resource):
    def get(self, gatewayAddr, nodeAddr):
        temps = db.session.query(GrainTemp.temp1, GrainTemp.temp2, GrainTemp.temp3, GrainTemp.battery_vol).filter(
            and_(LoraGateway.gateway_addr == gatewayAddr, LoraNode.node_addr == nodeAddr)).order_by(
            GrainTemp.datetime.desc()).first()
        temp_dic = {"numbers": [{"icon": "apple", "color": "#64ea91", "title": "温度1", "number": temps[0]},
                                {"icon": "apple", "color": "#8fc9fb", "title": "温度2", "number": temps[1]},
                                {"icon": "apple", "color": "#d897eb", "title": "温度3", "number": temps[2]},
                                {"icon": "message", "color": "#f69899", "title": "电池", "number": temps[3]}]}
        return temp_dic

    def delete(self, todo_id):
        pass

    def put(self, todo_id):
        pass


class BarnTemp(Resource):
    def get(self, barn_no):
        temps = db.session.query(GrainTemp.temp1, GrainTemp.temp2, GrainTemp.temp3, GrainTemp.battery_vol).filter(
            and_(LoraGateway.gateway_addr == '1', LoraNode.node_addr == '1')).order_by(
            GrainTemp.datetime.desc()).first()
        print('---------temps-----------')
        print(temps)

        temp_dic1 = {"air_conditioner": [{"title": "温度1", "value": temps[0]}, {"title": "温度2", "value": temps[1]},
                                         {"title": "温度3", "value": temps[2]}, {"title": "电池", "value": temps[3]}]}
        temp_dic2 = {"air_conditioner": [{"title": "温度1", "value": temps[0]}, {"title": "温度2", "value": temps[1]},
                                         {"title": "温度3", "value": temps[2]}, {"title": "电池", "value": temps[3]}]}
        temp_dic3 = {"air_conditioner": [{"title": "温度1", "value": temps[0]}, {"title": "温度2", "value": temps[1]},
                                         {"title": "温度3", "value": temps[2]}, {"title": "电池", "value": temps[3]}]}
        temp_dic4 = {"air_conditioner": [{"title": "温度1", "value": temps[0]}, {"title": "温度2", "value": temps[1]},
                                         {"title": "温度3", "value": temps[2]}, {"title": "电池", "value": temps[3]}]}

        temps_dict = {"air_conditioner_data": [temp_dic1, temp_dic2, temp_dic3, temp_dic4],
                      "alarm": random.randint(0, 1)}

        return temps_dict

    def delete(self, todo_id):
        pass

    def put(self, todo_id):
        pass


class LoraTemps(Resource):
    '''
        get the lates 10 temps.
    '''

    def get(self, gatewayAddr, nodeAddr):
        temp_records = db.session.query(GrainTemp.temp1, GrainTemp.temp2, GrainTemp.temp3, GrainTemp.datetime).filter(
            and_(LoraGateway.gateway_addr == gatewayAddr, LoraNode.node_addr == nodeAddr)).order_by(
            GrainTemp.datetime.desc()).limit(10).all()

        temp_log = []
        for i in range(len(temp_records)):
            temp_log.append({"时间": temp_records[i][3].strftime("%Y-%m-%d %H:%M:%S"), "温度1": temp_records[i][0],
                             "温度2": temp_records[i][1], "温度3": temp_records[i][2]})

        temps_reverse = temp_log[::-1]
        print('------------temps_reverse--------------')
        print(temps_reverse)

        temps_dict = {"temps": temps_reverse}
        return temps_dict

    def delete(self, todo_id):
        pass

    def put(self, todo_id):
        pass


class LoraTempRecord(Resource):
    '''
        get the temp records by the input datetime. %H:%M:S%
    '''

    def get(self, gatewayAddr, nodeAddr, startTime, endTime):
        startTime = datetime.datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
        endTime = datetime.datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S")

        print(startTime)
        print(endTime)
        temp_records = db.session.query(GrainTemp.temp1, GrainTemp.temp2, GrainTemp.temp3, GrainTemp.datetime).filter(
            and_(LoraGateway.gateway_addr == gatewayAddr, LoraNode.node_addr == nodeAddr,
                 GrainTemp.datetime.between(startTime, endTime))).order_by(GrainTemp.datetime.desc()).all()

        temp_log = []
        for i in range(len(temp_records)):
            temp_log.append(
                {"key": i, "time": temp_records[i][3].strftime("%Y-%m-%d %H:%M:%S"), "Temp1": temp_records[i][0],
                 "Temp2": temp_records[i][1], "Temp3": temp_records[i][2]})

        temps_reverse = temp_log[::-1]
        print('------------temps_records--------------')
        print(temps_reverse)

        temps_record_dict = {"tempRecord": temps_reverse}
        return temps_record_dict

    def delete(self, todo_id):
        pass

    def put(self, todo_id):
        pass


class LoRaBattery(Resource):
    '''
        get the latest baterry voltage.
    '''

    def get(self, gatewayAddr, nodeAddr):
        battery_vol = db.session.query(GrainTemp.battery_vol).filter(
            and_(LoraGateway.gateway_addr == gatewayAddr, LoraNode.node_addr == nodeAddr)).order_by(
            GrainTemp.datetime.desc()).first()
        battery_dict = {}
        battery_dict["vol"] = battery_vol[0]
        return battery_dict

    def post(self):
        pass


class Barns(Resource):
    def get(self):

        def return_color(max_abc):
            if max_abc < 40:
                return "#64ea91"
            elif (40 <= max_abc) and (max_abc <= 50):
                return "#8fc9fb"
            else:
                return "#f69899"

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
                # todo: repalce geteway_addr
                print('******node******', node)
                temps = db.session.query(GrainTemp.temp1, GrainTemp.temp2, GrainTemp.temp3, LoraGateway.gateway_addr,
                                         LoraNode.node_addr).join(LoraGateway,
                                                                  LoraGateway.id == GrainTemp.lora_gateway_id).join(
                    LoraNode,
                    LoraNode.id == GrainTemp.lora_node_id).filter(
                    and_(LoraGateway.gateway_addr == '1', LoraNode.node_addr == node[0])).order_by(
                    GrainTemp.datetime.desc()).all()

                # print('temps', temps)
                if temps:
                    max_temp = max(temps[0][0], temps[0][1], temps[0][2])
                    print('max_temp', max_temp)

                    max_temp_dic = {"max_temp": max_temp}
                    max_temps.append(max_temp_dic)
                else:
                    max_temps = []
            print('max_temps:', max_temps)

            if max_temps:
                max_temp_value = max(a['max_temp'] for a in max_temps)
            else:
                max_temp_value = 0

            barn_temps_dic = {"icon": "home", "color": return_color(max_temp_value), "title": barn[1],
                              "number": max_temp_value, "barnNo": barn[0]}
            barn_temps.append(barn_temps_dic)
        barn_dic = {"barns": barn_temps}
        # conc_dash_dic = {"concDash":[{"name":"1","status":1,"content":"上：25.7℃, 中：26.5℃, 下： 31℃","avatar":"http://dummyimage.com/48x48/f279aa/757575.png&text=1","date":"2017-08-19 23:38:45"},{"name":"White","status":2,"content":"上：25.7℃, 中：26.5℃, 下： 31℃","avatar":"http://dummyimage.com/48x48/79cdf2/757575.png&text=W","date":"2017-04-22 14:17:06"},{"name":"Martin","status":3,"content":"上：25.7℃, 中：26.5℃, 下： 31℃","avatar":"http://dummyimage.com/48x48/f1f279/757575.png&text=M","date":"2017-05-07 04:29:13"},{"name":"Johnson","status":1,"content":"上：25.7℃, 中：26.5℃, 下： 31℃","avatar":"http://dummyimage.com/48x48/d079f2/757575.png&text=J","date":"2017-01-14 02:38:37"},{"name":"Jones","status":2,"content":"上：25.7℃, 中：26.5℃, 下： 31℃","avatar":"http://dummyimage.com/48x48/79f2ac/757575.png&text=J","date":"2017-07-08 20:05:50"}]}
        # conc_dash_dic = {"concDash":statuses}
        print("barns", barn_dic)

        # barn_dic = {"barns": [{"icon": "home", "color": "#64ea91", "title": "1haocang", "number": 27.1}, {"icon": "home", "color": "#8fc9fb", "title": "2haocang", "number": 27.5}, {"icon": "home", "color": "#d897eb", "title": "3haocang", "number": 31}, {"icon": "home", "color": "#f69899", "title": "4haocang", "number": 32}, {"icon": "home", "color": "#64ea91", "title": "5haocang", "number": 27.1}, {"icon": "home", "color": "#8fc9fb", "title": "6haocang", "number": 27.5}, {"icon": "home", "color": "#d897eb", "title": "7haocang", "number": 31}, {"icon": "home", "color": "#f69899", "title": "8haocang", "number": 32}]}
        return barn_dic

    def delete(self, todo_id):
        pass

    def put(self, todo_id):
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

        storehouse_value_lable = {'value':'1', 'label':'福州库'}

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

        storehouse_value_lable = {'value':'1', 'label':'福州库'}

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
                node_children.append({'value':node[0], 'label':node[1]+'({0}号节点)'.format(node[0])})

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
        parser.add_argument('gateway_addr', type=str)
        parser.add_argument('node_addr', type=str)

        args = parser.parse_args()

        print('-----realtimetemp args-----', args)

        gatewayAddr = args['gateway_addr']
        nodeAddr = args['node_addr']

        temps = db.session.query(GrainTemp.temp1, GrainTemp.temp2, GrainTemp.temp3, GrainTemp.battery_vol).join(
            LoraNode, LoraNode.id == GrainTemp.lora_node_id).join(
            LoraGateway, LoraGateway.id == GrainTemp.lora_gateway_id).filter(
            and_(LoraNode.node_addr == nodeAddr, LoraGateway.gateway_addr == gatewayAddr)).order_by(
            GrainTemp.datetime.desc()).first()

        # print("temps:", temps)
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
        parser.add_argument('gateway_addr', type=str)
        parser.add_argument('node_addr', type=str)

        args = parser.parse_args()

        print('-------aircontemps args---------', args)

        gatewayAddr = args['gateway_addr']
        nodeAddr = args['node_addr']

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
        max_abc = max(a, b, c)
        print('max_abc:', max_abc)
        if max_abc < 40:
            return 1
        elif (40 <= max_abc) and (max_abc <= 50):
            return 2
        else:
            return 3

    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('gatewayAddr', type=str)
        parser.add_argument('barnNo', type=str)

        args = parser.parse_args()

        print('-------AirConDashboard args---------', args)

        gatewayAddr = args['gatewayAddr']
        barnNo = args['barnNo']


        nodes = db.session.query(LoraNode.node_addr).join(GrainBarn, GrainBarn.id == LoraNode.grain_barn_id).filter(
            GrainBarn.barn_no == barnNo).order_by(LoraNode.node_addr.asc()).all()
        print("nodes are:", nodes)
        statuses = []
        for i in range(len(nodes)):
            node = nodes[i]
            # todo: repalce geteway_addr
            temps = db.session.query(GrainTemp.temp1, GrainTemp.temp2, GrainTemp.temp3, GrainTemp.datetime).join(
                LoraGateway, LoraGateway.id == GrainTemp.lora_gateway_id).join(LoraNode, LoraNode.id == GrainTemp.lora_node_id).filter(
                and_(LoraGateway.gateway_addr == gatewayAddr, LoraNode.node_addr == node[0])).order_by(
                GrainTemp.datetime.desc()).first()
            if temps:
                status = {"name": node[0] + "号空调", "status": self.return_status(temps[0], temps[1], temps[2]),
                          "content": "插座：{0}℃, 空调：{1}℃, 仓温：{2}℃".format(
                              str(temps[0]), str(temps[1]), str(temps[2])),
                          "avatar": "http://dummyimage.com/48x48/{0}/757575.png&text={1}".format(
                              index_color(int(node[0]))[1:], node[0]),
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


class GrainSmarttempCtrl(Resource):
    def get(self, name, content):
        name = ''
        title = '智能控温'
        content = ''
        avatar = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1504847335593&di=d7fd8e71543f9b99f12f614718757a0e&imgtype=0&src=http%3A%2F%2Fc1.neweggimages.com.cn%2FNeweggPic2%2Fneg%2FP800%2FA16-184-4PU.jpg'
        smarttempctrl = {'name': name, 'title': title, 'content': content, 'avatar': avatar}
        smarttempctrl_dic = {'smarttempctrl': smarttempctrl}

        return smarttempctrl_dic

    def delete(self):
        pass

    def put(self):
        pass


class GrainRealtimeTemp(Resource):
    def get(self, name, content):
        name = ''
        title = '实时监测'
        content = ''
        avatar = 'https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=1819841961,264465916&fm=27&gp=0.jpg'
        realtimetemp = {'name': name, 'title': title, 'content': content, 'avatar': avatar}
        realtimetemp_dic = {'realtimetemp': realtimetemp}

        return realtimetemp_dic

    def delete(self):
        pass

    def put(self):
        pass


class GrainFireAlarm(Resource):
    def get(self, name, content):
        name = ''
        title = '火灾预警'
        content = ''
        avatar = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1504847444729&di=8d63e49c779b5c58f828bdcb45efd73a&imgtype=0&src=http%3A%2F%2Fimgsrc.baidu.com%2Fimgad%2Fpic%2Fitem%2F0b55b319ebc4b745d353e132c5fc1e178b8215ca.jpg'
        firealarm = {'name': name, 'title': title, 'content': content, 'avatar': avatar}
        firealarm_dic = {'firealarm': firealarm}

        return firealarm_dic

    def delete(self):
        pass

    def put(self):
        pass


class GrainUnmanned(Resource):
    def get(self):
        name = ''
        title = '无人值守'
        content = ''
        avatar = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1506452820706&di=2f39620de906300a10d3bc2e5920d45c&imgtype=0&src=http%3A%2F%2Fimg.taopic.com%2Fuploads%2Fallimg%2F120712%2F201699-120G2224T175.jpg'
        unmanned = {'name': name, 'title': title, 'content': content, 'avatar': avatar}
        unmanned_dic = {'unmanned': unmanned}

        return unmanned_dic

    def delete(self):
        pass

    def put(self):
        pass


class GrainDynamicLinkage(Resource):
    def get(self, name, content):
        name = ''
        title = u'动态联动'
        content = ''
        avatar = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1504847729495&di=f65bcca6a50ad1e5565c344eb05d0414&imgtype=jpg&src=http%3A%2F%2Fimg4.imgtn.bdimg.com%2Fit%2Fu%3D3709439994%2C3925194796%26fm%3D214%26gp%3D0.jpg'
        dynamiclinkage = {'name': name, 'title': title, 'content': content, 'avatar': avatar}
        dynamiclinkage_dic = {'dynamiclinkage': dynamiclinkage}

        return dynamiclinkage_dic

    def delete(self):
        pass

    def put(self):
        pass


class GrainSecurity(Resource):
    def get(self, name, content):
        name = ''
        title = u'作业安全'
        content = ''
        avatar = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1504847487313&di=250cf0c99e194c4a5c3413f866aa2a42&imgtype=0&src=http%3A%2F%2Fdown.safehoo.com%2Flt%2Fforum%2F201311%2F18%2F144905a4jnod435ndzn7sj.jpg'
        security = {'name': name, 'title': title, 'content': content, 'avatar': avatar}
        security_dic = {'security': security}

        return security_dic

    def delete(self):
        pass

    def put(self):
        pass


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
                'route': '/grain_dashboard',
            },
            {
                'id': '3',
                'bpid': '1',
                'name': '在线监测',
                'icon': 'bulb',
                'route': '/aircondetail',
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
                'route': '/aircon_control',
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
                'route': '/fire_alarm',
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
            if node[2] > 1:
                node_status = {'color':'green', 'text':'运行中', 'current_value':node[2]}
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