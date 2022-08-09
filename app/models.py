# Database models
# Author: Joel Phillips (22967051)

from flask_sqlalchemy import SQLAlchemy
from datetime import date, time, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login, db
from sqlalchemy import JSON, func
from sqlalchemy.ext.hybrid import hybrid_property

class User(UserMixin, db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    create_date = db.Column(db.Date, default=date.today)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User {} with name {}>'.format(self.userid, self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
           return (self.userid)

@login.user_loader
def load_user(uid):
    return User.query.get(int(uid))
