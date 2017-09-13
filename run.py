# -*- coding:utf-8 -*-

from app import app
from flasgger import Swagger, swag_from
from flask_restful import reqparse, abort, Api, Resource
from app import db
from app.models import GrainTemp, LoraGateway, LoraNode, GrainBarn, GrainStorehouse, ConcGateway, ConcNode, ConcTemp
from sqlalchemy import and_
import json
import random
import datetime
from utils import random_color, index_color
from mqtt_publisher import mqtt_pub_air_con

api = Api(app)

swagger = Swagger(app)


TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
    '42': {'task': 'Use Flasgger'}
}

def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))


class LoraTemp(Resource):

    def get(self, gatewayAddr, nodeAddr):

        # get_parser = reqparse.RequestParser()
        # get_parser.add_argument('id', type=int, location='args', required=True)
        #
        # args = get_parser.parse_args()
        # id = args.get('id')

        temps = db.session.query(GrainTemp.temp1, GrainTemp.temp2, GrainTemp.temp3, GrainTemp.battery_vol).filter(and_(LoraGateway.gateway_addr == gatewayAddr, LoraNode.node_addr == nodeAddr)).order_by(GrainTemp.datetime.desc()).first()
        temp_dic = {"numbers": [{"icon": "apple", "color": "#64ea91", "title": "温度1", "number": temps[0]}, {"icon": "apple", "color": "#8fc9fb", "title": "温度2", "number": temps[1]}, {"icon": "apple", "color": "#d897eb", "title": "温度3", "number": temps[2]}, {"icon": "message", "color": "#f69899", "title": "电池", "number": temps[3]}]}
        return temp_dic

    def delete(self, todo_id):
		pass

    def put(self, todo_id):
		pass


class BarnTemp(Resource):

    def get(self, barn_no):

        # get_parser = reqparse.RequestParser()
        # get_parser.add_argument('id', type=int, location='args', required=True)
        #
        # args = get_parser.parse_args()
        # id = args.get('id')

        temps = db.session.query(GrainTemp.temp1, GrainTemp.temp2, GrainTemp.temp3, GrainTemp.battery_vol).filter(and_(LoraGateway.gateway_addr == '1', LoraNode.node_addr == '1')).order_by(GrainTemp.datetime.desc()).first()
        print('---------temps-----------')
        print(temps)

        temp_dic1 = {"air_conditioner": [{"title": "温度1", "value": temps[0]}, {"title": "温度2", "value": temps[1]}, {"title": "温度3", "value": temps[2]}, {"title": "电池", "value": temps[3]}]}
        temp_dic2 = {"air_conditioner": [{"title": "温度1", "value": temps[0]}, {"title": "温度2", "value": temps[1]}, {"title": "温度3", "value": temps[2]}, {"title": "电池", "value": temps[3]}]}
        temp_dic3 = {"air_conditioner": [{"title": "温度1", "value": temps[0]}, {"title": "温度2", "value": temps[1]}, {"title": "温度3", "value": temps[2]}, {"title": "电池", "value": temps[3]}]}
        temp_dic4 = {"air_conditioner": [{"title": "温度1", "value": temps[0]}, {"title": "温度2", "value": temps[1]}, {"title": "温度3", "value": temps[2]}, {"title": "电池", "value": temps[3]}]}

        temps_dict = {"air_conditioner_data": [temp_dic1, temp_dic2, temp_dic3, temp_dic4], "alarm": random.randint(0,1)}

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

        temp_records = db.session.query(GrainTemp.temp1, GrainTemp.temp2, GrainTemp.temp3, GrainTemp.datetime).filter(and_(LoraGateway.gateway_addr == gatewayAddr, LoraNode.node_addr == nodeAddr)).order_by(GrainTemp.datetime.desc()).limit(10).all()

        temp_log = []
        for i in xrange(len(temp_records)):
            temp_log.append({"时间": temp_records[i][3].strftime("%Y-%m-%d %H:%M:%S"), "温度1": temp_records[i][0], "温度2": temp_records[i][1], "温度3": temp_records[i][2]})
        
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
        temp_records = db.session.query(GrainTemp.temp1, GrainTemp.temp2, GrainTemp.temp3, GrainTemp.datetime).filter(and_(LoraGateway.gateway_addr == gatewayAddr, LoraNode.node_addr == nodeAddr, GrainTemp.datetime.between(startTime, endTime))).order_by(GrainTemp.datetime.desc()).all()


        temp_log = []
        for i in xrange(len(temp_records)):
            temp_log.append({"key": i, "time": temp_records[i][3].strftime("%Y-%m-%d %H:%M:%S"), "Temp1": temp_records[i][0], "Temp2": temp_records[i][1], "Temp3": temp_records[i][2]})
        
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
    	battery_vol = db.session.query(GrainTemp.battery_vol).filter(and_(LoraGateway.gateway_addr == gatewayAddr, LoraNode.node_addr == nodeAddr)).order_by(GrainTemp.datetime.desc()).first()
    	battery_dict = {}
    	battery_dict["vol"] = battery_vol[0]
        return battery_dict

    def post(self):
    	pass


