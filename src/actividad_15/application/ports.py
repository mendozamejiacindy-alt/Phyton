from typing import Protocol
from uuid import UUID

from actividad_15.domain.entities import Order


class OrderRepository(Protocol):
    """Puerto para almacenar y recuperar órdenes."""

    def save(self, order: Order) -> Order:
        """Guarda una orden."""
        ...

    def get_by_id(self, order_id: UUID) -> Order | None:
        """Busca una orden por su identificador."""
        ...


class NotificationPort(Protocol):
    """Puerto para enviar notificaciones."""

    def send_order_created(self, order: Order) -> None:
        """Notifica que una orden fue creada."""
        ...
