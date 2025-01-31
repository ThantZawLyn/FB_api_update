from flask import jsonify, request

from ..database.mapping import WorkerCredentialSchema
from ..database.worker_credentials_dao import update_worker_credential
from ..main import app


@app.route('/worker-credential/block', methods=['POST'])
def worker_credential_block():
    data = request.get_json()
    worker_credential = update_worker_credential(data)
    return WorkerCredentialSchema().dump(worker_credential)
