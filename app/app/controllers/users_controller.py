from flask import jsonify, request
from flask_restplus import Resource

from ..api.users_api import users_namespace, users_post_request, users_request
from ..database.users_dao import (get_users, get_users_liked_post, get_users_keyword,
                                  get_users_shared_post)
from ..main import api


@users_namespace.route('/getUsersBySource')
class PostsSource(Resource):
    @api.expect(users_request)
    def post(self):
        users = get_users(request.get_json())
        return users


@users_namespace.route('/getSharedUsers')
class PostsSource(Resource):
    @api.expect(users_post_request)
    def post(self):
        users = get_users_shared_post(request.get_json())
        return jsonify(users)


@users_namespace.route('/getLikedUsers')
class PostsSource(Resource):
    @api.expect(users_post_request)
    def post(self):
        users = get_users_liked_post(request.get_json())
        return jsonify(users)

@users_namespace.route('/getUsersByKeyword')
class PostsSource(Resource):
    @api.expect(users_request)
    def post(self):
        users = get_users_keyword(request.get_json())
        return users