# -*- coding:utf-8 -*-

from app import app
from flasgger import Swagger, swag_from
from flask_restful import reqparse, abort, Api, Resource
from app import db
from app.models import GrainTemp, LoraGateway, LoraNode, ConcGateway, ConcNode, ConcTemp
from sqlalchemy import and_
import json
import random
import datetime


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

parser = reqparse.RequestParser()
parser.add_argument('task')

class LoraTemp(Resource):
    # """
    #         Get the latest temp.
    #         ---
    #         tags:
    #           - LoraTemp
    #         parameters:
    #           - in: path
    #             name: gateway_addr
    #             required: true
    #             description: The ID of the task, try 42!
    #             type: string
    #         responses:
    #           200:
    #             description: The task data
    #             schema:
    #               id: Task
    #               properties:
    #                 task:
    #                   type: string
    #                   default: My Task
    #         """
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
    """
            Get the barn's latest temp.
            ---
            tags:
              - LoraTemp
            parameters:
              - in: path
                name: barn_no
                required: true
                description: Barn NO!
                type: string
            responses:
              200:
                description: The latest temperatues data of this barn
                schema:
                  id: Task
                  properties:
                    task:
                      type: string
                      default: My Task
            """
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
    # """
    #         Get the latest temp.
    #         ---
    #         tags:
    #           - LoraTemp
    #         parameters:
    #           - in: path
    #             name: gateway_addr
    #             required: true
    #             description: The ID of the task, try 42!
    #             type: string
    #         responses:
    #           200:
    #             description: The task data
    #             schema:
    #               id: Task
    #               properties:
    #                 task:
    #                   type: string
    #                   default: My Task
    #         """
    def get(self):

        # get_parser = reqparse.RequestParser()
        # get_parser.add_argument('id', type=int, location='args', required=True)
        #
        # args = get_parser.parse_args()
        # id = args.get('id')

        barn_dic = {"barns": [{"icon": "home", "color": "#64ea91", "title": "1haocang", "number": 27.1}, {"icon": "home", "color": "#8fc9fb", "title": "2haocang", "number": 27.5}, {"icon": "home", "color": "#d897eb", "title": "3haocang", "number": 31}, {"icon": "home", "color": "#f69899", "title": "4haocang", "number": 32}, {"icon": "home", "color": "#64ea91", "title": "5haocang", "number": 27.1}, {"icon": "home", "color": "#8fc9fb", "title": "6haocang", "number": 27.5}, {"icon": "home", "color": "#d897eb", "title": "7haocang", "number": 31}, {"icon": "home", "color": "#f69899", "title": "8haocang", "number": 32}]}
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

        return conc_dash_dic

    def delete(self, todo_id):
        pass

    def put(self, todo_id):
        pass

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
# api.add_resource(ConcTemp, '/api/v1/concrete_temperature/<gatewayAddr>/<nodeAddr>')
api.add_resource(ConcRealtimeTemp, '/api/v1/concrete_temperature/<gatewayAddr>/<nodeAddr>')

api.add_resource(ConcTemps, '/api/v1/concrete_temperatures/<gatewayAddr>/<nodeAddr>')
api.add_resource(ConcTempRecord, '/api/v1/concrete_temperature_record/<gatewayAddr>/<nodeAddr>/<startTime>/<endTime>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)

