from flask import Blueprint
from . import authentication, posts, users, comments, errors
from flask_restful import Api
from app.api.resources import UserResource, UserList

api = Blueprint('api', __name__)
api_resource = Api(api)

api_resource.add_resource(UserResource, '/users/<int:user_id>')
api_resource.add_resource(UserList, '/users')
