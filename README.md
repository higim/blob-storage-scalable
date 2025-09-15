### Music Streaming File Upload POC

This repository contains a working proof-of-concept demonstrating the large-file upload pattern explained in [this blog post](https://higim.github.io/2025/09/12/Handling-Huge-File-Uploads-for-a-Music-Streaming-Platform.html):

- FastAPI – metadata API and pre-signed URLs
- MinIO – S3-compatible object storage
- Kafka – file upload events
- PostgreSQL – file metadata
- Docker Compose – local development environment

⚠️ Disclaimer: This is a POC to demonstrate the design pattern.
The code is minimal, procedural, and not meant for production.

### Getting started

Clone the repo:

`
git clone https://github.com/higim/blob-storage-scalable
cd blob-storage-scalable
`

Start the full stack:

`docker compose up --build`

### Accessing pre-signed URL

There is a known, hard to solve problem to make MinIO accessible from your host machine. If you want to test pre-signed URLs outside Docker, you have to add the name resolution to /etc/hosts:

`sudo sh -c 'echo "127.0.0.1 minio" >> /etc/hosts`

### MinIO Configuration with mc

I had some problems with the auto-configuration of MinIO with the init container, sometimes the variable enabling the kafka notification seems to not work, so you might have to do it manually. Install mc or use a minio/mc docker image.

```
mc alias set local http://minio:9000 minio minio123

mc mb -p local/files || true

mc admin config set localminio notify_kafka:PRIMARY enable=true

mc event add local/files arn:minio:sqs::MINIO: --event put
``

### Notes

- Abandoned uploads: The consumer updates the DB only after the file lands in MinIO. For expired or abandoned uploads, consider TTLs or background cleanup jobs.
- POC only: No OOP or clean-code patterns are used here; the focus is demonstrating the architecture.
- Scaling considerations: In production, replace MinIO with S3 (or equivalent), add persistent Kafka storage, and implement retries/error handling for the consumer.