class Barns(Resource):

    def get(self):

        # (get_parser = reqparse.RequestParser()
        # get_parser.add_argument('id', type=int, location='args', required=True)
        #
        # args = get_parser.parse_args()
        # id = args.get('id')

        def return_color(max_abc):
            print('max_abc:', max_abc)
            if max_abc < 35:
                return "#64ea91"
            elif (35 <= max_abc) and (max_abc <= 50):
                return "#8fc9fb"
            else:
                return "#f69899"

        barns = db.session.query(GrainBarn.barn_no, GrainBarn.barn_name).join(GrainStorehouse, GrainStorehouse.id == GrainBarn.grain_storehouse_id).filter(GrainStorehouse.storehouse_no=='1').all()
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
                    GrainTemp.datetime.desc()).all()

                print('temps', temps)
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

            barn_temps_dic = {"icon": "home", "color": return_color(max_temp_value), "title": barn[1], "number": max_temp_value}
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


class ConcRealtimeTemp(Resource):

    def get(self, gatewayAddr, nodeAddr):
        # temps = db.session.query(ConcTemp.temp1, ConcTemp.temp2, ConcTemp.temp3, ConcTemp.battery_vol,ConcNode.node_addr ).filter(and_(ConcGateway.gateway_addr == gatewayAddr, ConcNode.node_addr == unicode(nodeAddr))).order_by(ConcTemp.datetime.desc()).first()
        temps = db.session.query(ConcTemp.temp1, ConcTemp.temp2, ConcTemp.temp3, ConcTemp.battery_vol,ConcNode.node_addr ).filter(ConcNode.node_addr == unicode(nodeAddr)).order_by(ConcTemp.datetime.desc()).first()

        print("temps:",temps)
        conc_realtime_temp_dic = {"concRealtimeTemp": [{"icon": "bulb", "color": "#64ea91", "title": "上", "number": temps[0]}, {"icon": "bulb", "color": "#8fc9fb", "title": "中", "number": temps[1]}, {"icon": "bulb", "color": "#d897eb", "title": "下", "number": temps[2]}, {"icon": "home", "color": "#f69899", "title": "电池", "number": temps[3]}]}
        return conc_realtime_temp_dic

    def delete(self, todo_id):
        pass

    def put(self, todo_id):
        pass


class ConcTemps(Resource):
    '''
        get the lates 10 temps.
    '''
    def get(self, gatewayAddr, nodeAddr):

        temp_records = db.session.query(ConcTemp.temp1, ConcTemp.temp2, ConcTemp.temp3, ConcTemp.datetime).filter(and_(ConcGateway.gateway_addr == gatewayAddr, ConcNode.node_addr == nodeAddr)).order_by(ConcTemp.datetime.desc()).limit(10).all()

        temp_log = []
        for i in xrange(len(temp_records)):
            temp_log.append({"时间": temp_records[i][3].strftime("%Y-%m-%d %H:%M:%S"), "温度1": temp_records[i][0], "温度2": temp_records[i][1], "温度3": temp_records[i][2]})
        
        temps_reverse = temp_log[::-1]
        print('------------temps_reverse--------------')
        print(temps_reverse)

        temps_dict = {"concTemps": temps_reverse}
        return temps_dict

    def delete(self, todo_id):
        pass

    def put(self, todo_id):
        pass


