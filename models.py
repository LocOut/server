__author__ = 'Aron Kunze'

from server import db
import json

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    deviceLocations = db.relationship("DeviceLocation", backref="user")

    def deviceLocationsAsJson(self):
        if len(self.deviceLocations) == 0:
            return "[]"
        return "[" + ",".join([x.asJson for x in self.deviceLocations]) + "]"

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

    def asJson(self):
        return "{id:{}, lat:{}, long:{}, trustLevel:{}, name:{}}".format(self.id, self.lat, self.long, self.trustLevel,
                                                                         self.name)
