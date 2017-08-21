# -*- coding:utf-8 -*-

from app import app
from flasgger import Swagger, swag_from
from flask_restful import reqparse, abort, Api, Resource
from app import db
from app.models import GrainTemp, LoraGateway, LoraNode
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


##
## Actually setup the Api resource routing here
##
api.add_resource(LoRaBattery, '/api/v1/loranode_battery/<gatewayAddr>/<nodeAddr>')
api.add_resource(LoraTemp, '/api/v1/loranode_temperature/<gatewayAddr>/<nodeAddr>')
api.add_resource(LoraTemps, '/api/v1/loranode_temperatures/<gatewayAddr>/<nodeAddr>')
api.add_resource(LoraTempRecord, '/api/v1/loranode_temperature_record/<gatewayAddr>/<nodeAddr>/<startTime>/<endTime>')
api.add_resource(BarnTemp, '/api/v1/barn_temperatures/<barn_no>')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)