class ConcTempRecord(Resource):
    '''
        get the temp records by the input datetime. %H:%M:S%
    '''
    def get(self, gatewayAddr, nodeAddr, startTime, endTime):
        startTime = datetime.datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
        endTime = datetime.datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S")

        print(startTime)
        print(endTime)
        temp_records = db.session.query(ConcTemp.temp1, ConcTemp.temp2, ConcTemp.temp3, ConcTemp.datetime).filter(and_(ConcGateway.gateway_addr == gatewayAddr, ConcNode.node_addr == nodeAddr, ConcTemp.datetime.between(startTime, endTime))).order_by(ConcTemp.datetime.desc()).all()

        temp_log = []
        for i in xrange(len(temp_records)):
            temp_log.append({"key": i, "time": temp_records[i][3].strftime("%Y-%m-%d %H:%M:%S"), "Temp1": temp_records[i][0], "Temp2": temp_records[i][1], "Temp3": temp_records[i][2]})
        
        temps_reverse = temp_log[::-1]
        print('------------temps_records--------------')
        print(temps_reverse)

        temps_record_dict = {"concTempRecord": temps_reverse}
        return temps_record_dict

    def delete(self, todo_id):
        pass

    def put(self, todo_id):
        pass


class ConcDashboard(Resource):
    def return_status(self,a,b,c):
        max_abc = max(a,b,c)
        print('max_abc:', max_abc)
        if max_abc < 35:
            return 1
        elif (35 <= max_abc) and (max_abc <= 50):
            return 2
        else:
            return 3

    def get(self):
        nodes = db.session.query(ConcNode.node_addr).order_by(ConcNode.node_addr.desc()).all()
        print("nodes are:", nodes)
        statuses = []
        for node in nodes:
            print(type(node))

            # todo: repalce geteway_addr
            temps = db.session.query(ConcTemp.temp1, ConcTemp.temp2, ConcTemp.temp3, ConcTemp.datetime).filter(
                and_(ConcGateway.gateway_addr == '1', ConcNode.node_addr == node[0])).order_by(
                ConcTemp.datetime.desc()).first()
            if temps:
                status = {"name":node[0]+u"号测温点","status":self.return_status(temps[0], temps[1], temps[2]),"content":"上：{0}℃, 中：{1}℃, 下：{2}℃".format(str(temps[0]),str(temps[1]),str(temps[2])),"avatar":"http://dummyimage.com/48x48/f279aa/757575.png&text={0}".format(node[0]),"date":datetime.datetime.strftime(temps[3], "%Y-%m-%d %H:%M:%S")}
                statuses.append(status)
            else:
                statuses = []
        # conc_dash_dic = {"concDash":[{"name":"1","status":1,"content":"上：25.7℃, 中：26.5℃, 下： 31℃","avatar":"http://dummyimage.com/48x48/f279aa/757575.png&text=1","date":"2017-08-19 23:38:45"},{"name":"White","status":2,"content":"上：25.7℃, 中：26.5℃, 下： 31℃","avatar":"http://dummyimage.com/48x48/79cdf2/757575.png&text=W","date":"2017-04-22 14:17:06"},{"name":"Martin","status":3,"content":"上：25.7℃, 中：26.5℃, 下： 31℃","avatar":"http://dummyimage.com/48x48/f1f279/757575.png&text=M","date":"2017-05-07 04:29:13"},{"name":"Johnson","status":1,"content":"上：25.7℃, 中：26.5℃, 下： 31℃","avatar":"http://dummyimage.com/48x48/d079f2/757575.png&text=J","date":"2017-01-14 02:38:37"},{"name":"Jones","status":2,"content":"上：25.7℃, 中：26.5℃, 下： 31℃","avatar":"http://dummyimage.com/48x48/79f2ac/757575.png&text=J","date":"2017-07-08 20:05:50"}]}
        conc_dash_dic = {"concDash":statuses}
        print("conc_dash_dic", conc_dash_dic)


