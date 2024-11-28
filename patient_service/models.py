from flask_sqlalchemy import *
from uuid import uuid4


# This is a database instance
db = SQLAlchemy()


# get unique id
def get_uid():
    return uuid4().hex


class Patient(db.Model):
    __tableName__ = "patients"
    nhs = db.Column(db.Integer, primary_key=True)
    dob = db.Column(db.String(150), )
    name = db.Column(db.String(150), )
    age = db.Column(db.Integer)
    gender = db.Column(db.String(150))
    medical = db.Column(db.String(550))
    allergies = db.Column(db.String(550))
    address = db.Column(db.String(150))
    hospital_code = db.Column(db.String(150))
    timestamp = db.Column(db.String(150))
    injury = db.Column(db.String(150))
    action_taken = db.Column(db.String(150))
    # This is to not use NHS or IHS number
    # __table_args__ = (db.UniqueConstraint('name', 'dob', name='com_key'),)  # composite unique constraint

    # getter
    def get(self):
        return {'nhs': self.nhs, 'dob': self.dob, 'name': self.name, 'age': self.age, 'gender': self.gender,
                'medical': self.medical, 'allergies': self.allergies, 'address': self.address,
                'hospital_code': self.hospital_code, 'timestamp': self.timestamp, 'injury': self.injury, 'action_taken': self.action_taken}

    # create dictionary out of the row
    def to_dict(self):
        return {
            "nhs": self.nhs,
            "dob": self.dob,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "medical": self.medical,
            "allergies": self.allergies,
            "address": self.address,
            "hospital_code": self.hospital_code,
            "timestamp": self.timestamp,
            "injury": self.injury,
            "action_taken": self.action_taken
        }

