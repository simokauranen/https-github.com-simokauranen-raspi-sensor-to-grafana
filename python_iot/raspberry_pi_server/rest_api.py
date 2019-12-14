"""
Author:         Simo Kauranen
Description:    Get Flask web server running and wake up DHT22Sensor instance.
                Serve client through REST API / JSON
Note:           This code should run in Raspberry Pi device.

"""

from flask import Flask
from flask import jsonify
from flask import abort
import dht22_sensor
from datetime import datetime

# Get the server running
app = Flask(__name__)

# Wake up instance of dht22 in this Raspberry Pi
sensor = dht22_sensor.DHT22Sensor("kamk_11")

# Set up URL path for REST API
@app.route('/api/v1/<sensor_id>')
def api_v1_sensor(sensor_id): 
    sensorInfo = sensor.getSensorInfo()
    if sensorInfo.sensorID != sensor_id: # If not my sensor ID return 404
        return abort(404)
    # Make dictionary out of sensor readings and serve as JSON
    dict = {"sensor_id": sensorInfo.sensorID,
            "temperature": sensorInfo.temperature,
            "humidity": sensorInfo.humidity}
    return jsonify(dict)

if __name__ == '__main__':
    app.run(host='0.0.0.0') # Allow requests from all IPs