class AirConRealtimeTemp(Resource):

    def get(self, gatewayAddr, nodeAddr):
        temps = db.session.query(GrainTemp.temp1, GrainTemp.temp2, GrainTemp.temp3, GrainTemp.battery_vol).join(
            LoraNode, LoraNode.id == GrainTemp.lora_node_id).join(
            LoraGateway, LoraGateway.id == GrainTemp.lora_gateway_id).filter(
            and_(LoraNode.node_addr == unicode(nodeAddr), LoraGateway.gateway_addr == unicode(gatewayAddr))).order_by(
            GrainTemp.datetime.desc()).first()

        print("temps:",temps)
        air_con_realtime_temp_dic = {"airConRealtimeTemp": [{"icon": "bulb", "color": "#64ea91", "title": "左", "number": temps[0]}, {"icon": "bulb", "color": "#8fc9fb", "title": "中", "number": temps[1]}, {"icon": "bulb", "color": "#d897eb", "title": "右", "number": temps[2]}, {"icon": "message", "color": "#f69899", "title": "电池", "number": temps[3]}]}
        return air_con_realtime_temp_dic

    def delete(self, todo_id):
        pass

    def put(self, todo_id):
        pass


class AirConTemps(Resource):
    '''
        get the lates 10 temps.
    '''
    def get(self, gatewayAddr, nodeAddr):

        temp_records = db.session.query(GrainTemp.temp1, GrainTemp.temp2, GrainTemp.temp3, GrainTemp.datetime).join(
            LoraNode, LoraNode.id == GrainTemp.lora_node_id).join(
            LoraGateway, LoraGateway.id == GrainTemp.lora_gateway_id).filter(
            and_(LoraNode.node_addr == unicode(nodeAddr), LoraGateway.gateway_addr == unicode(gatewayAddr))).order_by(
            GrainTemp.datetime.desc()).limit(10).all()
        temp_log = []
        for i in xrange(len(temp_records)):
            temp_log.append({"时间": temp_records[i][3].strftime("%Y-%m-%d %H:%M:%S"), "温度1": temp_records[i][0], "温度2": temp_records[i][1], "温度3": temp_records[i][2]})
        
        temps_reverse = temp_log[::-1]
        print('------------temps_reverse--------------')
        print(temps_reverse)

        temps_dict = {"airConTemps": temps_reverse}
        return temps_dict

    def delete(self, todo_id):
        pass

    def put(self, todo_id):
        pass


class AirConTempRecord(Resource):
    '''
        get the temp records by the input datetime. %H:%M:S%
    '''
    def get(self, gatewayAddr, nodeAddr, startTime, endTime):
        startTime = datetime.datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
        endTime = datetime.datetime.strptime(endTime, "%Y-%m-%d %H:%M:%S")

        print(startTime)
        print(endTime)
        temp_records = db.session.query(GrainTemp.temp1, GrainTemp.temp2, GrainTemp.temp3, GrainTemp.datetime).join(
            LoraNode, LoraNode.id == GrainTemp.lora_node_id).join(
            LoraGateway, LoraGateway.id == GrainTemp.lora_gateway_id).filter(
            and_(LoraNode.node_addr == unicode(nodeAddr), LoraGateway.gateway_addr == unicode(gatewayAddr), 
                GrainTemp.datetime.between(startTime, endTime))).order_by(
            GrainTemp.datetime.desc()).all()
        print('*********temp_records*************', temp_records)

        temp_log = []
        for i in xrange(len(temp_records)):
            temp_log.append({"key": i, "time": temp_records[i][3].strftime("%Y-%m-%d %H:%M:%S"), "Temp1": temp_records[i][0], "Temp2": temp_records[i][1], "Temp3": temp_records[i][2]})
        
        temps_reverse = temp_log[::-1]
        print('------------temps_records--------------')
        print(temps_reverse)

        temps_record_dict = {"airConTempRecord": temps_reverse}
        return temps_record_dict

    def delete(self, todo_id):
        pass

    def put(self, todo_id):
        pass


