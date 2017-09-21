# -*- coding:utf-8 -*-

import calendar
from flask_appbuilder import ModelView, DirectByChartView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.group import aggregate_count
from flask_appbuilder.widgets import FormHorizontalWidget, FormInlineWidget, FormVerticalWidget
from flask_babel import lazy_gettext as _


from app import db, appbuilder
from .models import ContactGroup, Gender, Contact, GrainStorehouse, GrainBarn, LoraGateway, \
    LoraNode, GrainTemp, PowerIoRs485, AlarmLevelSetting, PowerIoRs485Func, NodeMqttTransFunc  #ConcLocation, ConcGateway, ConcRegion, ConcNode, ConcTemp

def fill_gender():
    try:
        db.session.add(Gender(name='Male'))
        db.session.add(Gender(name='Female'))
        db.session.commit()
    except:
        db.session.rollback()


def fill_grain_storehouse():
    try:
        db.session.add(Gender(storehouse_no='1', storehouse_name='福州直属库'))
        db.session.commit()
    except:
        db.session.rollback()


class LoraGateway(Model):
    id = Column(Integer, primary_key=True)
    gateway_addr = Column(String(4), unique=True, nullable=False)
    grain_storehouse_id = Column(Integer, ForeignKey('grain_storehouse.id'), nullable=False)
    grain_storehouse = relationship("GrainStorehouse")

    def __repr__(self):
        return self.gateway_addr


def fill_lora_gateway():
    try:
        db.session.add(Gender(name='Male'))
        db.session.add(Gender(name='Female'))
        db.session.commit()
    except:
        db.session.rollback()
