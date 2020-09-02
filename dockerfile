FROM python
RUN apt-get update && apt-get install mosquitto -y
RUN pip install paho-mqtt
COPY main.py .
ENTRYPOINT ["/bin/sh"]