class AirConDashboard(Resource):
    def return_status(self,a,b,c):
        max_abc = max(a,b,c)
        print('max_abc:', max_abc)
        if max_abc < 35:
            return 1
        elif (35 <= max_abc) and (max_abc <= 50):
            return 2
        else:
            return 3

    def get(self, gatewayAddr, barnNo):
        nodes = db.session.query(LoraNode.node_addr).join(GrainBarn, GrainBarn.id == LoraNode.grain_barn_id).filter(
            GrainBarn.barn_no == unicode(barnNo)).order_by(LoraNode.node_addr.desc()).all()
        print("nodes are:", nodes)
        statuses = []
        for node in nodes:

            # todo: repalce geteway_addr
            temps = db.session.query(GrainTemp.temp1, GrainTemp.temp2, GrainTemp.temp3, GrainTemp.datetime).join(
                LoraGateway, LoraGateway.id == GrainTemp.lora_gateway_id).join(LoraNode, LoraNode.id == GrainTemp.lora_node_id).filter(
                and_(LoraGateway.gateway_addr == unicode(gatewayAddr), LoraNode.node_addr == node[0])).order_by(
                GrainTemp.datetime.desc()).first()
            if temps:
                status = {"name":node[0]+u"号空调","status":self.return_status(temps[0], temps[1], temps[2]),"content":"左：{0}℃, 中：{1}℃, 右：{2}℃".format(
                    str(temps[0]),str(temps[1]),str(temps[2])),"avatar":"http://dummyimage.com/48x48/{0}/757575.png&text={1}".format(index_color(int(node[0]))[1:], node[0]),"date":datetime.datetime.strftime(temps[3], "%Y-%m-%d %H:%M:%S")}
                statuses.append(status)
            else:
                statuses = []
        # conc_dash_dic = {"concDash":[{"name":"1","status":1,"content":"上：25.7℃, 中：26.5℃, 下： 31℃","avatar":"http://dummyimage.com/48x48/f279aa/757575.png&text=1","date":"2017-08-19 23:38:45"},{"name":"White","status":2,"content":"上：25.7℃, 中：26.5℃, 下： 31℃","avatar":"http://dummyimage.com/48x48/79cdf2/757575.png&text=W","date":"2017-04-22 14:17:06"},{"name":"Martin","status":3,"content":"上：25.7℃, 中：26.5℃, 下： 31℃","avatar":"http://dummyimage.com/48x48/f1f279/757575.png&text=M","date":"2017-05-07 04:29:13"},{"name":"Johnson","status":1,"content":"上：25.7℃, 中：26.5℃, 下： 31℃","avatar":"http://dummyimage.com/48x48/d079f2/757575.png&text=J","date":"2017-01-14 02:38:37"},{"name":"Jones","status":2,"content":"上：25.7℃, 中：26.5℃, 下： 31℃","avatar":"http://dummyimage.com/48x48/79f2ac/757575.png&text=J","date":"2017-07-08 20:05:50"}]}
        air_con_dash_dic = {"airConDash":statuses}
        print("air_con_dash_dic", air_con_dash_dic)
        return air_con_dash_dic


class GrainQuote(Resource):
    def get(self,name,content):
        name = name
        title = u'公告栏'
        content = content
        avatar = 'http://img.hb.aicdn.com/bc442cf0cc6f7940dcc567e465048d1a8d634493198c4-sPx5BR_fw236'
        quote = {'name':name, 'title':title, 'content':content, 'avatar':avatar}
        quote_dic = {'quote':quote}

        return quote_dic

    def delete(self, todo_id):
        pass

    def put(self, todo_id):
        pass


