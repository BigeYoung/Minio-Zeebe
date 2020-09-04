import json
import logging
import grpc
from zeebe_grpc import gateway_pb2, gateway_pb2_grpc
with grpc.insecure_channel("116.57.83.11:30200") as channel:
    stub = gateway_pb2_grpc.GatewayStub(channel)

    # start a workflow instance
    variable = {"aml": "1.aml"}
    createResponse = stub.CreateWorkflowInstance(
        gateway_pb2.CreateWorkflowInstanceRequest(
            bpmnProcessId='aml2owl-process-id',
            version=-1,
            variables=json.dumps(variable)
        )
    )

    variables = {"aml_path": "1.aml"}
    createResponse = stub.PublishMessage(
        gateway_pb2.PublishMessageRequest(
            # the name of the message
            name = "aml_uploaded",
            # how long the message should be buffered on the broker, in milliseconds
            timeToLive = 100000,
            correlationKey = "aml_path",
            # the unique ID of the message; can be omitted. only useful to ensure only one message
            # with the given ID will ever be published (during its lifetime)
            # the message variables as a JSON document; to be valid, the root of the document must be an
            # object, e.g. { "a": "foo" }. [ "foo" ] would not be valid.
            variables = json.dumps(variables)
        )
    )
    
    print(createResponse)