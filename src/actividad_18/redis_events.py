import json
from datetime import UTC, datetime

import redis

REDIS_HOST = "localhost"
REDIS_PORT = 6379
CHANNEL = "orders"


def publish_order_created(
    order_id: str,
    product: str,
    quantity: int,
    price: float,
) -> None:
    client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        decode_responses=True,
    )

    event = {
        "event": "OrderCreated",
        "order_id": order_id,
        "product": product,
        "quantity": quantity,
        "price": price,
        "created_at": datetime.now(UTC).isoformat(),
    }

    client.publish(CHANNEL, json.dumps(event))

    print("Evento publicado:")
    print(json.dumps(event, indent=2))


def listen_orders() -> None:
    client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        decode_responses=True,
    )

    pubsub = client.pubsub()
    pubsub.subscribe(CHANNEL)

    print(f"Escuchando eventos en el canal '{CHANNEL}'...")

    for message in pubsub.listen():
        if message["type"] == "message":
            print("\nEvento recibido:")
            print(message["data"])


if __name__ == "__main__":
    publish_order_created(
        order_id="demo-001",
        product="Laptop",
        quantity=2,
        price=15000.00,
    )