class GrainSmarttempCtrl(Resource):
    def get(self,name,content):
        name = ''
        title = u'智能控温'
        content = ''
        avatar = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1504847335593&di=d7fd8e71543f9b99f12f614718757a0e&imgtype=0&src=http%3A%2F%2Fc1.neweggimages.com.cn%2FNeweggPic2%2Fneg%2FP800%2FA16-184-4PU.jpg'
        smarttempctrl = {'name':name, 'title':title, 'content':content, 'avatar':avatar}
        smarttempctrl_dic = {'smarttempctrl':smarttempctrl}

        return smarttempctrl_dic

    def delete(self, todo_id):
        pass

    def put(self, todo_id):
        pass


class GrainRealtimeTemp(Resource):
    def get(self,name,content):
        name = ''
        title = u'实时监测'
        content = ''
        avatar = 'https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=1819841961,264465916&fm=27&gp=0.jpg'
        realtimetemp = {'name':name, 'title':title, 'content':content, 'avatar':avatar}
        realtimetemp_dic = {'realtimetemp':realtimetemp}

        return realtimetemp_dic

    def delete(self, todo_id):
        pass

    def put(self, todo_id):
        pass


class GrainFireAlarm(Resource):
    def get(self,name,content):
        name = ''
        title = u'火灾预警'
        content = ''
        avatar = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1504847444729&di=8d63e49c779b5c58f828bdcb45efd73a&imgtype=0&src=http%3A%2F%2Fimgsrc.baidu.com%2Fimgad%2Fpic%2Fitem%2F0b55b319ebc4b745d353e132c5fc1e178b8215ca.jpg'
        firealarm = {'name':name, 'title':title, 'content':content, 'avatar':avatar}
        firealarm_dic = {'firealarm':firealarm}

        return firealarm_dic

    def delete(self, todo_id):
        pass

    def put(self, todo_id):
        pass


class GrainDynamicLinkage(Resource):
    def get(self,name,content):
        name = ''
        title = u'动态联动'
        content = ''
        avatar = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1504847729495&di=f65bcca6a50ad1e5565c344eb05d0414&imgtype=jpg&src=http%3A%2F%2Fimg4.imgtn.bdimg.com%2Fit%2Fu%3D3709439994%2C3925194796%26fm%3D214%26gp%3D0.jpg'
        dynamiclinkage = {'name':name, 'title':title, 'content':content, 'avatar':avatar}
        dynamiclinkage_dic = {'dynamiclinkage':dynamiclinkage}

        return dynamiclinkage_dic

    def delete(self, todo_id):
        pass

    def put(self, todo_id):
        pass


