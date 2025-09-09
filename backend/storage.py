import os
from datetime import timedelta

from minio import Minio

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
BUCKET_NAME = "music-bucket"
EXPIRING = 1 # in hours

client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

if not client.bucket_exists(BUCKET_NAME):
    client.make_bucket(BUCKET_NAME)

def generate_presigned_url(filename: str) -> str:
    return client.presigned_put_object(BUCKET_NAME, filename, expires=timedelta(hours=EXPIRING))