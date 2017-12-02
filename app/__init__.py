from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from flask_admin import Admin
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
from app.admin import UserAdminView, TestAdminView, UserModelView
flas_admin.add_view(UserAdminView(name='UserAdmin', category='UserAdmin'))
flas_admin.add_view(TestAdminView(name='test', endpoint='test', category='UserAdmin'))

flas_admin.add_view(UserModelView(db.session))

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
    app.register_blueprint(api_blueprint, url_prefix='/api/v2')




