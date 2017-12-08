from flask import request, jsonify, make_response
from flask_restful import Resource, reqparse, abort
import time
import datetime
import json
from app.models import User


class Login(Resource):

    def get(self):
        pass

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)

        args = parser.parse_args()

        username = args['username']
        password = args['password']

        user = User.query.filter_by(username=username).first()
        if user is not None and user.verify_password(password):
            print('-----verify success!-----')
            user_id = user.id
            print(user_id)

            resp = make_response("Set cookie")
            outdate=datetime.datetime.today() + datetime.timedelta(days=30)
            time_now = time.time()
            deadline = time_now + 3600 * 24

            auth_token = user.generate_auth_token(3600)

            print('------auth_token-----')
            print(auth_token)


            print('------set deadline-----')
            print(time_now)
            print(deadline)
            token = json.dumps({'auth_token': auth_token, 'deadline': deadline})

            resp.set_cookie("token", token, expires=outdate)
            resp.status = 'success'
            resp.status_code = 200
            return resp


        # return jsonify({ 'success': True, 'message': 'Ok' })

    def delete(self):
        pass

    def put(self):
        pass



class Logout(Resource):

    def get(self):
        resp = make_response("Delete cookie")
        resp.delete_cookie('token')
        return resp

    def post(self):
        pass

    def delete(self):
        pass

    def put(self):
        pass


class GetUser(Resource):
    def get(self):

        EnumRoleType = {
            'ADMIN': 'admin',
            'DEFAULT': 'guest',
            'DEVELOPER': 'developer',
            }

        userPermission = {
            'DEFAULT': {
                'visit': ['1', '2', '21', '7', '5', '51', '52', '53'],
                'role': EnumRoleType['DEFAULT'],
            },
            'ADMIN': {
                'role': EnumRoleType['ADMIN'],
            },
            'DEVELOPER': {
                'role': EnumRoleType['DEVELOPER'],
            },
            }



        cookie = request.cookies
        print(cookie)

        if cookie:
            try:
                token = cookie['token']
                print('------token-------')
                print(token)
                token_dict = json.loads(token)
                print(token_dict)

                time_now = time.time()
                print('-----time_now-------')
                print(time_now)

                expires = token_dict['deadline']
                print('------expires------')
                print(expires)

                auth_token = token_dict['auth_token']
                print('------auth_token------')
                print(auth_token)

                if expires > time_now:
                    print('in deadline')
                    print(expires-time_now)
                    # filter return iterator in python3,need list to trans
                    # userItem = list(filter(lambda x: x['id'] == 0, adminUsers))[0]

                    # print(userItem)
                    user = User
                    print('-----need verify-----')
                    auth_user = user.verify_auth_token(auth_token)

                    print('------auth-user-----')
                    print(auth_user)

                    user = {}
                    # user['permissions'] = auth_user.role_id
                    user['permissions'] = userPermission['ADMIN']
                    user['username'] = auth_user.username
                    user['id'] = auth_user.id
                    print('-------user--------')
                    print(user)

                    return jsonify({"success": True, "user": user})
                else:
                    return jsonify({"success": False, 'msg': 'cookie expired!'})

            except:
                return jsonify({"success": False, 'msg': 'have no token'})

        return jsonify({"success": False, 'msg': 'have no cookie'})

    def post(self):
        pass

    def delete(self):
        pass

    def put(self):
        pass
