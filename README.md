# Python IoT Project
Get temperature and humidity from Raspberry Pi devices to Grafana through InfluxDB – all on Docker.

## Arcitecture

Two parts:
- Sensors and API server on Raspberry Pi devices (```python_iot/raspberry_pi_server/*.py```)
- Client (Engine) anywhere on Docker (```python_iot/engine_client/*.py```)

When RasPi servers are running, Engine can fetch the data as JSON through REST API using list of IPs (configured in the file ```/python_iot/engine_client/config/raspberry-pi-urls```). Engine fetches the data every 2 seconds, timestamp is added and JSON stored to InfluxDB. 

![Python IoT Arcitecture](/python_iot/readme_images/IoT_architecture.jpg?raw=true)


## Grafana output (sample)

Since InfluxDB works well with Grafana, the visualization is easy to get with only light configuring. Here we have two Raspberry Pi devices DHT1 and DHT2, which both have sensors for temperature & humidity.

![Grafana Output](/python_iot/readme_images/grafana_view.jpg?raw=true)




## Background
This project was made on KAMK (www.kamk.fi) course Python Project for IoT – which was engaging experience, thanks to course coach Jaakko Vanhala.


