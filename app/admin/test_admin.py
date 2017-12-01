from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView


class TestAdminView(BaseView):
    @expose('/')
    def index(self):
        # return self.render('index.html')
        return 'test_index.html'

    @expose('/test')
    def test(self):
        # return self.render('index.html')
        return 'test.html'


class TestModelView(ModelView):
    """View function of Flask-Admin for Models page."""
    pass