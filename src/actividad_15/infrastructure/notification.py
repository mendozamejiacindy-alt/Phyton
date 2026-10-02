from actividad_15.domain.entities import Order


class HttpNotificationAdapter:
    """Adaptador HTTP simulado para enviar notificaciones."""

    def __init__(self) -> None:
        self.sent_notifications: list[str] = []

    def send_order_created(self, order: Order) -> None:
        """Simula el envío de una notificación HTTP."""
        message = (
            f"Orden creada: {order.id} - "
            f"Producto: {order.product} - "
            f"Total: {order.total()}"
        )

        self.sent_notifications.append(message)
