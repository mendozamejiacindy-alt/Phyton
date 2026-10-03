from uuid import UUID

from proyecto_final.domain.entities import Order


class InMemoryOrderRepository:
    def __init__(self) -> None:
        self.orders: dict[UUID, Order] = {}

    def save(self, order: Order) -> Order:
        self.orders[order.id] = order
        return order

    def get_by_id(self, order_id: UUID) -> Order | None:
        return self.orders.get(order_id)

    def list_all(self) -> list[Order]:
        return list(self.orders.values())

    def delete(self, order_id: UUID) -> None:
        self.orders.pop(order_id, None)
