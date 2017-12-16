from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from app.models import AlarmStatus, AlarmTypes, AlarmRecords, AlarmLevelSetting
import flask_login as login



class AlarmStatusModelView(ModelView):

    def __init__(self, session, **kwargs):
        super(AlarmStatusModelView, self).__init__(AlarmStatus, session, **kwargs)
    def is_accessible(self):
        return login.current_user.is_authenticated


class AlarmTypesModelView(ModelView):

    def __init__(self, session, **kwargs):
        super(AlarmTypesModelView, self).__init__(AlarmTypes, session, **kwargs)
    def is_accessible(self):
        return login.current_user.is_authenticated


class AlarmRecordsModelView(ModelView):
    def __init__(self, session, **kwargs):
        super(AlarmRecordsModelView, self).__init__(AlarmRecords, session, **kwargs)
    def is_accessible(self):
        return login.current_user.is_authenticated


class AlarmLevelSettingModelView(ModelView):

    def __init__(self, session, **kwargs):
        super(AlarmLevelSettingModelView, self).__init__(AlarmLevelSetting, session, **kwargs)

    def is_accessible(self):
        return login.current_user.is_authenticated