from flask_sqlalchemy import *
from uuid import uuid4
from sqlalchemy.orm import relationship

# This is a database instance
db = SQLAlchemy()


# get unique id
def get_uid():
    return uuid4().hex


class Hospital(db.Model):
    __tableName__ = "hospitals"
    id = db.Column(db.String(11), primary_key=True, unique=True, default=get_uid)
    lat = db.Column(db.String(150))
    lon = db.Column(db.String(150))
    name = db.Column(db.String(150))
    password = db.Column(db.Text, nullable=False)

    def get(self):
        return {'id': self.id, 'lat': self.lat, 'lon': self.lon, 'name': self.name}
