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
    LoraNode, GrainTemp, PowerIo, AlarmLevelSetting, PowerIoRs485Func, NodeMqttTransFunc  


from flask_appbuilder import AppBuilder, BaseView, expose, has_access
from flask import render_template


class MyView(BaseView):

    default_view = 'method1'

    @expose('/method1/')
    @has_access
    def method1(self):
        # do something with param1
        # and return to previous page or index
        return 'Hello'

    @expose('/method2/<string:param1>')
    @has_access
    def method2(self, param1):
        # do something with param1
        # and render template with param
        param1 = 'Goodbye %s' % (param1)
        return param1



    @expose('/method3/')
    # @has_access
    def method3(self):
        # do something with param1
        # and render template with param
        # param1 = 'Goodbye %s' % (param1)
        self.update_redirect()
        return self.render_template('index.html')


def fill_gender():
    try:
        db.session.add(Gender(name='Male'))
        db.session.add(Gender(name='Female'))
        db.session.commit()
    except:
        db.session.rollback()


class ContactModelView(ModelView):
    datamodel = SQLAInterface(Contact)

    list_columns = ['name', 'personal_celphone', 'birthday', 'contact_group.name']

    base_order = ('name', 'asc')
    show_fieldsets = [
        ('Summary', {'fields': ['name', 'gender', 'contact_group']}),
        (
            'Personal Info',
            {'fields': ['address', 'birthday', 'personal_phone', 'personal_celphone'], 'expanded': False}),
    ]

    add_fieldsets = [
        ('Summary', {'fields': ['name', 'gender', 'contact_group']}),
        (
            'Personal Info',
            {'fields': ['address', 'birthday', 'personal_phone', 'personal_celphone'], 'expanded': False}),
    ]

    edit_fieldsets = [
        ('Summary', {'fields': ['name', 'gender', 'contact_group']}),
        (
            'Personal Info',
            {'fields': ['address', 'birthday', 'personal_phone', 'personal_celphone'], 'expanded': False}),
    ]


class GroupModelView(ModelView):
    datamodel = SQLAInterface(ContactGroup)
    related_views = [ContactModelView]


class ContactChartView(GroupByChartView):
    datamodel = SQLAInterface(Contact)
    chart_title = 'Grouped contacts'
    label_columns = ContactModelView.label_columns
    chart_type = 'PieChart'

    definitions = [
        {
            'group' : 'contact_group',
            'series' : [(aggregate_count,'contact_group')]
        },
        {
            'group' : 'gender',
            'series' : [(aggregate_count,'contact_group')]
        }
    ]


def pretty_month_year(value):
    return calendar.month_name[value.month] + ' ' + str(value.year)

def pretty_year(value):
    return str(value.year)


class ContactTimeChartView(GroupByChartView):
    datamodel = SQLAInterface(Contact)

    chart_title = 'Grouped Birth contacts'
    chart_type = 'AreaChart'
    label_columns = ContactModelView.label_columns
    definitions = [
        {
            'group' : 'month_year',
            'formatter': pretty_month_year,
            'series': [(aggregate_count, 'group')]
        },
        {
            'group': 'year',
            'formatter': pretty_year,
            'series': [(aggregate_count, 'group')]
        }
    ]


class GrainStorehouseModelView(ModelView):
    datamodel = SQLAInterface(GrainStorehouse)

    list_columns = ['storehouse_no', 'storehouse_name']
    base_order = ('storehouse_no', 'asc')
    show_fieldsets = [
        ('Summary', {'fields': ['storehouse_no', 'storehouse_name']}),
    ]

    add_fieldsets = [
        ('Summary', {'fields': ['storehouse_no', 'storehouse_name']}),
    ]

    edit_fieldsets = [
        ('Summary', {'fields': ['storehouse_no', 'storehouse_name']}),
    ]

class LoraGatewayModelView(ModelView):
    datamodel = SQLAInterface(LoraGateway)

    list_columns = ['gateway_addr', 'grain_storehouse.storehouse_no', 'grain_storehouse.storehouse_name']

    base_order = ('gateway_addr', 'asc')
    show_fieldsets = [
        ('Summary', {'fields': ['gateway_addr', 'grain_storehouse']}),
    ]

    add_fieldsets = [
        ('Summary', {'fields': ['gateway_addr', 'grain_storehouse']}),
    ]

    edit_fieldsets = [
        ('Summary', {'fields': ['gateway_addr', 'grain_storehouse']}),
    ]

