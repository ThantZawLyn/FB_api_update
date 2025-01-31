from flask import jsonify, request
from flask_restplus import Resource

from ..api.credentials_api import (account_request, credentials_namespace,
                                   proxy_request, user_agent_request)
from ..database.mapping import AccountsSchema, ProxySchema, UserAgentSchema
from ..database.worker_credentials_dao import (create_account, create_proxy,
                                               create_user_agent, get_accounts,
                                               get_accounts_stat,
                                               get_available_wc_count,
                                               get_locked_count,
                                               get_potential_new_wc_count,
                                               get_proxy, get_proxy_stat,
                                               get_user_agent)
from ..main import api
from ..services.celery_service import send_re_login_disabled_accounts
from ..services.credentials_management import accounts_warming, proxy_re_enable


@credentials_namespace.route('/accounts')
class Accounts(Resource):
    def get(self):
        return AccountsSchema().dump(get_accounts(), many=True)

    @api.expect(account_request)
    def post(self):
        data = request.get_json()
        accounts = data['accounts']

        count = 0
        for account in accounts:
            split = account.split(";", 2)
            if create_account(split[0], split[1]):
                count += 1
        return "{} accounts created {} has already stored".format(count,
                                                                  len(accounts) - count)


@credentials_namespace.route('/proxies')
class Proxies(Resource):
    def get(self):
        return ProxySchema().dump(get_proxy(), many=True)

    @api.expect(proxy_request)
    def post(self):
        data = request.get_json()
        expiration_date = data['expirationDate']
        proxies = data['proxies']

        count = 0
        for proxy in proxies:
            split = proxy.split(":")
            if create_proxy(split[0], split[1], split[2], split[3], expiration_date):
                count += 1
        return "{} accounts created {} has already stored".format(count,
                                                                  len(proxies) - count)


@credentials_namespace.route('/user-agent')
class UserAgent(Resource):
    def get(self):
        return UserAgentSchema().dump(get_user_agent(), many=True)

    @api.expect(user_agent_request)
    def post(self):
        data = request.get_json()
        user_agents = data['user-agents']

        count = 0
        for user_agent in user_agents:
            if create_user_agent(user_agent):
                count += 1

        return "{} agents created {} has already stored".format(count,
                                                                len(user_agents) - count)


@credentials_namespace.route('/accounts/stat')
class ProxiesStat(Resource):
    def get(self):
        all, available = get_proxy_stat()
        return jsonify({"all": all, "available": available})


@credentials_namespace.route('/accounts/warming')
class Warming(Resource):
    def get(self):
        wc_count = accounts_warming()
        return jsonify({"message": "send " + str(wc_count) + " accounts to warm"})


@credentials_namespace.route('/accounts/relogin')
class Relogin(Resource):
    def get(self):
        send_re_login_disabled_accounts()
        return jsonify({"message": "send all accounts to relogin"})


@credentials_namespace.route('/proxies/stat')
class ProxiesStat(Resource):
    def get(self):
        all, available = get_accounts_stat()
        return jsonify({"all": all, "available": available})


@credentials_namespace.route('/proxies/reenable/<int:count>')
class ProxyEnable(Resource):
    def get(self, count):
        if count:
            proxy_re_enable(count)
        else:
            proxy_re_enable(None)

        return jsonify({"message": "send proxy to enable"})


@credentials_namespace.route('/statistics')
class Statistics(Resource):
    def get(self):
        account_count, proxy_count, user_agent_count = get_potential_new_wc_count()
        account_locked_count, proxy_locked_count = get_locked_count()
        return jsonify({"working_credentials_available": str(get_available_wc_count()),
                        "locked": "accounts locked by proxy: {}, proxy locked by account: {}"
                       .format(str(account_locked_count), str(proxy_locked_count)),
                        "spare": "accounts: {}, proxy: {}, user_agent: {}"
                       .format(str(account_count), str(proxy_count),
                               str(user_agent_count))})
