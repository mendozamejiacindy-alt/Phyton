from uuid import UUID

from actividad_15.domain.entities import Order


class MemoryOrderRepository:
    """Adaptador de repositorio que almacena órdenes en memoria."""

    def __init__(self) -> None:
        self.orders: dict[UUID, Order] = {}

    def save(self, order: Order) -> Order:
        """Guarda una orden en memoria."""
        self.orders[order.id] = order
        return order

    def get_by_id(self, order_id: UUID) -> Order | None:
        """Busca una orden por su identificador."""
        return self.orders.get(order_id)
