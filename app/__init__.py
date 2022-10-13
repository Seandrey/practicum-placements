# Module initialiser for app, adapted from drtnf/cits3403-pair-up
# Author: Joel Phillips (22967051), David Norris (22690264)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config, DevConfig
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
import os
from jinja2.utils import markupsafe

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, template_folder="views")

# database stuff
dev = os.environ.get('DEVELOPMENT')
if dev:
  app.config.from_object(DevConfig)
else:
  app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
login = LoginManager(app)
login.login_view = "loginroute"

Bootstrap(app)

# import routes, db models, other stuff (for some reason)
from app import routes
from app.models import User, ActivityLog
from app.reports import teardown_db, fill_db_multiple_students

# DEBUG
#teardown_db()
# this fill db starts at 22000000, for testing navigate to /reports/student/22000000 as we only populate one
#fill_db_multiple_students(10)
