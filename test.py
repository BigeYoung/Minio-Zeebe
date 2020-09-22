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


zeebe_msg("aml/CPPS.aml")