class GrainSecurity(Resource):
    def get(self,name,content):
        name = ''
        title = u'作业安全'
        content = ''
        avatar = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1504847487313&di=250cf0c99e194c4a5c3413f866aa2a42&imgtype=0&src=http%3A%2F%2Fdown.safehoo.com%2Flt%2Fforum%2F201311%2F18%2F144905a4jnod435ndzn7sj.jpg'
        security = {'name':name, 'title':title, 'content':content, 'avatar':avatar}
        security_dic = {'security':security}

        return security_dic

    def delete(self, todo_id):
        pass

    def put(self, todo_id):
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
            'route': '/graindashboard',
          },
          {
            'id': '21',
            'bpid': '1',
            'name': '粮仓测温点',
            'icon': 'bulb',
            'route': '/aircondetail',
          },
          {
            'id': '9',
            'bpid': '1',
            'name': '历史记录',
            'icon': 'user',
            'route': '/user',
          },
          {
            'id': '7',
            'bpid': '1',
            'name': '历史记录',
            'icon': 'shopping-cart',
            'route': '/grain_history',
          },
          {
            'id': '8',
            'bpid': '1',
            'name': '智能控温',
            'icon': 'shopping-cart',
            'route': '/aricon_control',
          },
          {
            'id': '21',
            'mpid': '-1',
            'bpid': '2',
            'name': 'User Detail',
            'route': '/user/:id',
          },
          {
            'id': '3',
            'bpid': '1',
            'name': 'Request',
            'icon': 'api',
            'route': '/request',
          },
          {
            'id': '4',
            'bpid': '1',
            'name': 'UI Element',
            'icon': 'camera-o',
          },
          {
            'id': '41',
            'bpid': '4',
            'mpid': '4',
            'name': 'IconFont',
            'icon': 'heart-o',
            'route': '/UIElement/iconfont',
          },
          {
            'id': '42',
            'bpid': '4',
            'mpid': '4',
            'name': 'DataTable',
            'icon': 'database',
            'route': '/UIElement/dataTable',
          },
          {
            'id': '43',
            'bpid': '4',
            'mpid': '4',
            'name': 'DropOption',
            'icon': 'bars',
            'route': '/UIElement/dropOption',
          },
          {
            'id': '44',
            'bpid': '4',
            'mpid': '4',
            'name': 'Search',
            'icon': 'search',
            'route': '/UIElement/search',
          },
          {
            'id': '45',
            'bpid': '4',
            'mpid': '4',
            'name': 'Editor',
            'icon': 'edit',
            'route': '/UIElement/editor',
          },
          {
            'id': '46',
            'bpid': '4',
            'mpid': '4',
            'name': 'layer (Function)',
            'icon': 'credit-card',
            'route': '/UIElement/layer',
          },
          {
            'id': '5',
            'bpid': '1',
            'name': '图表',
            'icon': 'code-o',
          },
          {
            'id': '51',
            'bpid': '5',
            'mpid': '5',
            'name': '线状图',
            'icon': 'line-chart',
            'route': '/chart/lineChart',
          },
          {
            'id': '52',
            'bpid': '5',
            'mpid': '5',
            'name': '柱状图',
            'icon': 'bar-chart',
            'route': '/chart/barChart',
          },
          {
            'id': '53',
            'bpid': '5',
            'mpid': '5',
            'name': '面积图',
            'icon': 'area-chart',
            'route': '/chart/areaChart',
          },
          {
            'id': '6',
            'bpid': '1',
            'name': 'Test Navigation',
            'icon': 'setting',
          },
          {
            'id': '61',
            'bpid': '6',
            'mpid': '6',
            'name': 'Test Navigation1',
            'route': '/navigation/navigation1',
          },
          {
            'id': '62',
            'bpid': '6',
            'mpid': '6',
            'name': 'Test Navigation2',
            'route': '/navigation/navigation2',
          },
          {
            'id': '621',
            'bpid': '62',
            'mpid': '62',
            'name': 'Test Navigation21',
            'route': '/navigation/navigation2/navigation1',
          },
          {
            'id': '622',
            'bpid': '62',
            'mpid': '62',
            'name': 'Test Navigation22',
            'route': '/navigation/navigation2/navigation2',
          },
        ]
        return menus

    def delete(self, todo_id):
        pass

    def put(self, todo_id):
        pass


class GrainHistory(Resource):

    def get(self):
        get_parser = reqparse.RequestParser()
        get_parser.add_argument('status', type=int, location='args', required=True)
        args = get_parser.parse_args()
        status = args.get('status')

        history_records = db.session.query(GrainTemp.grain_barn_id, GrainTemp.lora_gateway_id, GrainTemp.lora_node_id, 
            GrainTemp.temp1, GrainTemp.temp2, GrainTemp.temp3, GrainTemp.battery_vol, GrainTemp.datetime).order_by(
            GrainTemp.datetime.desc()).all()
        print('*********history_records*************', history_records)

        historys = []
        for i in xrange(len(history_records)):

            historys.append({"status":1, "grain_barn_id":"http://dummyimage.com/100x100/{0}/{1}.png&text={2}".format(index_color(history_records[i][0])[1:], '000000', str(history_records[i][0])), "lora_gateway_id":history_records[i][1], "lora_node_id":history_records[i][2],  
                "temp1": history_records[i][3], "temp2": history_records[i][4], "temp3": history_records[i][5], "battery_vol":history_records[i][6], "datetime": history_records[i][7].strftime("%Y-%m-%d %H:%M:%S")})
        
        historys_reverse = historys[::-1]
        print('-------------historys_reverse-------------', historys_reverse)

        # history = [{"title":"Ikkovumf Zhrp Zhxe","author":"Thomas","categories":"ukev","tags":"ubhim","views":64,"comments":182,"date":"1974-03-21 02:24:20","id":10001,"visibility":"Public","image":"http://dummyimage.com/100x100/79f2d2/757575.png&text=T"},]
        grain_history_dic = {'data':historys_reverse, "total":100}

        return grain_history_dic

    def delete(self, todo_id):
        pass

    def put(self, todo_id):
        pass


