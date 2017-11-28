from flask import request, jsonify, make_response
from flask_restful import Resource, reqparse, abort
import time
import datetime
import json


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
        if password == 'admin':
            id = 0
            resp = make_response("Set cookie")
            outdate=datetime.datetime.today() + datetime.timedelta(days=30)
            time_now = time.time()
            deadline = time_now + 3600 * 24

            print('------set deadline-----')
            print(time_now)
            print(deadline)
            token = json.dumps({'id': id, 'deadline': deadline})

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


class User(Resource):
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


        adminUsers = [
          {
            'id': 0,
            'username': 'admin',
            'password': 'admin',
            'permissions': userPermission['ADMIN'],
          }, {
            'id': 1,
            'username': 'guest',
            'password': 'guest',
            'permissions': userPermission['DEFAULT'],
          }, {
            'id': 2,
            'username': '吴彦祖',
            'password': '123456',
            'permissions': userPermission['DEVELOPER'],
          },
        ]


        cookie = request.cookies
        print(cookie)

        if cookie:
            try:
                token = cookie['token']
                print('------token-------')
                print(token)
                token_dict = json.loads(token)
                print(token_dict)

                # time_now = time.time()
                print('-----time_now-------')
                # print(time_now)

                expires = token_dict['deadline']
                print('------expires------')
                print(expires)

                if expires > 1:
                    print('in deadline')
                    # print(expires-time_now)
                    userItem = filter(lambda x: x['id'] == 0, adminUsers)[0]
                    print(userItem)

                    user = {}
                    user['permissions'] = userItem['permissions']
                    user['username'] = userItem['username']
                    user['id'] = userItem['id']
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