class GrainBarnModelView(ModelView):
    datamodel = SQLAInterface(GrainBarn)

    list_columns = ['barn_no', 'barn_name', 'grain_storehouse.storehouse_no', 'lora_gateway.gateway_addr', 'high_limit', 'low_limit']

    base_order = ('barn_no', 'asc')
    show_fieldsets = [
        ('Summary', {'fields': ['barn_no', 'barn_name', 'grain_storehouse', 'lora_gateway', 'high_limit', 'low_limit']}),
    ]

    add_fieldsets = [
        ('Summary', {'fields': ['barn_no', 'barn_name', 'grain_storehouse', 'lora_gateway', 'high_limit', 'low_limit']}),
    ]

    edit_fieldsets = [
        ('Summary', {'fields': ['barn_no', 'barn_name', 'grain_storehouse', 'lora_gateway', 'high_limit', 'low_limit']}),
    ]

class PowerIoModelView(ModelView):
    datamodel = SQLAInterface(PowerIo)

    list_columns = ['addr', 'name']

    base_order = ('addr', 'asc')
    show_fieldsets = [
        ('Summary', {'fields': ['addr', 'name']}),
    ]

    add_fieldsets = [
        ('Summary', {'fields': ['addr', 'name']}),
    ]

    edit_fieldsets = [
        ('Summary', {'fields': ['addr', 'name']}),
    ]


class PowerIoRs485FuncModelView(ModelView):
    datamodel = SQLAInterface(PowerIoRs485Func)

    list_columns = ['function_name', 'function_code', 'start_at_reg_high', 'start_at_reg_low', 'num_of_reg_high', 'num_of_reg_low']

    base_order = ('function_name', 'asc')
    show_fieldsets = [
        ('Summary', {'fields': ['function_name', 'function_code', 'start_at_reg_high', 'start_at_reg_low', 'num_of_reg_high', 'num_of_reg_low']}),
    ]

    add_fieldsets = [
        ('Summary', {'fields': ['function_name', 'function_code', 'start_at_reg_high', 'start_at_reg_low', 'num_of_reg_high', 'num_of_reg_low']}),
    ]

    edit_fieldsets = [
        ('Summary', {'fields': ['function_name', 'function_code', 'start_at_reg_high', 'start_at_reg_low', 'num_of_reg_high', 'num_of_reg_low']}),
    ]


class NodeMqttTransFuncModelView(ModelView):
    datamodel = SQLAInterface(NodeMqttTransFunc)

    list_columns = ['gateway_addr', 'node_addr', 'trans_direct', 'func_code', 'wind_direct', 'wind_speed', 'model', 'on_off', 'work_mode', 'temp']

    base_order = ('node_addr', 'asc')
    show_fieldsets = [
        ('Summary', {'fields': ['node_addr', 'temp']}),
        (
            'Options',
            {'fields': ['gateway_addr', 'trans_direct', 'func_code', 'wind_direct', 'wind_speed', 'model', 'on_off', 'work_mode'], 'expanded': False}),
    ]

    add_fieldsets = [
        ('Summary', {'fields': ['node_addr', 'temp']}),
        (
            'Options',
            {'fields': ['gateway_addr', 'trans_direct', 'func_code', 'wind_direct', 'wind_speed', 'model', 'on_off', 'work_mode'], 'expanded': False}),
    ]
    edit_fieldsets = [
        ('Summary', {'fields': ['node_addr', 'temp']}),
        (
            'Options',
            {'fields': ['gateway_addr', 'trans_direct', 'func_code', 'wind_direct', 'wind_speed', 'model', 'on_off', 'work_mode'], 'expanded': False}),
    ]


class AlarmLevelSettingModelView(ModelView):
    datamodel = SQLAInterface(AlarmLevelSetting)

    list_columns = ['warning', 'error']

    base_order = ('id', 'asc')
    show_fieldsets = [
        ('Summary', {'fields': ['warning', 'error']}),
    ]

    add_fieldsets = [
        ('Summary', {'fields': ['warning', 'error']}),
    ]

    edit_fieldsets = [
        ('Summary', {'fields': ['warning', 'error']}),
    ]


class LoraNodeModelView(ModelView):
    datamodel = SQLAInterface(LoraNode)

    list_columns = ['node_addr', 'grain_storehouse.storehouse_no', 'lora_gateway.gateway_addr', 'grain_barn.barn_no', 'power_io.addr']

    base_order = ('node_addr', 'asc')
    show_fieldsets = [
        ('Summary', {'fields': ['node_addr', 'grain_storehouse', 'lora_gateway', 'grain_barn', 'power_io']}),
    ]

    add_fieldsets = [
        ('Summary', {'fields': ['node_addr', 'grain_storehouse', 'lora_gateway', 'grain_barn', 'power_io']}),
    ]

    edit_fieldsets = [
        ('Summary', {'fields': ['node_addr', 'grain_storehouse', 'lora_gateway', 'grain_barn', 'power_io']}),
    ]




