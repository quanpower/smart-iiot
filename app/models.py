import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Date,DateTime, SmallInteger, Float, Boolean
from sqlalchemy.orm import relationship
from flask_appbuilder import Model

mindate = datetime.date(datetime.MINYEAR, 1, 1)


class ContactGroup(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class Gender(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class Contact(Model):
    id = Column(Integer, primary_key=True)
    name =  Column(String(150), unique=True, nullable=False)
    address = Column(String(564))
    birthday = Column(Date, nullable=True)
    personal_phone = Column(String(20))
    personal_celphone = Column(String(20))
    contact_group_id = Column(Integer, ForeignKey('contact_group.id'), nullable=False)
    contact_group = relationship("ContactGroup")
    gender_id = Column(Integer, ForeignKey('gender.id'), nullable=False)
    gender = relationship("Gender")

    def __repr__(self):
        return self.name

    def month_year(self):
        date = self.birthday or mindate
        return datetime.datetime(date.year, date.month, 1) or mindate

    def year(self):
        date = self.birthday or mindate
        return datetime.datetime(date.year, 1, 1)


class GrainStorehouse(Model):
    id = Column(Integer, primary_key=True)
    storehouse_no = Column(String(10), unique=True, nullable=False)
    storehouse_name = Column(String(50))

    def __repr__(self):
        return self.storehouse_no


class LoraGateway(Model):
    id = Column(Integer, primary_key=True)
    gateway_addr = Column(String(4), unique=True, nullable=False)
    grain_storehouse_id = Column(Integer, ForeignKey('grain_storehouse.id'), nullable=False)
    grain_storehouse = relationship("GrainStorehouse")

    def __repr__(self):
        return self.gateway_addr


class GrainBarn(Model):
    id = Column(Integer, primary_key=True)
    barn_no = Column(String(10))
    barn_name = Column(String(50))
    grain_storehouse_id = Column(Integer, ForeignKey('grain_storehouse.id'), nullable=False)
    grain_storehouse = relationship("GrainStorehouse")
    lora_gateway_id = Column(Integer, ForeignKey('lora_gateway.id'), nullable=False)
    lora_gateway = relationship("LoraGateway")
    high_limit = Column(SmallInteger)
    low_limit = Column(SmallInteger)

    def __repr__(self):
        return self.barn_name


class PowerIoRs485(Model):
    id = Column(Integer, primary_key=True)
    io_addr = Column(String(8), unique=True)
    io_name = Column(String(50))

    def __repr__(self):
        return self.io_addr
 

class TianshuoRs485(Model):
    id = Column(Integer, primary_key=True)
    tianshuo_addr = Column(String(8), unique=True)
    tianshuo_name = Column(String(50))

    def __repr__(self):
        return self.tianshuo_addr


class LoraNode(Model):
    id = Column(Integer, primary_key=True)
    node_addr = Column(String(8), unique=True)
    grain_storehouse_id = Column(Integer, ForeignKey('grain_storehouse.id'), nullable=False)
    grain_storehouse = relationship("GrainStorehouse")
    lora_gateway_id = Column(Integer, ForeignKey('lora_gateway.id'), nullable=False)
    lora_gateway = relationship("LoraGateway")
    grain_barn_id = Column(Integer, ForeignKey('grain_barn.id'), nullable=False)
    grain_barn = relationship("GrainBarn")
    power_io_rs485_id = Column(Integer, ForeignKey('power_io_rs485.id'), nullable=False)
    power_io_rs485 = relationship("PowerIoRs485")

    def __repr__(self):
        return self.node_addr


class GrainTemp(Model):
    id = Column(Integer, primary_key=True)
    grain_storehouse_id = Column(Integer, ForeignKey('grain_storehouse.id'), nullable=False)
    grain_storehouse = relationship("GrainStorehouse", backref='grain_storehouse')
    lora_gateway_id = Column(Integer, ForeignKey('lora_gateway.id'), nullable=False)
    lora_gateway = relationship("LoraGateway", backref='lora_gateway')
    grain_barn_id = Column(Integer, ForeignKey('grain_barn.id'), nullable=False)
    grain_barn = relationship("GrainBarn", backre ='grain_barn')
    lora_node_id = Column(Integer, ForeignKey('lora_node.id'), nullable=False)
    lora_node = relationship("LoraNode", backref='lora_node')
    switch = Column(Boolean)
    temp1 = Column(Float)
    temp2 = Column(Float)
    temp3 = Column(Float)
    battery_vol = Column(SmallInteger)
    datetime = Column(DateTime)

    def __repr__(self):
        return str(self.temp1)


class PowerIoRs485Func(Model):
    id = Column(Integer, primary_key=True)
    function_name = Column(String(50), unique=True)
    function_code = Column(SmallInteger)
    start_at_reg_high = Column(SmallInteger)
    start_at_reg_low = Column(SmallInteger)
    num_of_reg_high = Column(SmallInteger)
    num_of_reg_low = Column(SmallInteger)

    def __repr__(self):
        return str(self.function_name)


class TianshuoRs485Func(Model):
    id = Column(Integer, primary_key=True)
    function_name = Column(String(50), unique=True)
    function_code = Column(SmallInteger)
    start_at_reg_high = Column(SmallInteger)
    start_at_reg_low = Column(SmallInteger)
    num_of_reg_high = Column(SmallInteger)
    num_of_reg_low = Column(SmallInteger)

    def __repr__(self):
        return str(self.function_name)


class NodeMqttTransFunc(Model):
    id = Column(Integer, primary_key=True)
    gateway_addr = Column(String(3), default='001')
    node_addr = Column(String(13))
    trans_direct = Column(String(1), default='1')
    func_code = Column(String(7), default='0010001')
    wind_direct = Column(String(2), default='00')
    wind_speed = Column(String(2), default='11')
    model = Column(String(10), default='1000111001') # sanling 569
    on_off = Column(String(2))
    work_mode = Column(String(3), default='001')
    temp = Column(String(5), default='10100') #20


    def __repr__(self):
        return str(self.node_addr)



class AlarmLevelSetting(Model):
    id = Column(Integer, primary_key=True)
    warning = Column(SmallInteger, default=35)
    error = Column(SmallInteger, default=45)

    def __repr__(self):
        return str(self.warning)


# class ConcLocation(Model):
#     id = Column(Integer, primary_key=True)
#     location_no = Column(String(10), unique=True, nullable=False)
#     location_name = Column(String(50))

#     def __repr__(self):
#         return self.location_no


# class ConcGateway(Model):
#     id = Column(Integer, primary_key=True)
#     gateway_addr = Column(String(4), unique=True, nullable=False)
#     conc_location_id = Column(Integer, ForeignKey('conc_location.id'), nullable=False)
#     conc_location = relationship("ConcLocation")

#     def __repr__(self):
#         return self.gateway_addr


# class ConcRegion(Model):
#     id = Column(Integer, primary_key=True)
#     region_no = Column(String(10))
#     region_name = Column(String(50))
#     conc_location_id = Column(Integer, ForeignKey('conc_location.id'), nullable=False)
#     conc_location = relationship("ConcLocation")
#     conc_gateway_id = Column(Integer, ForeignKey('conc_gateway.id'), nullable=False)
#     conc_gateway = relationship("ConcGateway")

#     def __repr__(self):
#         return self.region_name


# class ConcNode(Model):
#     id = Column(Integer, primary_key=True)
#     node_addr = Column(String(8), unique=True)
#     conc_location_id = Column(Integer, ForeignKey('conc_location.id'), nullable=False)
#     conc_location = relationship("ConcLocation")
#     conc_gateway_id = Column(Integer, ForeignKey('conc_gateway.id'), nullable=False)
#     conc_gateway = relationship("ConcGateway")
#     conc_region_id = Column(Integer, ForeignKey('conc_region.id'), nullable=False)
#     conc_region = relationship("ConcRegion")

#     def __repr__(self):
#         return self.node_addr


# class ConcTemp(Model):
#     id = Column(Integer, primary_key=True)
#     conc_location_id = Column(Integer, ForeignKey('conc_location.id'), nullable=False)
#     conc_location = relationship("ConcLocation")
#     conc_gateway_id = Column(Integer, ForeignKey('conc_gateway.id'), nullable=False)
#     conc_gateway = relationship("ConcGateway")
#     conc_region_id = Column(Integer, ForeignKey('conc_region.id'), nullable=False)
#     conc_region = relationship("ConcRegion")
#     conc_node_id = Column(Integer, ForeignKey('conc_node.id'), nullable=False)
#     conc_node = relationship("ConcNode", backref = 'conc_node')
#     switch = Column(Boolean)
#     temp1 = Column(Float)
#     temp2 = Column(Float)
#     temp3 = Column(Float)
#     battery_vol = Column(SmallInteger)
#     datetime = Column(DateTime)

#     def __repr__(self):
#         return str(self.datetime)

