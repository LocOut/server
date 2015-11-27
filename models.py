__author__ = 'Aron Kunze'

from server import db
import json

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    deviceLocations = db.relationship("DeviceLocation", backref="user")

    def deviceLocationsForJsonify(self):
        return [x.forJsonify() for x in self.deviceLocations].sort(key=lambda e: int(e["id"]))

    def forJsonify(self):
        return {'id': self.id, 'deviceLocations': self.deviceLocationsForJsonify()}

class DeviceLocation(db.Model):
    __tablename__ = "device_locations"
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String)
    trustLevel = db.Column(db.Float, default=0.0)
    lat = db.Column(db.Float)
    long = db.Column(db.Float)

    def setTrustLevel(self, trustLevel):
        try:
            t = float(trustLevel)
            if t >= 0.0 and t <= 1.0:
                self.trustLevel = t
                db.session.commit()
                return True
            return False
        except ValueError:
            return False

    def forJsonify(self):
        out = self.__dict__
        out.pop("_sa_instance_state", None)
        return out