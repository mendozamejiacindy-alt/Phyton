from .models import Order
from .ports import OrderRepository


class OrderService:
    def __init__(self, repository: OrderRepository) -> None:
        self.repository = repository

    def create_order(
        self,
        order_or_product: Order | str,
        quantity: int | None = None,
        price: float | None = None,
    ) -> Order:
        if isinstance(order_or_product, Order):
            order = order_or_product
        else:
            if quantity is None or price is None:
                raise ValueError(
                    "quantity y price son obligatorios " "cuando se proporciona product"
                )

            next_id = self._next_id()

            order = Order(
                id=next_id,
                product=order_or_product,
                quantity=quantity,
                price=price,
            )

        self.repository.save(order)
        return order

    def get_order(self, order_id: int) -> Order | None:
        return self.repository.get(order_id)

    def _next_id(self) -> int:
        order_id = 1

        while self.repository.get(order_id) is not None:
            order_id += 1

        return order_id
