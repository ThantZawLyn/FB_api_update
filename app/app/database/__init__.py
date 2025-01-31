from flask_sqlalchemy import SQLAlchemy

from ..main import app
from ..utils.logging import Log

db = SQLAlchemy(app)
dbro = SQLAlchemy(app)

logger =Log()
logger.log("API DB "+str(db))

from . import models
from . import mapping
from . import tasks_dao
from . import comments_dao
from . import users_dao
