__author__ = 'Aron Kunze'

from flask import Flask, jsonify, request
from flask.ext.sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

from models import User, DeviceLocation

@app.route('/')
def index():
    return "LocOut"

@app.route('/user/<id>')
def getUser(id):
    user = User.query.filter_by(id=id).first()
    if user:
        return "user exists"
    else:
        return "user does not exist"

@app.route('/get_user_devices/<id>')
def getUserDevices(id):
    user = User.query.filter_by(id=id).first()
    if user:
        return jsonify({'status': 200, 'deviceLocations': User.deviceLocationsAsJson()})
    else:
        return jsonify({'status': 400})

@app.route('/set_trust_level/<deviceLocationId>')
def setTrustLevel(deviceLocationId):
    # set trust level (float 0-1) for device
    deviceLocation = DeviceLocation.query.filter_by(id=deviceLocationId).first()
    if deviceLocation:
        trustLevel = request.args.get('trustLevel')
        if trustLevel:
            if deviceLocation.setTrustLevel(trustLevel):
                return jsonify({'status': 200})
    return jsonify({'status': 400})

@app.route('/get_trust_level/<deviceLocationId>')
def getTrustLevel(deviceLocationId):
    # get the TrustLevel for a deviceId
    deviceLocation = DeviceLocation.query.filter_by(id=deviceLocationId).first()
    if deviceLocation:
        return jsonify({'status': 200, 'trustLevel': deviceLocation.trustLevel})
    else:
        return jsonify({'status': 400})

@app.route('/add_device_locatiom/<userId>')
def addDeviceLocation(userId):
    # add a DeviceLocation with a name for a user
    user = User.query.filter_by(id=userId).fist()
    if user:
        lat = request.args.get('lat')
        long = request.args.get('long')
        name = request.args.get('name')
        if lat and long and name:
            deviceLocation = DeviceLocation(userId=userId, lat=lat, long=long, name=name)
            db.session.add(deviceLocation)
            db.session.commit()
            return jsonify({'deviceLocation': deviceLocation.asJson(), 'status': 201})
        else:
            jsonify({'status': 400})
    else:
        return jsonify({'status': 400})


