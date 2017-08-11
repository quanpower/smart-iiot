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
    name = Column(String(50), unique = True, nullable=False)

    def __repr__(self):
        return self.name


class Contact(Model):
    id = Column(Integer, primary_key=True)
    name =  Column(String(150), unique = True, nullable=False)
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

class GrainTemp(Model):
    id = Column(Integer, primary_key=True)
    gateway_addr = Column(SmallInteger)
    node_addr = Column(Integer)
    switch = Column(Boolean)
    temp1 = Column(Float)
    temp2 = Column(Float)
    temp3 = Column(Float)
    battery_vol = Column(SmallInteger)
    date = Column(DateTime)

    def __repr__(self):
        return self.node_addr

        
        
