from decimal import Decimal

from actividad_15.application.use_cases import CreateOrder
from actividad_15.domain.entities import Order
from actividad_15.infrastructure.memory_repository import (
    MemoryOrderRepository,
)
from actividad_15.infrastructure.notification import (
    HttpNotificationAdapter,
)
from actividad_15.infrastructure.sqlalchemy_repository import (
    SQLAlchemyOrderRepository,
)


def test_order_domain() -> None:
    order = Order(
        product="Laptop",
        quantity=2,
        price=Decimal(15000),
    )

    order.validate()

    assert order.product == "Laptop"
    assert order.quantity == 2
    assert order.total() == Decimal(30000)


def test_memory_repository() -> None:
    repository = MemoryOrderRepository()

    order = Order(
        product="Laptop",
        quantity=2,
        price=Decimal(15000),
    )

    repository.save(order)

    saved_order = repository.get_by_id(order.id)

    assert saved_order is not None
    assert saved_order.id == order.id
    assert saved_order.product == "Laptop"


def test_sqlalchemy_repository() -> None:
    repository = SQLAlchemyOrderRepository()

    order = Order(
        product="Laptop",
        quantity=2,
        price=Decimal(15000),
    )

    repository.save(order)

    saved_order = repository.get_by_id(order.id)

    assert saved_order is not None
    assert saved_order.id == order.id
    assert saved_order.product == "Laptop"
    assert saved_order.total() == Decimal(30000)


def test_create_order_with_memory_repository() -> None:
    repository = MemoryOrderRepository()
    notification = HttpNotificationAdapter()

    use_case = CreateOrder(repository, notification)

    order = use_case.execute(
        "Laptop",
        2,
        Decimal(15000),
    )

    assert order.product == "Laptop"
    assert order.quantity == 2
    assert order.total() == Decimal(30000)
    assert repository.get_by_id(order.id) is not None
    assert len(notification.sent_notifications) == 1


def test_create_order_with_sqlalchemy_repository() -> None:
    repository = SQLAlchemyOrderRepository()
    notification = HttpNotificationAdapter()

    use_case = CreateOrder(repository, notification)

    order = use_case.execute(
        "Laptop",
        2,
        Decimal(15000),
    )

    saved_order = repository.get_by_id(order.id)

    assert saved_order is not None
    assert saved_order.product == "Laptop"
    assert saved_order.quantity == 2
    assert saved_order.total() == Decimal(30000)
    assert len(notification.sent_notifications) == 1


def test_notification_adapter() -> None:
    notification = HttpNotificationAdapter()

    order = Order(
        product="Laptop",
        quantity=2,
        price=Decimal(15000),
    )

    notification.send_order_created(order)

    assert len(notification.sent_notifications) == 1
    assert "Laptop" in notification.sent_notifications[0]
    assert "30000" in notification.sent_notifications[0]
