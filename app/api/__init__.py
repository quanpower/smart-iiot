from flask import Blueprint
api = Blueprint('api', __name__)

# from . import authentication, posts, users, comments, errors

from flask_restful import Api
from app.api.resources import Login, Logout, GetUser, Barns, AllBarns, AllNodes, AirConRealtimeTemp, AirConTemps, AirConTempRecord, AirConDashboard, \
    Menus, GrainHistory, AirConControl, AirConControlOnOff, AirConControls, AirConControlItems, ElectricPowerControl, ElectricPowerControlItems, \
    TianshuoOnOffControl, LoraNodeUpdate, BarnLoraNodeUpdate, NodeAddressByBarnNo, AirConOnOffAllOneKey, OneAirConStartEndTimeUpdate, AutoInit, \
    NodeAlarmStatus, AirconBlockItems, AlarmEmail


api_resource = Api(api)

api_resource.add_resource(Login, '/user/login')
api_resource.add_resource(Logout, '/user/logout')
api_resource.add_resource(GetUser, '/user')
api_resource.add_resource(Menus, '/menus')

api_resource.add_resource(Barns, '/barns')
api_resource.add_resource(AllBarns, '/all_barns')
api_resource.add_resource(AllNodes, '/all_nodes')
api_resource.add_resource(AirConRealtimeTemp, '/air-conditioner_temperature')
api_resource.add_resource(AirConTemps, '/air-conditioner_temperatures')
api_resource.add_resource(AirConTempRecord, '/air-conditioner_temperature_record')
api_resource.add_resource(AirConDashboard, '/air-conditioner_dashboard')
api_resource.add_resource(GrainHistory, '/grain_history')
api_resource.add_resource(AirConControl, '/air-conditioner_control')
api_resource.add_resource(AirConControls, '/air-conditioner_controls')
api_resource.add_resource(AirConControlItems, '/air-conditioner_control_items')
api_resource.add_resource(AirConControlOnOff, '/air-conditioner_control_on_off')
api_resource.add_resource(ElectricPowerControl, '/electric_power_control')
api_resource.add_resource(ElectricPowerControlItems, '/electric_power_control_items')
api_resource.add_resource(TianshuoOnOffControl, '/tianshuo_on_off_control')
api_resource.add_resource(LoraNodeUpdate, '/lora_node_datetime_update')
api_resource.add_resource(BarnLoraNodeUpdate, '/barn_lora_node_datetime_update')
api_resource.add_resource(NodeAddressByBarnNo, '/node_address_by_barn_no')
api_resource.add_resource(AirConOnOffAllOneKey, '/air-conditioner_on_off_all_one_key')
api_resource.add_resource(OneAirConStartEndTimeUpdate, '/one_air-conditioner_start_end_time_update')
api_resource.add_resource(AutoInit, '/auto_init')
api_resource.add_resource(NodeAlarmStatus, '/alarm_status')
api_resource.add_resource(AirconBlockItems, '/air-conditioner_block_items')
api_resource.add_resource(AlarmEmail, '/alarm_email')
