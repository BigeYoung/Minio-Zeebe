# Minio-Zeebe
MinIO Bucket Notification To Zeebe Message

## 预先配置

需要在k8s里安装 [minio](https://hub.helm.sh/charts/minio/minio) 和 [mosquitto](https://hub.helm.sh/charts/halkeye/mosquitto)

```sh
wget https://dl.min.io/client/mc/release/linux-amd64/mc
chmod +x mc
./mc event add local/txt arn:minio:sqs::1:mqtt
```


