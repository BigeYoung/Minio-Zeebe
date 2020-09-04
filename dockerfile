FROM python
RUN apt-get update && apt-get install mosquitto -y
RUN pip install paho-mqtt
ENV ZEEBE_GATEWAY MQTT_SERVER
COPY main.py .
ENTRYPOINT ["/bin/sh"]