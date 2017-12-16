from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from app.models import GrainStorehouse, GrainBarn, GrainTemp
import flask_login as login



class GrainStorehouseModelView(ModelView):

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(GrainStorehouseModelView, self).__init__(GrainStorehouse, session, **kwargs)
    def is_accessible(self):
        return login.current_user.is_authenticated


class GrainBarnModelView(ModelView):

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(GrainBarnModelView, self).__init__(GrainBarn, session, **kwargs)
    def is_accessible(self):
        return login.current_user.is_authenticated


class GrainTempModelView(ModelView):
    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(GrainTempModelView, self).__init__(GrainTemp, session, **kwargs)
    def is_accessible(self):
        return login.current_user.is_authenticated


