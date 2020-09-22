#!/usr/bin/env python3
from __future__ import print_function
import paho.mqtt.client as mqtt
import json
import logging
import grpc
from zeebe_grpc import gateway_pb2, gateway_pb2_grpc
import os

ZEEBE_GATEWAY = os.environ['ZEEBE_GATEWAY']
MQTT_SERVER = os.environ['MQTT_SERVER']

print(ZEEBE_GATEWAY)
print(MQTT_SERVER)

def zeebe_msg(file_path):
    print("完整路径：", file_path)

    directory = file_path.split("/", 1)[0]
    print("文件夹：", directory)

    file_whole_name = file_path.split("/", 1)[1]
    print("文件全名：", file_whole_name)

    file_name = file_whole_name.split(".", 1)[0]
    print("文件名：", file_name)

    with grpc.insecure_channel(ZEEBE_GATEWAY) as channel:
        stub = gateway_pb2_grpc.GatewayStub(channel)
        var = {directory: file_path}
        print(var)
        publishMessageRequest = gateway_pb2.PublishMessageRequest(
            # the name of the message
            name=directory+"-uploaded",
            # how long the message should be buffered on the broker, in milliseconds
            timeToLive=1000,
            correlationKey="aml/"+file_name+".aml",
            # the unique ID of the message; can be omitted. only useful to ensure only one message
            # with the given ID will ever be published (during its lifetime)
            # the message variables as a JSON document; to be valid, the root of the document must be an
            # object, e.g. { "a": "foo" }. [ "foo" ] would not be valid.
            variables=json.dumps(var)
        )
        print(publishMessageRequest)
        publishMessageResponse = stub.PublishMessage(publishMessageRequest)
        print("Response")
        print(publishMessageResponse)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # qos level is set to 1
    client.subscribe("minio", 1)


def on_message(client, userdata, msg):
    payload_json = bytes.decode(msg.payload)
    print(payload_json)   # b'{"EventName":"s3:ObjectCreated:Put","Key":"aml/_Robot_Grasp_AAS_Model.aml","Records":[{"eventVersion":"2.0","eventSource":"minio:s3","awsRegion":"","eventTime":"2020-09-03T09:16:43.983Z","eventName":"s3:ObjectCreated:Put","userIdentity":{"principalId":"YOURACCESSKEY"},"requestParameters":{"accessKey":"YOURACCESSKEY","region":"","sourceIPAddress":"10.244.0.0"},"responseElements":{"x-amz-request-id":"16313B5A71D964F8","x-minio-deployment-id":"c7cfef0d-b256-4514-94a1-0a14a6b469eb","x-minio-origin-endpoint":"http://10.244.2.25:9000"},"s3":{"s3SchemaVersion":"1.0","configurationId":"Config","bucket":{"name":"aml","ownerIdentity":{"principalId":"YOURACCESSKEY"},"arn":"arn:aws:s3:::aml"},"object":{"key":"_Robot_Grasp_AAS_Model.aml","size":5849928,"eTag":"7eafb3b517b94e1f041fc360e8b5f581","contentType":"application/octet-stream","userMetadata":{"content-type":"application/octet-stream"},"sequencer":"16313B5AD40396AF"}},"source":{"host":"10.244.0.0","port":"","userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"}}]}'
    payload = json.loads(payload_json)
    if payload['EventName'] != 's3:ObjectCreated:Put':
        return
    zeebe_msg(payload['Key'])


# client_id is a randomly generated unique ID for the mqtt broker to identify the connection.
client = mqtt.Client(client_id="myclientid", clean_session=False)

client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER)
client.loop_forever()
