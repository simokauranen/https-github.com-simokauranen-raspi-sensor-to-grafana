FROM       python:3.7.5
LABEL      maintainer="SK"

RUN			pip install requests
RUN         pip install influxdb


WORKDIR    /app

RUN         mkdir python_iot
RUN         cd python_iot
RUN         mkdir engine_client
RUN         cd engine_client
RUN         mkdir config

COPY       ./engine_client/engine_influx.py /app/python_iot/engine_client/
COPY       ./engine_client/tools.py /app/python_iot/engine_client/

COPY        ./engine_client/config/raspberry-pi-urls /app/python_iot/engine_client/config/

RUN        cd /app/python_iot/engine_client
RUN        chmod a+x .

WORKDIR    /app/python_iot/engine_client

ENV PYTHONPATH "${PYTHONPATH}:/app"

CMD 	["python", "engine_influx.py"]