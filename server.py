__author__ = 'Aron Kunze'

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "LocOut"
    
@app.route('/get_user/<id>')
def getUser(id):
    # return all devices for user
    pass

@app.route('/set_trust_level/<deviceId>')
def setTrustLevel(trustLevel, deviceId):
    # set trust level (float 0-1) for device
    pass

@app.route('/get_trust_level/<deviceId>')
def getTrustLevel(deviceId):
    # get the TrustLevel for a deviceId
    pass

@app.route('/add_device_locatiom/<userId>')
def addDeviceLocation(lat, long, name, userId):
    # add a DeviceLocation with a name for a user
    pass


