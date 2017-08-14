# -*- coding:utf-8 -*-

from app import app
from flask_restful import reqparse, abort, Api, Resource
from app import db
from app.models import GrainTemp
from sqlalchemy import and_
import json
import random
import datetime


api = Api(app)


class LoraTemp(Resource):
    '''
        get the latest temp.
    '''
    def get(self, gatewayAddr, nodeAddr):
        temps = db.session.query(GrainTemp.temp1, GrainTemp.temp2, GrainTemp.temp3, GrainTemp.battery_vol).filter(and_(GrainTemp.gateway_addr == gatewayAddr, GrainTemp.node_addr == nodeAddr)).order_by(GrainTemp.datetime.desc()).first()
        temp_dic = {"numbers": [{"icon": "apple", "color": "#64ea91", "title": "温度1", "number": temps[0]}, {"icon": "team", "color": "#8fc9fb", "title": "温度2", "number": temps[1]}, {"icon": "team", "color": "#d897eb", "title": "温度3", "number": temps[2]}, {"icon": "message", "color": "#f69899", "title": "电池", "number": temps[3]}]}
        return temp_dic

    def delete(self, todo_id):
		pass

    def put(self, todo_id):
		pass

class LoraTemps(Resource):
    '''
        get the lates 10 temps.
    '''
    def get(self, gatewayAddr, nodeAddr):

        temp_records = db.session.query(GrainTemp.temp1, GrainTemp.temp2, GrainTemp.temp3, GrainTemp.datetime).filter(and_(GrainTemp.lora_gateway.gateway_addr == gatewayAddr, GrainTemp.lora_node.node_addr == nodeAddr)).order_by(GrainTemp.datetime.desc()).limit(10).all()

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
        get the temp records by the input datetime.
    '''
    def get(self, gatewayAddr, nodeAddr, startTime, endTime):
        print(startTime)
        print(endTime)
        # temp_records = db.session.query(GrainTemp.temp1, GrainTemp.temp2, GrainTemp.temp3, GrainTemp.date).filter(GrainTemp.gateway_addr == gatewayAddr, GrainTemp.node_addr == nodeAddr, GrainTemp.date.between(startTime, endTime)).order_by(GrainTemp.date.desc()).all()
        temp_records = db.session.query(GrainTemp.temp1, GrainTemp.temp2, GrainTemp.temp3, GrainTemp.datetime).filter(GrainTemp.datetime.between(startTime, endTime)).order_by(GrainTemp.datetime.desc()).all()

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
    	battery_vol = db.session.query(GrainTemp.battery_vol).filter(and_(GrainTemp.gateway_addr == gatewayAddr, GrainTemp.node_addr == nodeAddr)).order_by(GrainTemp.datetime.desc()).first()
    	battery_dict = {}
    	battery_dict["vol"] = battery_vol[0]
        return json.dumps(battery_dict)

    def post(self):
    	pass


##
## Actually setup the Api resource routing here
##
api.add_resource(LoRaBattery, '/api/v1/loranode_battery/<gatewayAddr>/<nodeAddr>')
api.add_resource(LoraTemp, '/api/v1/loranode_temperature/<gatewayAddr>/<nodeAddr>')
api.add_resource(LoraTemps, '/api/v1/loranode_temperatures/<gatewayAddr>/<nodeAddr>')
api.add_resource(LoraTempRecord, '/api/v1/loranode_temperature_record/<gatewayAddr>/<nodeAddr>/<startTime>/<endTime>')


if __name__ == '__main__':
    app.run(debug=True)

app.run(host='0.0.0.0', port=8888, debug=True)

