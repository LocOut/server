__author__ = 'Aron Kunze'

from server import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    deviceLocations = db.relationship("DeviceLocation", backref="user")

class DeviceLocation(db.Model):
    __tablename__ = "device_locations"
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String)
    trustLevel = db.Column(db.Float)
    lat = db.Column(db.Float)
    long = db.Column(db.Float)

    def setTrustLevel(self, trustLevel):
        if trustLevel >= 0.0 and trustLevel <= 1.0:
            self.trustLevel = trustLevel
            return True