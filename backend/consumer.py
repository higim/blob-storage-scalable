import os
import json
import threading

from kafka import KafkaConsumer

KAFKA_BROKER = os.getenv("KAFKA_BROKER")
KAFKA_GROUP_ID = "blob-events-group"
KAFKA_TOPIC = "new_file"

print(f"KAFKA_BROKER: {KAFKA_BROKER}")

def consume_events():
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
                print(f"📥 Event received for: {filename}")

    except KeyboardInterrupt:
        print("⏹️ Kafka consumer stopped")
    finally:
        consumer.close()

def start_consumer_thread():
    t = threading.Thread(target=consume_events, daemon=True)
    t.start()
