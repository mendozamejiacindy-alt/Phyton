from proyecto_final.application.ports import EventPublisher
from proyecto_final.domain.entities import Order


class ConsoleEventPublisher(EventPublisher):
    def publish_order_created(self, order: Order) -> None:
        print(
            f"EVENTO OrderCreated | "
            f"id={order.order_id} | "
            f"producto={order.product} | "
            f"cantidad={order.quantity} | "
            f"precio={order.price:.2f}"
        )
