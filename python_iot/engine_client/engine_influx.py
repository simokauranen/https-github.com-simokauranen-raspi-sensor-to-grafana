"""
Author:         Simo Kauranen
Description:    Engine to fetch sensor readings from Raspberry Pi devices through REST API / JSON

"""

import tools
import json
from datetime import datetime
import time
import logging
from influxdb import InfluxDBClient
import requests

logging.basicConfig(level=logging.DEBUG)

# Get the Raspberry Pi devices' IP addresses
piList = tools.getPiJSONAddresses()

if len(piList) == 0:
    logging.error("No Pis configured")

piUp = [] # All the sensor Pis that are UP
failed = [] # All the sensor Pis that are DOWN

for i in range(0, len(piList)):
    try:
        resp = requests.get(piList[i])
        if resp.status_code != 200:
            logging.exception("Sensor is DOWN: " + piList[i])
            failed.append(i)
            continue
        logging.debug("Sensor is UP: " + piList[i])
        piUp.append(piList[i])
    except Exception as e:
        logging.exception("Sensor not up: " + piList[i])
        failed.append(i)


# Initialize InfluxDB connection # Sorry about hard coding...
host = 'influxdb'
port = 8086
user = 'admin'
password = 'REPLACE_WITH_PASSWD_2'
dbname = 'sensorhub'
dbuser = 'sensorhub'
dbuser_password = 'REPLACE_WITH_PASSWD_1'

client = InfluxDBClient(host, port, user, password, dbname)
client.switch_user(dbuser, dbuser_password)

# Counts how many times (limit 10) we try to get connection to Pis
counter = 0

# Start the endless fetching process
while True:
    counter += 1
    # Let's take care of all our sensor Pis
    for i in range(0, len(piList)):

        # Let's try connection again if failed before
        if i in failed:
            try:
                resp = requests.get(piList[i])
                if resp.status_code != 200:
                    logging.exception("Sensor is still DOWN: " + piList[i])
                    failed.append(i)
                    continue
                logging.debug("Sensor is now UP: " + piList[i])
                piUp.append(piList[i])
            except Exception as e:
                logging.exception("Sensor DOWN: " + piList[i])
                failed.append(i)
        
        # No use to run endlessly if no sensor Pis up after 10 tries
        if len(piUp) == 0 and counter > 9:
            logging.error("No Sensor Pis up. Exiting.")
            break        
        try:
            resp = requests.get(piList[i]).json()
            # Now we are getting actual data
            # Let's put the JSON in InfluxDB form
            json_body = [
                {
                    "measurement": "temp_hum",
                    "tags": {
                        "pi_addr": piList[i],
                        "sensor_id": resp["sensor_id"]
                    },
                    "time": int(time.time() * 1000),
                    "fields": {
                        "humidity": resp["humidity"],
                        "temperature": resp["temperature"]
                    }
                }
            ]
            logging.debug("Write points: {0}".format(json_body))
            # Write to DB
            client.write_points(json_body, database=dbname, time_precision='ms', batch_size=10000, protocol='json')
            
        except Exception as e:
            logging.exception("Writing to DB not successful: " + str(e))
            pass
    
    # Let's wait a bit before the next round, sensors give new data only after 2 seconds       
    time.sleep(2)

