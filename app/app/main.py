import os

from flask import Flask
from flask_restplus import Api

from .utils.logging import Log

app = Flask(__name__)
api = Api(app=app, version="1.0", description="FBS services", title="FBS")
logger = Log()

app.config['CELERY_QUEUE_NAME'] = 'tasks'
app.config['CELERY_BROKER_URL'] = 'amqp://guest@{0}//'.format(
    os.environ.get('RABBITMQ_SERVICE_SERVICE_HOST')
)
app.config['CELERY_BACKEND'] = 'amqp'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'FBS_DATABASE_POSTGRESQL_SERVICE_HOST')

# binds multiple database definition
logger.log("API CONFIG " + app.config['SQLALCHEMY_DATABASE_URI'])
app.config['SQLALCHEMY_BINDS'] = {
    "db": os.environ.get('FBS_DATABASE_POSTGRESQL_SERVICE_HOST'),
    "dbro": os.environ.get('FBS_DATABASE_POSTGRESQL_SLAVE_SERVICE_HOST')
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

TIMEOUT_BETWEEN_ACCOUNTS_WORK = 3
