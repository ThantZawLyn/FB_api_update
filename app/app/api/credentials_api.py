from flask_restplus import fields

from ..main import api

credentials_namespace = api.namespace('credentials', description='Credentials')

account_request = api.model('AccountsRequest', {
    'accounts': fields.List(fields.String(required=True,
                                          description='Accounts string format email:password')),
})

proxy_request = api.model('ProxiesRequest', {
    'expirationDate': fields.DateTime(required=False, description='expirationDate'),
    'proxies': fields.List(fields.String(required=True,
                                         description='Proxy string format IP:PORT:login:password')),
})

user_agent_request = api.model('UserAgentRequest', {
    'user-agents': fields.List(
        fields.String(required=True, description='User agents string'))
})
