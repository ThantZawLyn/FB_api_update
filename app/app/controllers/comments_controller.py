from flask import jsonify, request
from flask_restplus import Resource

from ..api.comments_api import comments_namespace, comments_request
from ..database.comments_dao import get_post_comments
from ..main import api


@comments_namespace.route('/getByPostId')
class CommentsByPost(Resource):
    @api.expect(comments_request)
    def post(self):
        comments = get_post_comments(request.get_json())
        return jsonify(comments)
