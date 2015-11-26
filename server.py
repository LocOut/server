__author__ = 'Aron Kunze'

from flask import Flask, jsonify, request, abort
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
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
        return jsonify({'status': 200, 'deviceLocations': User.deviceLocations})
    else:
        return jsonify({'status': 400})

@app.route('/set_trust_level/<deviceLocationId>')
def setTrustLevel(trustLevel, deviceLocationId):
    # set trust level (float 0-1) for device
    deviceLocation = DeviceLocation.query.filter_by(id=deviceLocationId)
    if deviceLocation:
        deviceLocation.setTrustLevel()
        return jsonify({'status': 200})
    else:
        return jsonify({'status': 400})

@app.route('/get_trust_level/<deviceId>')
def getTrustLevel(deviceLocationId):
    # get the TrustLevel for a deviceId
    deviceLocation = DeviceLocation.query.filter_by(id=deviceLocationId)
    if deviceLocation:
        return jsonify({'status': 200, 'trustLevel': deviceLocation.trustLevel})
    else:
        return jsonify({'status': 400})

@app.route('/add_device_locatiom/<userId>')
def addDeviceLocation(userId):
    # add a DeviceLocation with a name for a user
    user = User.query.filter_by(id=userId)
    if user:
        lat = request.args.get('lat')
        long = request.args.get('long')
        name = request.args.get('name')
        if lat and long and name:
            deviceLocation = DeviceLocation(userId=userId, lat=lat, long=long, name=name)
            db.session.add(deviceLocation)
            db.session.commit()
            return jsonify({'deviceLocation': deviceLocation, 'status': 201})
        else:
            jsonify({'status': 400})
    else:
        return jsonify({'status': 400})


