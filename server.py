__author__ = 'Aron Kunze'

from flask import Flask, jsonify, request, render_template, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cors import CORS
import os


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

from models import User, DeviceLocation

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/js/<path:fileName>')
def send_js(fileName):
    return send_from_directory('js', fileName)

@app.route('/dashboard/<id>')
def getDashboart(id):
    user = User.query.filter_by(id=id).first()
    if user:
        return render_template('index.html')
    else:
        return 404

@app.route('/user/<id>')
def getUser(id):
    user = User.query.filter_by(id=id).first()
    if user:
        return jsonify({'user': user.forJsonify()}), 200
    else:
        return jsonify({'status': 404})

@app.route('/get_user_devices/<id>')
def getUserDevices(id):
    user = User.query.filter_by(id=id).first()
    if user:
        return jsonify({'status': 200, 'deviceLocations': user.deviceLocationsForJsonify()})
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
                db.session.refresh(deviceLocation)
                return jsonify({'status': 200, 'deviceLocation': deviceLocation.forJsonify()})
    return jsonify({'status': 400})

@app.route('/get_trust_level/<deviceLocationId>')
def getTrustLevel(deviceLocationId):
    # get the TrustLevel for a deviceId
    deviceLocation = DeviceLocation.query.filter_by(id=deviceLocationId).first()
    if deviceLocation:
        return jsonify({'status': 200, 'trustLevel': deviceLocation.trustLevel})
    else:
        return jsonify({'status': 400})

@app.route('/add_device_location/<userId>')
def addDeviceLocation(userId):
    # add a DeviceLocation with a name for a user
    user = User.query.filter_by(id=userId).first()
    if user:
        try:
            lat = float(request.args.get('lat'))
            long = float(request.args.get('long'))
            name = request.args.get('name')
            if lat and long and name:
                deviceLocation = DeviceLocation(userId=userId, lat=lat, long=long, name=name)
                db.session.add(deviceLocation)
                db.session.commit()
                db.session.refresh(deviceLocation)
                return jsonify({'deviceLocation': deviceLocation.forJsonify(), 'status': 201})
            else:
                return jsonify({'status': 400})
        except:
            return jsonify({'status': 400})
    else:
        return jsonify({'status': 400})

@app.route('/remove_device_location/<deviceLocationId>')
def removeDeviceLocation(deviceLocationId):
    deviceLocation = DeviceLocation.query.filter_by(id=deviceLocationId).first()
    if deviceLocation:
        db.session.delete(deviceLocation)
        db.session.commit()
        return jsonify({'status': 200})
    return jsonify({'status': 400})