class AirConControl(Resource):

    def get(self):
        airconcontrol_dic = {'data':'airconcontrol'}

        return airconcontrol_dic

    def delete(self, todo_id):
        pass

    def put(self, todo_id):

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

        # node_select = args['node_select']
        # wind_directtion = args['wind_directtion']
        # wind_speed = args['wind_speed']
        # working_model = args['working_model']
        # temp_setting = args['temp_setting']
        # switch = args['switch']

        # print(bin(node_select))
        # print(bin(wind_directtion))
        # print(bin(wind_speed))
        # print(bin(working_model))
        # print(bin(temp_setting))
        # print(bin(switch))





        return args



class AirConControls(Resource):

    def get(self):

        airconcontrols_dic = {'data':'airconcontrols'}

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

##
## Actually setup the Api resource routing here
##
api.add_resource(LoRaBattery, '/api/v1/loranode_battery/<gatewayAddr>/<nodeAddr>')
api.add_resource(LoraTemp, '/api/v1/loranode_temperature/<gatewayAddr>/<nodeAddr>')
api.add_resource(LoraTemps, '/api/v1/loranode_temperatures/<gatewayAddr>/<nodeAddr>')
api.add_resource(LoraTempRecord, '/api/v1/loranode_temperature_record/<gatewayAddr>/<nodeAddr>/<startTime>/<endTime>')
api.add_resource(BarnTemp, '/api/v1/barn_temperatures/<barn_no>')
api.add_resource(Barns, '/api/v1/barns')

api.add_resource(ConcDashboard, '/api/v1/concrete_dashboard')
api.add_resource(Menus, '/api/v1/menus')

# api.add_resource(ConcTemp, '/api/v1/concrete_temperature/<gatewayAddr>/<nodeAddr>')
api.add_resource(ConcRealtimeTemp, '/api/v1/concrete_temperature/<gatewayAddr>/<nodeAddr>')

api.add_resource(ConcTemps, '/api/v1/concrete_temperatures/<gatewayAddr>/<nodeAddr>')
api.add_resource(ConcTempRecord, '/api/v1/concrete_temperature_record/<gatewayAddr>/<nodeAddr>/<startTime>/<endTime>')

api.add_resource(AirConRealtimeTemp, '/api/v1/air-conditioner_temperature/<gatewayAddr>/<nodeAddr>')

api.add_resource(AirConTemps, '/api/v1/air-conditioner_temperatures/<gatewayAddr>/<nodeAddr>')
api.add_resource(AirConTempRecord, '/api/v1/air-conditioner_temperature_record/<gatewayAddr>/<nodeAddr>/<startTime>/<endTime>')
api.add_resource(AirConDashboard, '/api/v1/air-conditioner_dashboard/<gatewayAddr>/<barnNo>')
api.add_resource(GrainQuote, '/api/v1/grain_quote/<name>/<content>')
api.add_resource(GrainSmarttempCtrl, '/api/v1/grain_smart_temperature_control/<name>/<content>')
api.add_resource(GrainRealtimeTemp, '/api/v1/grain_realtime_temperature/<name>/<content>')
api.add_resource(GrainFireAlarm, '/api/v1/grain_fire_alarm/<name>/<content>')
api.add_resource(GrainDynamicLinkage, '/api/v1/grain_dynamic_linkage/<name>/<content>')
api.add_resource(GrainSecurity, '/api/v1/grain_security/<name>/<content>')
api.add_resource(GrainHistory, '/api/v1/grain_history')
api.add_resource(AirConControl, '/api/v1/air-conditioner_control')
api.add_resource(AirConControls, '/api/v1/air-conditioner_controls')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)

