FROM python
RUN apt-get update && apt-get install mosquitto -y
RUN pip3 install paho-mqtt zeebe-grpc
ENV ZEEBE_GATEWAY zeebe-zeebe-gateway:26500
ENV MQTT_SERVER mqtt-mosquitto
COPY main.py .
ENTRYPOINT ["python3", "main.py"]