from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from app.models import User


class UserAdminView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')
        # return 'index.html'


class CustomModelView(ModelView):
    """View function of Flask-Admin for Models page."""
    pass


class UserModelView(ModelView):
    """View function of Flask-Admin for Models page."""

    # def is_accessible(self):
    #     if current_user.is_authenticated and current_user.username == "admin":
    #         return True
    #     return False

    can_create = True
    can_delete = False
    can_edit = False


    column_list = ('email', 'username', 'role_id', 'password_hash', 'confirmed')
    column_searchable_list = ('username', 'email')
    column_filters = ('username', 'email') 
    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(UserModelView, self).__init__(User, session, **kwargs)