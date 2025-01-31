from flask_restplus import fields

from ..main import api

posts_namespace = api.namespace('posts', description='Post')

post_keyword_request = api.model('PostKeywordRequest', {
    'keyword': fields.String(required=True, description='Keyword'),
    'from': fields.DateTime(required=True, description='From'),
    'limit': fields.Integer(required=True, description='Page size'),
    'page': fields.Integer(required=True, description='Page number')
})

post_source_request = api.model('PostSourceRequest', {
    'source_id': fields.String(required=True, description='Source id'),
    'from': fields.DateTime(required=True, description='From'),
    'limit': fields.Integer(required=True, description='Page size'),
    'page': fields.Integer(required=True, description='Page number')
})
