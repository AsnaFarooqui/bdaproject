import time
import json
import os
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
from pymongo import MongoClient

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
MONGO_URI = os.getenv("MONGO_URI", "mongo://mongo:27017")

mongo_client = MongoClient(MONGO_URI)
db = mongo_client["bda_project"]
orders_col = db["orders_stream"]

def create_consumer():
    while True:
        try:
            consumer = KafkaConsumer(
                "orders",
                bootstrap_servers=KAFKA_BOOTSTRAP,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                auto_offset_reset="earliest",
                enable_auto_commit=True,
                group_id="mongo-consumer",
                api_version_auto_timeout_ms=30000
            )
            print("Kafka consumer connected.")
            return consumer
        except NoBrokersAvailable:
            print("Kafka not ready, retrying in 5 seconds...")
            time.sleep(5)

consumer = create_consumer()

for message in consumer:
    orders_col.insert_one(message.value)
    print("Inserted: ", message.value["order_id"], flush=True)
