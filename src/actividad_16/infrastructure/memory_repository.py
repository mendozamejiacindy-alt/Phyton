from uuid import UUID

from actividad_16.domain.entities import Order


class MemoryOrderRepository:
    def __init__(self) -> None:
        self.orders: dict[UUID, Order] = {}

    def add(self, order: Order) -> None:
        if order.id is None:
            raise ValueError("La orden debe tener un ID.")

        self.orders[order.id] = order

    def get_by_id(self, order_id: UUID) -> Order | None:
        return self.orders.get(order_id)
