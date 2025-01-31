from flask_restplus import fields

from ..main import api

users_namespace = api.namespace('users', description='Users')

users_request = api.model('UsersRequest', {
    'source_ids': fields.List(fields.String(required=True, description='Source ids')),
    'limit': fields.Integer(required=True, description='Page size'),
    'page': fields.Integer(required=True, description='Page number')
})

users_post_request = api.model('UsersPostRequest', {
    'fb_post_id': fields.String(required=True, description='Post id'),
    'limit': fields.Integer(required=True, description='Page size'),
    'page': fields.Integer(required=True, description='Page number')
})
