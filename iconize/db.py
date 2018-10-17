import sqlite3
import sys
from flask import current_app as app, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

class Post(db.Model):
    # pylint: disable=E1101
    __tableneme__ = "post"
    iD = db.Column(db.String, primary_key=True)
    created_date = db.Column(db.DateTime(
        timezone=True), server_default=func.now())
    author = db.Column(db.String, nullable=False)
    html = db.Column(db.LargeBinary, nullable=False)
    title = db.Column(db.String, nullable=False)
    s_title = db.Column(db.String, nullable=False)
    color = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    token = db.Column(db.String, nullable=False)
    icon = db.Column(db.LargeBinary, nullable=True)
    ver = db.Column(db.Integer, nullable=False,default=0)
    def __repr__(self):
        return "<post iD:{},title:{}>".format(self.iD, self.title)


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
