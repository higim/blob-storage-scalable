import os
import json
import time
from urllib.parse import unquote_plus

import psycopg2
from kafka import KafkaConsumer, errors

DB_URL = os.getenv("DATABASE_URL")
KAFKA_BROKER = os.getenv("KAFKA_BROKER")
KAFKA_GROUP_ID = "blob-events-group"
KAFKA_TOPIC = "new_file"

def get_connection():
    return psycopg2.connect(DB_URL)

def update_file_status(filename: str, status: str):
    print(f"Update {filename} with {status} in {DB_URL}")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE files SET status=%s WHERE filename=%s", (status, filename))
        conn.commit()
    except Exception as e:
        print("DB Update failed: ", e)
    finally:
        cur.close()
        conn.close()

print(f"Subscribing to kafka topic...")

# Retry loop until Kafka is ready
while True:
    try:
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=[KAFKA_BROKER],
            group_id=KAFKA_GROUP_ID,
            auto_offset_reset="earliest",
            enable_auto_commit=True
        )
        break
    except errors.NoBrokersAvailable:
        print("Kafka broker not ready, retrying in 5 seconds...")
        time.sleep(5)

print(f"✅ Subscribed to Kafka Topic: {KAFKA_TOPIC}")

try:
    for msg in consumer:
        # MinIO event comes as JSON
        event = json.loads(msg.value.decode("utf-8"))
        for record in event.get("Records", []):
            filename = record["s3"]["object"]["key"]
            filename = unquote_plus(filename)
            print(f"📥 Event received for: {filename}")
            update_file_status(filename, "uploaded")

except KeyboardInterrupt:
    print("⏹️ Kafka consumer stopped")
finally:
    consumer.close()