"""
Author:         Simo Kauranen
Description:    Module to handle device level communication with DHT22 sensor.
Note:           This code should run in Raspberry Pi device.

"""
from datetime import datetime
 
import adafruit_dht
import board
 
class SensorInfo:
    """Class to hold sensor readings"""
    def __init__(self, id = "xyz"):
        self.sensorID = id
        """Get alive with unrealistic values"""
        self.temperature = -1000
        self.humidity = -1000
        self.timestamp = datetime.utcfromtimestamp(0) # Day zero
        self.sensor_type = ""



class DHT22Sensor:
    """Class to interact with DHT22"""
    
    def __init__(self, id = "xyz"):
        self.sensorInfo = SensorInfo(id)
        self.dht = adafruit_dht.DHT22(board.D2)
     
    def over2Seconds(self, dt):
        """Return True if the last update was over 2 seconds ago"""
        return (dt - self.sensorInfo.timestamp).total_seconds() > 2


    def getSensorInfo(self):
        """Take care that DHT22 is not queried too often.
            Also, both values have to be updated at the same time.
            Returns (possibly updated) SensorInfo object."""

        # DHT22 can only be queried 2 seconds after the previous query
        if self.over2Seconds(datetime.now()):
            try:
               self.sensorInfo.temperature = self.dht.temperature
               self.sensorInfo.humidity = self.dht.humidity
            except Exception:
                pass # If we don't get readings, give old data
            self.sensorInfo.timestamp = datetime.now() # Set new value for last request time
        return self.sensorInfo

