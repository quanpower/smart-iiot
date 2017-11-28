from flask import Blueprint
api = Blueprint('api', __name__)

from . import authentication, posts, users, comments, errors

from flask_restful import Api
from app.api.resources import Login, Logout, User,LoraTemp, BarnTemp, LoraTemps, LoraTempRecord, LoRaBattery, Barns, AirConRealtimeTemp, AirConTemps, \
    AirConTempRecord, AirConDashboard, GrainSmarttempCtrl, GrainRealtimeTemp, GrainFireAlarm, GrainUnmanned, GrainDynamicLinkage, \
    GrainSecurity, Menus, GrainHistory, AirConControl, AirConControlOnOff, AirConControls, ElectricPowerControl, \
    TianshuoOnOffControl, LoraNodeUpdate, BarnLoraNodeUpdate, NodeAddressByBarnNo, AirConOnOffAllOneKey, OneAirConStartEndTimeUpdate, \
    AutoInit




api_resource = Api(api)

api_resource.add_resource(Login, '/user/login')
api_resource.add_resource(Logout, '/user/logout')
api_resource.add_resource(User, '/user')


api_resource.add_resource(Menus, 'menus')


api_resource.add_resource(LoRaBattery, '/loranode_battery/<gatewayAddr>/<nodeAddr>')
api_resource.add_resource(LoraTemp, '/loranode_temperature/<gatewayAddr>/<nodeAddr>')
api_resource.add_resource(LoraTemps, '/loranode_temperatures/<gatewayAddr>/<nodeAddr>')
api_resource.add_resource(LoraTempRecord, '/loranode_temperature_record/<gatewayAddr>/<nodeAddr>/<startTime>/<endTime>')
api_resource.add_resource(BarnTemp, '/barn_temperatures/<barn_no>')
api_resource.add_resource(Barns, '/barns')
api_resource.add_resource(AirConRealtimeTemp, '/air-conditioner_temperature')

api_resource.add_resource(AirConTemps, '/air-conditioner_temperatures')
api_resource.add_resource(AirConTempRecord, '/air-conditioner_temperature_record')
api_resource.add_resource(AirConDashboard, '/air-conditioner_dashboard/<gatewayAddr>/<barnNo>')
api_resource.add_resource(GrainSmarttempCtrl, '/grain_smart_temperature_control/<name>/<content>')
api_resource.add_resource(GrainRealtimeTemp, '/grain_realtime_temperature/<name>/<content>')
api_resource.add_resource(GrainFireAlarm, '/grain_fire_alarm/<name>/<content>')
api_resource.add_resource(GrainUnmanned, '/grain_unmanned/<name>/<content>')
api_resource.add_resource(GrainDynamicLinkage, '/grain_dynamic_linkage/<name>/<content>')
api_resource.add_resource(GrainSecurity, '/grain_security/<name>/<content>')
api_resource.add_resource(GrainHistory, '/grain_history')
api_resource.add_resource(AirConControl, '/air-conditioner_control')
api_resource.add_resource(AirConControls, '/air-conditioner_controls')
api_resource.add_resource(AirConControlOnOff, '/air-conditioner_control_on_off')
api_resource.add_resource(ElectricPowerControl, '/electric_power_control')
api_resource.add_resource(TianshuoOnOffControl, '/tianshuo_on_off_control')
api_resource.add_resource(LoraNodeUpdate, '/lora_node_datetime_update')
api_resource.add_resource(BarnLoraNodeUpdate, '/barn_lora_node_datetime_update')
api_resource.add_resource(NodeAddressByBarnNo, '/node_address_by_barn_no')
api_resource.add_resource(AirConOnOffAllOneKey, '/air-conditioner_on_off_all_one_key')
api_resource.add_resource(OneAirConStartEndTimeUpdate, '/one_air-conditioner_start_end_time_update')
api_resource.add_resource(AutoInit, '/auto_init')