class CountryDirectChartView(DirectByChartView):
    datamodel = SQLAInterface(GrainTemp)
    chart_title = 'Direct Data Example'

    definitions = [
    {
        'label': 'Unemployment',
        'group': 'stat_date',
        'series': ['unemployed_perc',
                   'college_perc']
    }
]


class GrainTempModelView(ModelView):
    datamodel = SQLAInterface(GrainTemp)

    list_columns = ['grain_storehouse.storehouse_no', 'lora_gateway.gateway_addr', 'grain_barn.barn_no', 'lora_node.node_addr']

    base_order = ('lora_node.node_addr', 'asc')
    show_fieldsets = [
        ('Summary', {'fields': ['grain_storehouse', 'lora_gateway', 'grain_barn', 'lora_node']}),
        (
            'TempData',
            {'fields': ['temp1', 'temp2', 'temp3', 'battery_vol', 'datetime'], 'expanded': True}),
    ]

    add_fieldsets = [
        ('Summary', {'fields': ['grain_storehouse', 'lora_gateway', 'grain_barn', 'lora_node']}),
        (
            'TempData',
            {'fields': ['temp1', 'temp2', 'temp3', 'battery_vol', 'datetime'], 'expanded': True}),
    ]
    edit_fieldsets = [
        ('Summary', {'fields': ['grain_storehouse', 'lora_gateway', 'grain_barn', 'lora_node']}),
        (
            'TempData',
            {'fields': ['temp1', 'temp2', 'temp3', 'battery_vol', 'datetime'], 'expanded': True}),
    ]


class GrainTempChartView(DirectByChartView):
    datamodel = SQLAInterface(GrainTemp)
    chart_title = 'Direct Data Chart'

    definitions = [
    {
        'label': 'temperature',
        'group': 'datetime',
        'series': ['temp1',
                   'temp2',
                   'temp3',
                   'battery_vol']
    }
]


db.create_all()

appbuilder.add_view(GroupModelView, "List Groups", icon="fa-folder-open-o", category="Contacts", category_icon='fa-envelope')
appbuilder.add_view(ContactModelView, "List Contacts", icon="fa-envelope", category="Contacts")
appbuilder.add_separator("Contacts")
appbuilder.add_view(ContactChartView, "Contacts Chart", icon="fa-dashboard", category="Contacts")
appbuilder.add_view(ContactTimeChartView, "Contacts Birth Chart", icon="fa-dashboard", category="Contacts")


appbuilder.add_view(GrainStorehouseModelView, "grain storehouse", icon="icon-home", label=_("Grain Storehouse"), category="Grain", category_icon='icon-home', category_label=_("Grain Setting"))
appbuilder.add_view(GrainBarnModelView, "barn", icon="icon-home", label=_("Barn"), category="Grain")


appbuilder.add_view(LoraGatewayModelView, "lora gateway", icon="icon-cloud", label=_("Lora Gateway"), category="Lora", category_icon='icon-cog', category_label=_("Lora Setting"))
appbuilder.add_view(LoraNodeModelView, "lora node", icon=" icon-circle", label=_("Lora Node"), category="Lora")

appbuilder.add_view(GrainTempModelView, "temperature records", icon="icon-list", label=_("Temperature Records"), category="Temperature", category_icon='icon-signal ', category_label=_("Temperature") )
appbuilder.add_view(GrainTempChartView, "temperature charts", icon="icon-bar-chart", label=_("Temperature Charts"), category="Temperature")


appbuilder.add_view(AlarmLevelSettingModelView, "Alarm Level Setting", icon="icon-list", label=_("Alarm Level Setting"), category="Dynamic", category_icon='icon-signal ', category_label=_("Dynamic") )
appbuilder.add_view(NodeMqttTransFuncModelView, "Node MQTT Trans Func", icon="icon-bar-chart", label=_("Node MQTT Trans Func"), category="Dynamic")
appbuilder.add_view(PowerIoModelView, "Power RS485 IO Control", icon="icon-bar-chart", label=_("Power RS485 IO Control"), category="Dynamic")
appbuilder.add_view(PowerIoRs485FuncModelView, "Power RS485 IO Func", icon="icon-bar-chart", label=_("Power RS485 IO Func"), category="Dynamic")



appbuilder.add_view(MyView, "dashboard", icon='icon-desktop', label=_("Dashboard"), category='Dashboard', category_icon='icon-link', category_label=_('Dashboard'))
appbuilder.add_link("Method2", icon='icon-dashboard', href='/myview/method2/john', category='Dashboard')
appbuilder.add_link("Method3", icon='icon-dashboard', href='/myview/method3/', category='Dashboard')
