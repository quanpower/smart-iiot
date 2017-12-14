from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from app.models import LoraGateway, LoraNode, NodeMqttTransFunc, PowerIo, RelayCurrentRs485Func
import flask_login as login


class LoraGatewayModelView(ModelView):
    """View function of Flask-Admin for Models page."""


    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(LoraGatewayModelView, self).__init__(LoraGateway, session, **kwargs)

    def is_accessible(self):
        return login.current_user.is_authenticated
    #
    # def inaccessible_callback(self, name, **kwargs):
    #     # redirect to login page if user doesn't have access
    #     return redirect(url_for('login', next=request.url))


class LoraNodeModelView(ModelView):
    """View function of Flask-Admin for Models page."""


    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(LoraNodeModelView, self).__init__(LoraNode, session, **kwargs)
    def is_accessible(self):
        return login.current_user.is_authenticated


class NodeMqttTransFuncModelView(ModelView):
    """View function of Flask-Admin for Models page."""


    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(NodeMqttTransFuncModelView, self).__init__(NodeMqttTransFunc, session, **kwargs)
    def is_accessible(self):
        return login.current_user.is_authenticated


class PowerIoModelView(ModelView):

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(PowerIoModelView, self).__init__(PowerIo, session, **kwargs)
    def is_accessible(self):
        return login.current_user.is_authenticated


class RelayCurrentRs485FuncModelView(ModelView):

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(RelayCurrentRs485FuncModelView, self).__init__(RelayCurrentRs485Func, session, **kwargs)
    def is_accessible(self):
        return login.current_user.is_authenticated


