FROM       python:3.7.5
LABEL      maintainer="KAMK Lab"

RUN			pip install flask requests influxdb
RUN			pip install adafruit_dht

WORKDIR    /app

RUN         mkdir python_iot
RUN         cd python_iot
RUN         mkdir raspberry_pi_server

COPY       *.py /app/python_iot/raspberry_pi_server/

RUN        cd python_iot
RUN        cd raspberry_pi_server
RUN        chmod a+x .

WORKDIR    /app/python_iot/raspberry_pi_server

ENV PYTHONPATH "${PYTHONPATH}:/app"

CMD 	["python", "rest_api.py"]