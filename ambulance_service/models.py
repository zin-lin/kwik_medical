from flask_sqlalchemy import *
from uuid import uuid4


# This is a database instance
db = SQLAlchemy()


# get unique id
def get_uid():
    return uuid4().hex


class Ambulance(db.Model):
    __tableName__ = "ambulances"
    id = db.Column(db.String(11), primary_key=True, unique=True, default=get_uid)
    lat = db.Column(db.String(150))
    lon = db.Column(db.String(150))
    password = db.Column(db.Text, nullable=False)

