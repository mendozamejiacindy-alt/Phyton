from decimal import Decimal

from actividad_16.application.ports import UnitOfWork
from actividad_16.domain.entities import Order
from actividad_16.domain.events import OrderCreated


class CreateOrder:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def execute(
        self,
        product: str,
        quantity: int,
        price: Decimal,
    ) -> OrderCreated:
        order = Order(
            product=product,
            quantity=quantity,
            price=price,
        )

        with self.uow:
            self.uow.orders.add(order)
            self.uow.commit()

        assert order.id is not None

        return OrderCreated(
            order_id=order.id,
            product=order.product,
            quantity=order.quantity,
        )
