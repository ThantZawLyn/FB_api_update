from flask_restplus import fields

from ..main import api

comments_namespace = api.namespace('comments', description='Comments')

comments_request = api.model('CommentsRequest', {
    'fb_post_id': fields.String(required=True, description='Post id'),
    'limit': fields.Integer(required=True, description='Page size'),
    'page': fields.Integer(required=True, description='Page number')
})
