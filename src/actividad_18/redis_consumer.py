import redis

REDIS_HOST = "localhost"
REDIS_PORT = 6379
CHANNEL = "orders"


def main() -> None:
    client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        decode_responses=True,
    )

    pubsub = client.pubsub()
    pubsub.subscribe(CHANNEL)

    print(f"Escuchando eventos en el canal '{CHANNEL}'...")
    print("Esperando eventos...")

    for message in pubsub.listen():
        if message["type"] == "message":
            print("\nEvento recibido:")
            print(message["data"])


if __name__ == "__main__":
    main()
