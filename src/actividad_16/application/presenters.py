from actividad_16.domain.events import OrderCreated


class OrderPresenter:
    def present(self, event: OrderCreated) -> dict[str, str | int]:
        return {
            "order_id": str(event.order_id),
            "product": event.product,
            "quantity": event.quantity,
        }
