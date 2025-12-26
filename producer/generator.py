# producer/generator.py
import os
import json
import time
import uuid
import numpy as np
from datetime import datetime
from kafka import KafkaProducer

# Load learned stats
with open("models/stats.json") as f:
    stats = json.load(f)

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def generate_order():
    num_items = np.random.choice(
        list(map(int, stats["items_per_order_dist"].keys())),
        p=list(stats["items_per_order_dist"].values())
    )

    items = []
    for _ in range(num_items):
        category = np.random.choice(
            list(stats["product_category_dist"].keys()),
            p=list(stats["product_category_dist"].values())
        )
        items.append({
            "product_category": category,
            "quantity": np.random.randint(1, 4),
            "price": round(np.random.normal(50, 10), 2)
        })

    event = {
        "order_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "customer_state": np.random.choice(
            list(stats["customer_state_dist"].keys()),
            p=list(stats["customer_state_dist"].values())
        ),
        "items": items,
        "payment_value": round(
            np.random.normal(
                stats["payment_mean"],
                stats["payment_std"]
            ), 2
        )
    }

    return event


while True:
    # Poisson arrival rate
    orders_this_minute = np.random.poisson(
        stats["lambda_orders_per_minute"]*5
    )

    for _ in range(max(1, orders_this_minute)):
        event = generate_order()
        producer.send("orders", event)
        print("Produced:", event["order_id"], flush=True)

    time.sleep(5)

