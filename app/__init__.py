from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from config import config
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.fileadmin import FileAdmin
from flask_babelex import Babel
import os.path as op


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()
flas_admin = Admin(name='smart-iiot')
babel = Babel()

# flask-login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

# flask-admin add views
from app.admin import UserAdminView, TestAdminView, UserModelView, LoraGatewayModelView, LoraNodeModelView, NodeMqttTransFuncModelView, PowerIoModelView, RelayCurrentRs485FuncModelView, \
GrainStorehouseModelView, GrainBarnModelView, GrainTempModelView, AlarmLevelSettingModelView, AlarmStatusModelView, AlarmTypesModelView, AlarmRecordsModelView

#
# flas_admin.add_view(UserAdminView(name='UserAdmin', category='UserAdmin'))
# flas_admin.add_view(TestAdminView(name='test', endpoint='test', category='UserAdmin'))

flas_admin.add_view(GrainStorehouseModelView(db.session, name='GrainStorehouse', endpoint='grain_storehouse', category='GrainAdmin'))
flas_admin.add_view(GrainBarnModelView(db.session, name='GrainBarn', endpoint='grain_barn', category='GrainAdmin'))
flas_admin.add_view(GrainTempModelView(db.session, name='GrainTemp', endpoint='grain_temps', category='GrainAdmin'))

flas_admin.add_view(LoraGatewayModelView(db.session, name='LoraGateway', endpoint='lora_gateway', category='LoraAdmin'))
flas_admin.add_view(LoraNodeModelView(db.session, name='LoraNode', endpoint='lora_node', category='LoraAdmin'))
flas_admin.add_view(NodeMqttTransFuncModelView(db.session, name='NodeMqttTransFunc', endpoint='node_mqtt_trans_func', category='LoraAdmin'))
flas_admin.add_view(PowerIoModelView(db.session, name='PowerIo', endpoint='power_io', category='LoraAdmin'))
flas_admin.add_view(RelayCurrentRs485FuncModelView(db.session, name='RelayCurrentRs485Func', endpoint='relay_current_rs485_func', category='LoraAdmin'))


flas_admin.add_view(AlarmStatusModelView(db.session, name='AlarmStatus', endpoint='alarm_status', category='AlarmAdmin'))
flas_admin.add_view(AlarmTypesModelView(db.session, name='AlarmTypes', endpoint='alarm_types', category='AlarmAdmin'))
flas_admin.add_view(AlarmRecordsModelView(db.session, name='AlarmRecords', endpoint='alarm_records', category='AlarmAdmin'))
flas_admin.add_view(AlarmLevelSettingModelView(db.session, name='AlarmLevelSetting', endpoint='alarm_level_setting', category='AlarmAdmin'))

flas_admin.add_view(UserModelView(db.session, name='User', endpoint='user', category='UserAdmin'))


path = op.join(op.dirname(__file__), 'static')
print(path)
flas_admin.add_view(FileAdmin(path, '/static/', name='Static Files'))

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    # bable config for i18n
    app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'


    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    configure_extensions(app)

    register_blueprints(app)


    return app



def configure_extensions(app):
    """configure flask extensions
    """
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    babel.init_app(app)
    flas_admin.init_app(app)


def register_blueprints(app):
    """register all blueprints for application
    """

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')


