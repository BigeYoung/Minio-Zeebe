FROM python:3.8.5
RUN apt-get update && apt-get install mosquitto -y
RUN pip install paho-mqtt zeebe-grpc
ENV ZEEBE_GATEWAY zeebe-zeebe-gateway:26500
ENV MQTT_SERVER mqtt-mosquitto
COPY main.py .
ENTRYPOINT ["python3", "main.py"]