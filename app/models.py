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

    def __repr__(self):
        return self.barn_name


class LoraNode(Model):
    id = Column(Integer, primary_key=True)
    node_addr = Column(String(8), unique=True)
    grain_storehouse_id = Column(Integer, ForeignKey('grain_storehouse.id'), nullable=False)
    grain_storehouse = relationship("GrainStorehouse")
    lora_gateway_id = Column(Integer, ForeignKey('lora_gateway.id'), nullable=False)
    lora_gateway = relationship("LoraGateway")
    grain_barn_id = Column(Integer, ForeignKey('grain_barn.id'), nullable=False)
    grain_barn = relationship("GrainBarn")

    def __repr__(self):
        return self.node_addr


class GrainTemp(Model):
    id = Column(Integer, primary_key=True)
    grain_storehouse_id = Column(Integer, ForeignKey('grain_storehouse.id'), nullable=False)
    grain_storehouse = relationship("GrainStorehouse", backref = 'grain_storehouse')
    lora_gateway_id = Column(Integer, ForeignKey('lora_gateway.id'), nullable=False)
    lora_gateway = relationship("LoraGateway",backref = 'lora_gateway')
    grain_barn_id = Column(Integer, ForeignKey('grain_barn.id'), nullable=False)
    grain_barn = relationship("GrainBarn", backref = 'grain_barn')
    lora_node_id = Column(Integer, ForeignKey('lora_node.id'), nullable=False)
    lora_node = relationship("LoraNode", backref = 'lora_node')
    switch = Column(Boolean)
    temp1 = Column(Float)
    temp2 = Column(Float)
    temp3 = Column(Float)
    battery_vol = Column(SmallInteger)
    datetime = Column(DateTime)

    def __repr__(self):
        return self.temp1

