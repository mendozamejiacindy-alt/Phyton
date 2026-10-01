import pytest

from .models import Order
from .repositories import (
    MemoryOrderRepository,
    SqlOrderRepository,
)
from .service import OrderService


@pytest.fixture(
    params=[
        MemoryOrderRepository,
        SqlOrderRepository,
    ]
)
def repository(request):
    return request.param()


def test_create_and_get_order(repository):
    service = OrderService(repository)

    order = Order(
        id=1,
        product="Laptop",
        quantity=1,
        price=15000,
    )

    service.create_order(order)

    result = service.get_order(1)

    assert result == order
    assert result is not None
    assert result.product == "Laptop"
    assert result.quantity == 1
    assert result.price == 15000


def test_create_order_with_values():
    repository = MemoryOrderRepository()
    service = OrderService(repository)

    order = service.create_order(
        "Laptop",
        1,
        15000,
    )

    assert order.product == "Laptop"
    assert order.quantity == 1
    assert order.price == 15000
    assert order.id == 1


@pytest.mark.parametrize(
    "repository_class",
    [
        MemoryOrderRepository,
        SqlOrderRepository,
    ],
)
def test_missing_order_returns_none(repository_class):
    repository = repository_class()
    service = OrderService(repository)

    result = service.get_order(999)

    assert result is None


def test_memory_repository_lsp():
    repository = MemoryOrderRepository()
    service = OrderService(repository)

    order = Order(
        id=1,
        product="Laptop",
        quantity=1,
        price=15000,
    )

    service.create_order(order)

    result = service.get_order(1)

    assert result == order


def test_sql_repository_lsp():
    repository = SqlOrderRepository()
    service = OrderService(repository)

    order = Order(
        id=1,
        product="Laptop",
        quantity=1,
        price=15000,
    )

    service.create_order(order)

    result = service.get_order(1)

    assert result == order


def test_order_is_immutable():
    order = Order(
        id=1,
        product="Laptop",
        quantity=1,
        price=15000,
    )

    with pytest.raises(AttributeError):
        order.price = 20000


def test_service_uses_repository():
    repository = MemoryOrderRepository()
    service = OrderService(repository)

    order = Order(
        id=1,
        product="Laptop",
        quantity=1,
        price=15000,
    )

    service.create_order(order)

    assert repository.get(1) == order


def test_order_total():
    order = Order(
        id=1,
        product="Laptop",
        quantity=2,
        price=15000,
    )

    assert order.total == 30000
