FROM eclipse-mosquitto
COPY main.py .
ENTRYPOINT ["python", "main.py"]