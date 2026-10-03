from uuid import UUID

import pytest

from proyecto_final.application.use_cases import (
    CreateOrder,
    DeleteOrder,
    GetOrder,
    ListOrders,
)
from proyecto_final.infrastructure.event_publisher import ConsoleEventPublisher
from proyecto_final.infrastructure.memory_repository import InMemoryOrderRepository


@pytest.fixture
def repository() -> InMemoryOrderRepository:
    return InMemoryOrderRepository()


@pytest.fixture
def publisher() -> ConsoleEventPublisher:
    return ConsoleEventPublisher()


def test_create_order(repository, publisher, capsys) -> None:
    use_case = CreateOrder(repository, publisher)

    order = use_case.execute(
        product="Laptop",
        quantity=2,
        price=15000.00,
    )

    assert isinstance(order.id, UUID)
    assert order.product == "Laptop"
    assert order.quantity == 2
    assert order.price == 15000.00
    assert order.status == "CREATED"
    assert order.total() == 30000.00

    captured = capsys.readouterr()

    assert "EVENTO OrderCreated" in captured.out
    assert "Laptop" in captured.out


def test_get_order(repository, publisher) -> None:
    create_order = CreateOrder(repository, publisher)
    get_order = GetOrder(repository)

    created = create_order.execute(
        product="Monitor",
        quantity=1,
        price=5000.00,
    )

    result = get_order.execute(created.id)

    assert result is not None
    assert result.id == created.id
    assert result.product == "Monitor"
    assert result.quantity == 1
    assert result.price == 5000.00


def test_list_orders(repository, publisher) -> None:
    create_order = CreateOrder(repository, publisher)
    list_orders = ListOrders(repository)

    create_order.execute(
        product="Laptop",
        quantity=1,
        price=15000.00,
    )

    create_order.execute(
        product="Mouse",
        quantity=2,
        price=500.00,
    )

    orders = list_orders.execute()

    assert len(orders) == 2
    assert orders[0].product == "Laptop"
    assert orders[1].product == "Mouse"


def test_delete_order(repository, publisher) -> None:
    create_order = CreateOrder(repository, publisher)
    delete_order = DeleteOrder(repository)
    get_order = GetOrder(repository)

    created = create_order.execute(
        product="Keyboard",
        quantity=1,
        price=800.00,
    )

    delete_order.execute(created.id)

    with pytest.raises(ValueError, match="Orden no encontrada."):
        get_order.execute(created.id)
