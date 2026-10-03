from unittest.mock import MagicMock, patch

from actividad_18.proto import orders_pb2
from actividad_18.redis_events import publish_order_created


def test_create_order_request() -> None:
    request = orders_pb2.CreateOrderRequest(
        product="Laptop",
        quantity=2,
        price=15000.00,
    )

    assert request.product == "Laptop"
    assert request.quantity == 2
    assert request.price == 15000.00


def test_order_response() -> None:
    response = orders_pb2.OrderResponse(
        order_id="test-001",
        product="Laptop",
        quantity=2,
        price=15000.00,
        status="CREATED",
    )

    assert response.order_id == "test-001"
    assert response.product == "Laptop"
    assert response.quantity == 2
    assert response.price == 15000.00
    assert response.status == "CREATED"


@patch("actividad_18.redis_events.redis.Redis")
def test_publish_order_created(mock_redis: MagicMock) -> None:
    client = mock_redis.return_value

    publish_order_created(
        order_id="test-001",
        product="Laptop",
        quantity=2,
        price=15000.00,
    )

    mock_redis.assert_called_once_with(
        host="localhost",
        port=6379,
        decode_responses=True,
    )

    client.publish.assert_called_once()

    channel, event_json = client.publish.call_args.args

    assert channel == "orders"
    assert "OrderCreated" in event_json
    assert "test-001" in event_json
    assert "Laptop" in event_json
