# Module initialiser for app, adapted from drtnf/cits3403-pair-up
# Author: Joel Phillips (22967051)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)

# database stuff
basedir = os.path.abspath(os.path.dirname(__file__))
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "loginroute"
Bootstrap(app)

# import routes, db models, other stuff (for some reason)
from app import routes
from app.models import User