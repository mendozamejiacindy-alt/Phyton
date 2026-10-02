from decimal import Decimal

from actividad_16.application.presenters import OrderPresenter
from actividad_16.application.use_cases import CreateOrder
from actividad_16.domain.entities import Order
from actividad_16.domain.events import OrderCreated
from actividad_16.infrastructure.memory_repository import MemoryOrderRepository
from actividad_16.infrastructure.unit_of_work import MemoryUnitOfWork


def test_order_domain() -> None:
    order = Order(
        product="Laptop",
        quantity=2,
        price=Decimal(15000),
    )

    assert order.product == "Laptop"
    assert order.quantity == 2
    assert order.total() == Decimal(30000)
    assert order.id is not None


def test_memory_repository() -> None:
    repository = MemoryOrderRepository()

    order = Order(
        product="Laptop",
        quantity=2,
        price=Decimal(15000),
    )

    repository.add(order)

    assert order.id is not None

    saved_order = repository.get_by_id(order.id)

    assert saved_order is not None
    assert saved_order.id == order.id
    assert saved_order.product == "Laptop"


def test_create_order_and_event() -> None:
    uow = MemoryUnitOfWork()
    use_case = CreateOrder(uow)

    event = use_case.execute(
        "Laptop",
        2,
        Decimal(15000),
    )

    assert isinstance(event, OrderCreated)
    assert event.product == "Laptop"
    assert event.quantity == 2
    assert event.order_id is not None


def test_presenter() -> None:
    uow = MemoryUnitOfWork()
    use_case = CreateOrder(uow)

    event = use_case.execute(
        "Laptop",
        2,
        Decimal(15000),
    )

    presenter = OrderPresenter()
    result = presenter.present(event)

    assert isinstance(result, dict)
    assert result["product"] == "Laptop"
    assert result["quantity"] == 2
    assert result["order_id"] == str(event.order_id)


def test_complete_clean_architecture_flow() -> None:
    uow = MemoryUnitOfWork()
    use_case = CreateOrder(uow)

    event = use_case.execute(
        "Laptop",
        2,
        Decimal(15000),
    )

    presenter = OrderPresenter()
    result = presenter.present(event)

    assert result["product"] == "Laptop"
    assert result["quantity"] == 2
    assert result["order_id"] == str(event.order_id)
