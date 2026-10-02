from decimal import Decimal

from actividad_15.application.ports import (
    NotificationPort,
    OrderRepository,
)
from actividad_15.domain.entities import Order


class CreateOrder:
    """Caso de uso para crear una orden."""

    def __init__(
        self,
        repository: OrderRepository,
        notification: NotificationPort,
    ) -> None:
        self.repository = repository
        self.notification = notification

    def execute(
        self,
        product: str,
        quantity: int,
        price: Decimal,
    ) -> Order:
        """Crea, valida, guarda y notifica una orden."""
        order = Order(
            product=product,
            quantity=quantity,
            price=price,
        )

        order.validate()

        saved_order = self.repository.save(order)
        self.notification.send_order_created(saved_order)

        return saved_order
