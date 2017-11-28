from flask import jsonify, request, current_app, url_for
from . import api
from ..models import User, Post
import json


@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


@api.route('/users/<int:id>/posts/')
def get_user_posts(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_posts', id=id, page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_posts', id=id, page=page+1)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/users/<int:id>/timeline/')
def get_user_followed_posts(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.followed_posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_followed_posts', id=id, page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_followed_posts', id=id, page=page+1)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })



@api.route('/users/login')
def user_login():
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.followed_posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_followed_posts', id=id, page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_followed_posts', id=id, page=page+1)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })



@api.route('/users/logout')
def user_logout():
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.followed_posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_followed_posts', id=id, page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_followed_posts', id=id, page=page+1)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })



@api.route('/users')
def api_get_user():
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

            expires = token_dict['deadline']
            print('------expires------')
            print(expires)
            time_now = time.time()
            if expires > time_now:
                print('in deadline')
                print(expires - time_now)
                userItem = filter(lambda x: x['id'] == 0, adminUsers)[0]
                print(userItem)

                user = {}
                user['permissions'] = userItem['permissions']
                user['username'] = userItem['username']
                user['id'] = userItem['id']
                print(user)

                return jsonify({"success": True, "user": user})
        except:
            return jsonify({"success": False, 'msg': 'have no token'})

    return jsonify({"success": False, 'msg': 'have no cookie'})