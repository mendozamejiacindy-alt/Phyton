from uuid import UUID

from proyecto_final.application.ports import EventPublisher, OrderRepository
from proyecto_final.domain.entities import Order


class CreateOrder:
    def __init__(
        self,
        repository: OrderRepository,
        event_publisher: EventPublisher,
    ) -> None:
        self.repository = repository
        self.event_publisher = event_publisher

    def execute(
        self,
        product: str,
        quantity: int,
        price: float,
    ) -> Order:
        order = Order(
            product=product,
            quantity=quantity,
            price=price,
        )

        saved_order = self.repository.save(order)

        self.event_publisher.publish_order_created(saved_order)

        return saved_order


class GetOrder:
    def __init__(self, repository: OrderRepository) -> None:
        self.repository = repository

    def execute(self, order_id: UUID) -> Order:
        order = self.repository.get_by_id(order_id)

        if order is None:
            raise ValueError("Orden no encontrada.")

        return order


class ListOrders:
    def __init__(self, repository: OrderRepository) -> None:
        self.repository = repository

    def execute(self) -> list[Order]:
        return self.repository.list_all()


class DeleteOrder:
    def __init__(self, repository: OrderRepository) -> None:
        self.repository = repository

    def execute(self, order_id: UUID) -> None:
        self.repository.delete(order_id)
